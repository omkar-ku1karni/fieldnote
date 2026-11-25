"""The encoders, one per modality. Loaded on first use, all open weights, all local.

  pages   ColSmol-256M        multi-vector retriever over page images
  photos  SigLIP2 so400m/384  image/text encoder for job photos
  text    bge-base-en-v1.5    dense text (manual chunks, call transcripts)
  sparse  BM25                so part numbers like "VPN-5520" match exactly
  rerank  MiniLM-L6           cross-encoder, off by default
"""
from __future__ import annotations

import math
import os
import re
import zlib
from collections import Counter
from functools import lru_cache

import numpy as np

import fieldnote.config  # noqa: F401  (sets HF_HOME before anything from HF is imported)

PAGE_MODEL = os.getenv("FIELDNOTE_PAGE_MODEL", "vidore/colSmol-256M")
PHOTO_MODEL = os.getenv("FIELDNOTE_PHOTO_MODEL", "google/siglip2-so400m-patch14-384")
TEXT_MODEL = os.getenv("FIELDNOTE_TEXT_MODEL", "BAAI/bge-base-en-v1.5")
RERANK_MODEL = os.getenv("FIELDNOTE_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L6-v2")
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def device() -> str:
    import torch
    if os.getenv("FIELDNOTE_DEVICE"):
        return os.environ["FIELDNOTE_DEVICE"]
    return "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"


# --- pages (ColSmol)

@lru_cache(maxsize=1)
def _colsmol():
    import torch
    from colpali_engine.models import ColIdefics3, ColIdefics3Processor
    # Loading straight onto MPS segfaults with this torch build. CPU first, then move it.
    model = ColIdefics3.from_pretrained(PAGE_MODEL, torch_dtype=torch.float32).eval().to(device())
    return model, ColIdefics3Processor.from_pretrained(PAGE_MODEL)


def _unpad(emb, mask) -> list[np.ndarray]:
    return [e[m.bool()].float().cpu().numpy() for e, m in zip(emb, mask)]


def encode_pages(images, batch_size: int = 4) -> list[np.ndarray]:
    """One (n_patches, 128) array per page."""
    import torch
    model, proc = _colsmol()
    out = []
    for i in range(0, len(images), batch_size):
        b = proc.process_images(images[i:i + batch_size]).to(model.device)
        with torch.no_grad():
            out += _unpad(model(**b), b["attention_mask"])
    return out


def encode_page_query(q: str) -> np.ndarray:
    import torch
    model, proc = _colsmol()
    b = proc.process_queries([q]).to(model.device)
    with torch.no_grad():
        return _unpad(model(**b), b["attention_mask"])[0]


# --- photos (SigLIP2)

@lru_cache(maxsize=1)
def _siglip():
    from transformers import AutoModel, AutoProcessor
    return AutoModel.from_pretrained(PHOTO_MODEL).eval(), AutoProcessor.from_pretrained(PHOTO_MODEL)


def _pooled(x):
    x = getattr(x, "pooler_output", x)
    x = x / x.norm(dim=-1, keepdim=True)
    return x.cpu().numpy()


def encode_photos(images, batch_size: int = 8) -> np.ndarray:
    import torch
    model, proc = _siglip()
    out = []
    for i in range(0, len(images), batch_size):
        with torch.no_grad():
            out.append(_pooled(model.get_image_features(**proc(images=images[i:i + batch_size], return_tensors="pt"))))
    return np.concatenate(out)


def encode_photo_query(q: str) -> np.ndarray:
    import torch
    model, proc = _siglip()
    text = f"a photo of {q.lower().rstrip('?.')}"
    with torch.no_grad():
        return _pooled(model.get_text_features(**proc(text=[text], padding="max_length", max_length=64,
                                                      truncation=True, return_tensors="pt")))[0]


def encode_photo_query_from_image(img) -> np.ndarray:
    return encode_photos([img])[0]


# --- text (bge) and reranking

@lru_cache(maxsize=1)
def _bge():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(TEXT_MODEL, device="cpu")


def encode_texts(texts: list[str]) -> np.ndarray:
    return _bge().encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)


def encode_text_query(q: str) -> np.ndarray:
    return _bge().encode([BGE_QUERY_PREFIX + q], normalize_embeddings=True)[0]


@lru_cache(maxsize=2)
def _reranker(name: str = RERANK_MODEL):
    from sentence_transformers import CrossEncoder
    return CrossEncoder(name, device="cpu")


def rerank(query: str, passages: list[str], model: str | None = None) -> np.ndarray:
    if not passages:
        return np.array([])
    return np.asarray(_reranker(model or RERANK_MODEL).predict([(query, p) for p in passages], show_progress_bar=False))


# --- BM25

TOKEN = re.compile(r"[a-z0-9]+(?:[-./][a-z0-9]+)*")
K1, B = 1.2, 0.75


def tokenize(text: str) -> list[str]:
    toks = TOKEN.findall(text.lower())
    # keep hyphenated ids whole and also split: "vpn-5520" -> vpn-5520, vpn, 5520
    out = []
    for t in toks:
        out.append(t)
        if "-" in t:
            out += t.split("-")
    return out


def _idx(tok: str) -> int:
    return zlib.crc32(tok.encode()) & 0x7FFFFFFF


def bm25_doc(text: str, avgdl: float) -> tuple[list[int], list[float]]:
    """The TF half of BM25. Qdrant's IDF modifier adds the IDF half at query time."""
    tf = Counter(tokenize(text))
    dl = sum(tf.values()) or 1
    items = {}
    for tok, f in tf.items():
        items[_idx(tok)] = f * (K1 + 1) / (f + K1 * (1 - B + B * dl / avgdl))
    return list(items), list(items.values())


def bm25_query(text: str) -> tuple[list[int], list[float]]:
    idx = sorted({_idx(t) for t in tokenize(text)})
    return idx, [1.0] * len(idx)


def avg_len(texts: list[str]) -> float:
    return max(1.0, sum(len(tokenize(t)) for t in texts) / max(1, len(texts)))


def warmup(pages: bool = True, photos: bool = True, text: bool = True, rerank_model: bool = True) -> None:
    """Load the models one at a time on this thread. transformers' lazy imports aren't thread-safe,
    and the first parallel search used to crash with an ImportError."""
    if text:
        _bge()
    if rerank_model:
        _reranker(rerank_model if isinstance(rerank_model, str) else RERANK_MODEL)
    if photos:
        _siglip()
    if pages:
        _colsmol()


def maxsim(q: np.ndarray, d: np.ndarray) -> float:
    return float((q @ d.T).max(axis=1).sum())


def safe_log(x: float) -> float:
    return math.log(max(x, 1e-9))
