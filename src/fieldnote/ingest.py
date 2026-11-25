"""Build the index from the generated corpus.

Three collections in embedded Qdrant (data/index/qdrant). Every point has a `modality` field.

  pages   one point per PDF page: ColSmol multi-vectors over the rendered page image
  photos  one point per job photo: SigLIP2 image embedding plus job metadata
  text    manual/bulletin/register chunks and call-transcript windows: bge dense + BM25 sparse

Figures are found from the PDF's own image objects (not from the generator's records) and
cropped, so an answer can cite the crop and the page it came from.

Run:  uv run python -m fieldnote.ingest [--no-asr-prompt] [--only text,photos]
"""
from __future__ import annotations

import argparse
import json
import re
import threading
import time

import numpy as np
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from PIL import Image

from fieldnote import encoders as E
from fieldnote.config import DATA, GENERATED, SPEC

INDEX = DATA / "index"
PAGES_DIR = GENERATED / "pages"
CROPS_DIR = GENERATED / "crops"
TRANSCRIPTS = GENERATED / "transcripts"
RENDER_SCALE = 2.0  # 144 dpi
CHUNK_WORDS, OVERLAP_WORDS = 180, 40
CALL_WINDOW_S = 40.0
HEADING = re.compile(r"^\d+(\.\d+)*\.?\s+[A-Z][^.]{2,80}$")
FOOTER = re.compile(r"^(Vantorr Climate Systems|Ridgeline Mechanical Services) .*Page \d+\s*$", re.M)

# Passed to Whisper as initial_prompt. Without it, it mangles the made-up brand and model names.
ASR_VOCAB = ("Vantorr Technical Support. Ridgeline Mechanical. VRT, VHP, VCU, VAH, VRL. VCB-200, VCB-400, VAB-50. "
             "RTU, debounce, high-pressure switch, contactor, capacitor, economizer, DIP switch, R-454B.")


_CLIENT = None
_CLIENT_LOCK = threading.Lock()


def client():
    """Shared Qdrant client. Embedded mode allows one client per folder, hence the lock."""
    global _CLIENT
    with _CLIENT_LOCK:
        if _CLIENT is None:
            import os

            from qdrant_client import QdrantClient
            INDEX.mkdir(parents=True, exist_ok=True)
            # Point this at a copy of the index to run an eval while the app has the real one open.
            _CLIENT = QdrantClient(path=os.getenv("FIELDNOTE_QDRANT_PATH", str(INDEX / "qdrant")))
        return _CLIENT


# --- documents

def process_docs() -> tuple[list[dict], list[dict]]:
    """Render pages, crop figures and chunk the text. Returns (pages, chunks)."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    pages, chunks = [], []
    for d in json.loads((GENERATED / "docs.json").read_text()):
        pdf = pdfium.PdfDocument(GENERATED / "docs" / d["file"])
        title = pdf[0].get_textpage().get_text_range().strip().splitlines()[0].strip()
        section = ""
        for pno in range(len(pdf)):
            page = pdf[pno]
            w_pt, h_pt = page.get_size()
            img = page.render(scale=RENDER_SCALE).to_pil().convert("RGB")
            img_path = PAGES_DIR / f"{d['doc_id']}_p{pno + 1:03d}.jpg"
            img.save(img_path, quality=85)
            figs = []
            for k, obj in enumerate(page.get_objects(filter=[pdfium_c.FPDF_PAGEOBJ_IMAGE])):
                left, bottom, right, top = obj.get_bounds()
                if (right - left) * (top - bottom) < 0.05 * w_pt * h_pt:
                    continue  # logos and other small images
                box = [left / w_pt, 1 - top / h_pt, right / w_pt, 1 - bottom / h_pt]  # normalized, top-left origin
                crop = img.crop((int(box[0] * img.width), int(box[1] * img.height),
                                 int(box[2] * img.width), int(box[3] * img.height)))
                crop_path = CROPS_DIR / f"{d['doc_id']}_p{pno + 1:03d}_f{k}.jpg"
                crop.save(crop_path, quality=90)
                figs.append(dict(bbox=[round(v, 4) for v in box], crop=crop_path.name))
            text = FOOTER.sub("", page.get_textpage().get_text_range()).replace("\r", "")
            text = re.sub(r"[ \t]+", " ", text).strip()
            pages.append(dict(modality="page", doc_id=d["doc_id"], kind=d["kind"], title=title, page=pno + 1,
                              image=img_path.name, figures=figs, text=text))
            # Track the current section heading per word, across page breaks too. Otherwise a table that
            # spills onto the next page loses its "VRT-060" heading and nothing can find it.
            words, word_sections = [], []
            for line in text.splitlines():
                if HEADING.match(line.strip()):
                    section = line.strip()
                for w in line.split():
                    words.append(w)
                    word_sections.append(section)
            step = CHUNK_WORDS - OVERLAP_WORDS
            for ci, i in enumerate(range(0, max(1, len(words) - OVERLAP_WORDS), step)):
                chunk = " ".join(words[i:i + CHUNK_WORDS])
                sec = word_sections[i] if word_sections else section
                chunks.append(dict(modality="doc_text", doc_id=d["doc_id"], kind=d["kind"], title=title,
                                   page=pno + 1, chunk=ci, section=sec, text=chunk,
                                   embed_text=f"{title} — {sec} — page {pno + 1}\n{chunk}"))
    return pages, chunks


# --- calls

def transcribe_calls(use_prompt: bool) -> list[dict]:
    import soundfile as sf
    from faster_whisper import WhisperModel
    tag = "vocab" if use_prompt else "plain"
    out_dir = TRANSCRIPTS / tag
    out_dir.mkdir(parents=True, exist_ok=True)
    model = None
    results = []
    for meta_path in sorted((GENERATED / "calls").glob("C*.json")):
        meta = json.loads(meta_path.read_text())
        cache = out_dir / f"{meta['call_id']}.json"
        if not cache.exists():
            if model is None:
                model = WhisperModel("small.en", device="cpu", compute_type="int8")
            audio, sr = sf.read(meta_path.with_suffix(".ogg"), dtype="float32")
            segs, _ = model.transcribe(audio, vad_filter=True, beam_size=5,
                                       initial_prompt=ASR_VOCAB if use_prompt else None)
            cache.write_text(json.dumps([dict(start=round(s.start, 2), end=round(s.end, 2), text=s.text.strip())
                                         for s in segs], indent=0))
        results.append(dict(meta=meta, segments=json.loads(cache.read_text())))
    return results


def call_chunks(transcripts: list[dict]) -> list[dict]:
    world = json.loads((SPEC / "world.json").read_text())
    site_ids = {s["name"]: s["id"] for s in world["sites"]}
    out = []
    for t in transcripts:
        m = t["meta"]
        site_id = next((sid for name, sid in site_ids.items() if m["site"].startswith(name)), None)
        header = f"Support call {m['date']} — {m['site']}, {m['unit']} ({m['model']}), tech {m['tech']}"
        segs, win = t["segments"], []
        for i, s in enumerate(segs):
            win.append(s)
            if s["end"] - win[0]["start"] >= CALL_WINDOW_S or i == len(segs) - 1:
                text = " ".join(x["text"] for x in win)
                out.append(dict(modality="call", call_id=m["call_id"], start=win[0]["start"], end=win[-1]["end"],
                                date=m["date"], site=m["site"], site_id=site_id, unit=m["unit"], model=m["model"],
                                tech=m["tech"], text=text, embed_text=f"{header}\n{text}"))
                win = win[-1:] if i < len(segs) - 1 else []  # one-segment overlap
    return out


# --- index

def build(use_prompt: bool = True, only: set[str] | None = None) -> None:
    only = only or {"pages", "photos", "text"}
    t0 = time.time()
    pages, doc_chunks = process_docs()
    print(f"docs: {len(pages)} pages, {sum(len(p['figures']) for p in pages)} figures, "
          f"{len(doc_chunks)} text chunks ({time.time() - t0:.0f}s)")
    transcripts = transcribe_calls(use_prompt)
    calls = call_chunks(transcripts)
    print(f"calls: {len(transcripts)} transcribed, {len(calls)} windows ({time.time() - t0:.0f}s)")
    photos = json.loads((SPEC / "photos.json").read_text())
    world = json.loads((SPEC / "world.json").read_text())
    site_names = {s["id"]: s["name"] for s in world["sites"]}

    c = client()
    for name in only:
        if c.collection_exists(name):
            c.delete_collection(name)

    texts = doc_chunks + calls
    if "text" in only:
        _index_text(c, texts)
        print(f"text: {len(texts)} points ({time.time() - t0:.0f}s)")
    if "photos" in only:
        _index_photos(c, photos, site_names)
        print(f"photos: {len(photos)} points ({time.time() - t0:.0f}s)")
    if "pages" in only:
        _index_pages(c, pages, t0)
    (INDEX / "manifest.json").write_text(json.dumps(dict(
        built=time.strftime("%Y-%m-%d %H:%M"), asr_prompt=use_prompt, pages=len(pages), text=len(texts),
        photos=len(photos), models=dict(page=E.PAGE_MODEL, photo=E.PHOTO_MODEL, text=E.TEXT_MODEL)), indent=1))
    print(f"done in {time.time() - t0:.0f}s")


def _index_text(c, texts):
    from qdrant_client import models as qm
    dense = E.encode_texts([x["embed_text"] for x in texts])
    avgdl = E.avg_len([x["embed_text"] for x in texts])
    c.create_collection("text", vectors_config={"dense": qm.VectorParams(size=dense.shape[1], distance=qm.Distance.COSINE)},
                        sparse_vectors_config={"bm25": qm.SparseVectorParams(modifier=qm.Modifier.IDF)})
    pts = []
    for i, (x, v) in enumerate(zip(texts, dense)):
        idx, val = E.bm25_doc(x["embed_text"], avgdl)
        pts.append(qm.PointStruct(id=i, vector={"dense": v.tolist(), "bm25": qm.SparseVector(indices=idx, values=val)},
                                  payload={k: v2 for k, v2 in x.items() if k != "embed_text"}))
    c.upsert("text", pts)


def _index_photos(c, photos, site_names):
    from qdrant_client import models as qm
    imgs = [Image.open(GENERATED / "photos" / p["file"]).convert("RGB") for p in photos]
    pv = E.encode_photos(imgs)
    c.create_collection("photos", vectors_config={"siglip": qm.VectorParams(size=pv.shape[1], distance=qm.Distance.COSINE)})
    c.upsert("photos", [qm.PointStruct(id=i, vector={"siglip": v.tolist()},
                                       payload=dict(modality="photo", site=site_names[p["site_id"]], **p))
                        for i, (p, v) in enumerate(zip(photos, pv))])


def _index_pages(c, pages, t0):
    from qdrant_client import models as qm
    c.create_collection("pages", vectors_config={"colsmol": qm.VectorParams(
        size=128, distance=qm.Distance.DOT, multivector_config=qm.MultiVectorConfig(
            comparator=qm.MultiVectorComparator.MAX_SIM))})
    batch = 8
    for i in range(0, len(pages), batch):
        part = pages[i:i + batch]
        embs = E.encode_pages([Image.open(PAGES_DIR / p["image"]).convert("RGB") for p in part])
        c.upsert("pages", [qm.PointStruct(id=i + j, vector={"colsmol": e.astype(np.float32).tolist()}, payload=p)
                           for j, (p, e) in enumerate(zip(part, embs))])
        print(f"  pages {i + len(part)}/{len(pages)} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-asr-prompt", action="store_true", help="transcribe without the domain vocabulary prompt")
    ap.add_argument("--only", default=None, help="rebuild only these collections, e.g. text,photos")
    a = ap.parse_args()
    build(use_prompt=not a.no_asr_prompt, only=set(a.only.split(",")) if a.only else None)
