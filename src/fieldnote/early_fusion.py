"""Early-fusion ablation: everything in one SigLIP2 space.

Pages, photos, text chunks and call windows all go into a single collection (image tower for
pixels, text tower for words) and a query does one search. It does a lot worse, mostly because:
  1. the text tower stops at 64 tokens, so most of a 180-word chunk is never read, and
  2. image-text and text-text similarities aren't on the same scale, so one kind of item
     ends up hogging the top of the ranking.

Run:  uv run python -m fieldnote.early_fusion index
      uv run python -m fieldnote.evaluate retrieval --configs early_fusion
"""
from __future__ import annotations

import sys
import time

import numpy as np
from PIL import Image

from fieldnote import encoders as E
from fieldnote.config import GENERATED
from fieldnote.ingest import PAGES_DIR, client

COLLECTION = "early_fusion"


def _scroll(name: str) -> list[dict]:
    c, out, offset = client(), [], None
    while True:
        pts, offset = c.scroll(name, limit=512, offset=offset, with_payload=True, with_vectors=False)
        out += [p.payload for p in pts]
        if offset is None:
            return out


def encode_texts_siglip(texts: list[str], batch: int = 16) -> np.ndarray:
    import torch
    model, proc = E._siglip()
    out = []
    for i in range(0, len(texts), batch):
        with torch.no_grad():
            out.append(E._pooled(model.get_text_features(**proc(
                text=[t.lower() for t in texts[i:i + batch]], padding="max_length", max_length=64,
                truncation=True, return_tensors="pt"))))
    return np.concatenate(out)


def build() -> None:
    from qdrant_client import models as qm
    t0 = time.time()
    pages, texts = _scroll("pages"), _scroll("text")
    photos = _scroll("photos")
    page_vecs = E.encode_photos([Image.open(PAGES_DIR / p["image"]).convert("RGB") for p in pages])
    print(f"pages: {len(pages)} ({time.time() - t0:.0f}s)", flush=True)
    text_vecs = encode_texts_siglip([t["text"] for t in texts])
    print(f"text: {len(texts)} ({time.time() - t0:.0f}s)", flush=True)
    photo_vecs = E.encode_photos([Image.open(GENERATED / "photos" / p["file"]).convert("RGB") for p in photos])
    c = client()
    if c.collection_exists(COLLECTION):
        c.delete_collection(COLLECTION)
    c.create_collection(COLLECTION, vectors_config={"siglip": qm.VectorParams(size=page_vecs.shape[1],
                                                                              distance=qm.Distance.COSINE)})
    items = [(p, v) for p, v in zip(pages, page_vecs)] + [(t, v) for t, v in zip(texts, text_vecs)] + \
            [(p, v) for p, v in zip(photos, photo_vecs)]
    c.upsert(COLLECTION, [qm.PointStruct(id=i, vector={"siglip": v.tolist()}, payload=p)
                          for i, (p, v) in enumerate(items)])
    print(f"{COLLECTION}: {len(items)} points in one space ({time.time() - t0:.0f}s)")


def retrieve(query: str, k: int = 20):
    from fieldnote.retrieve import Hit, unit_key
    pts = client().query_points(COLLECTION, query=E.encode_photo_query(query).tolist(), using="siglip",
                                limit=k * 3, with_payload=True).points
    seen, hits = set(), []
    for p in pts:
        key = unit_key(p.payload["modality"], p.payload)
        if (p.payload["modality"], key) in seen:
            continue
        seen.add((p.payload["modality"], key))
        hits.append(Hit(p.payload["modality"], key, p.score, p.payload, ["early-fusion"]))
    return hits[:k], dict(timings={})


if __name__ == "__main__":
    if sys.argv[1:] == ["index"]:
        build()
