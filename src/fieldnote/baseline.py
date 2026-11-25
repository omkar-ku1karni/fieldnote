"""Caption-only baseline: turn every image into text up front and never look at pixels again.

Each figure crop and job photo is captioned once by the same vision model the app uses. The
captions are indexed next to the usual text chunks and call windows, and answers are generated
from text only. Everything else stays the same, so the comparison is just pixels vs captions.

Captions are committed in eval/captions.json, so nobody has to re-run the API calls.

Run:  uv run python -m fieldnote.baseline captions   # caption figures + photos (calls the LLM)
      uv run python -m fieldnote.baseline index      # build the text_caption collection
"""
from __future__ import annotations

import json
import time

from PIL import Image

from fieldnote import encoders as E
from fieldnote import llm
from fieldnote.config import EVAL, GENERATED, SPEC
from fieldnote.ingest import client

CAPTIONS = EVAL / "captions.json"
CAPTION_PROMPT = ("Describe this image in detail for a search index used by HVAC technicians. Include what it "
                  "shows, all visible text and labels, and any numbers, values or readings you can see.")


def _targets() -> list[dict]:
    c = client()
    out, offset = [], None
    while True:
        pts, offset = c.scroll("pages", limit=256, offset=offset, with_payload=True, with_vectors=False)
        for p in pts:
            for f in p.payload["figures"]:
                out.append(dict(key=f"crop:{f['crop']}", image=f"crops/{f['crop']}", doc_id=p.payload["doc_id"],
                                page=p.payload["page"], title=p.payload["title"], kind="figure"))
        if offset is None:
            break
    for ph in json.loads((SPEC / "photos.json").read_text()):
        out.append(dict(key=f"photo:{ph['photo_id']}", image=f"photos/{ph['file']}", photo=ph, kind="photo"))
    return out


def caption_all(providers: list[str] | None = None) -> None:
    """Caption everything that isn't cached yet. Saves after each image, so it's safe to Ctrl-C."""
    cache = json.loads(CAPTIONS.read_text()) if CAPTIONS.exists() else {}
    todo = [t for t in _targets() if t["key"] not in cache]
    print(f"{len(cache)} cached, {len(todo)} to caption, providers: {llm.available(providers)}")
    for i, t in enumerate(todo):
        try:
            res = llm.generate("You write precise, factual image descriptions.", CAPTION_PROMPT,
                               [Image.open(GENERATED / t["image"])], providers=providers)
        except llm.LLMUnavailable as e:
            print(f"stopping at {t['key']}, every provider failed. Run it again later to resume.\n{e}")
            break
        cache[t["key"]] = dict(caption=res.text, provider=res.provider, model=res.model)
        CAPTIONS.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
        print(f"  {i + 1}/{len(todo)} {t['key']} ({res.model}, {res.latency_ms / 1000:.1f}s)", flush=True)
        if res.provider != "ollama":
            time.sleep(4)  # stay under the provider's requests-per-minute limit
    from collections import Counter
    print("captioned by:", dict(Counter(v["model"] for v in cache.values())))


def build_index() -> None:
    from qdrant_client import models as qm
    caps = json.loads(CAPTIONS.read_text())
    c = client()
    # start from the same points as the normal text collection
    base, offset = [], None
    while True:
        pts, offset = c.scroll("text", limit=512, offset=offset, with_payload=True, with_vectors=False)
        base += [p.payload for p in pts]
        if offset is None:
            break
    # and add one text point per caption in place of the image
    world = json.loads((SPEC / "world.json").read_text())
    site_names = {s["id"]: s["name"] for s in world["sites"]}
    for t in _targets():
        cap = caps.get(t["key"])
        if not cap:
            continue
        if t["kind"] == "figure":
            base.append(dict(modality="doc_text", doc_id=t["doc_id"], kind="caption", title=t["title"], page=t["page"],
                             chunk=f"cap-{t['key']}", text=f"[Figure caption] {cap['caption']}"))
        else:
            ph = t["photo"]
            base.append(dict(modality="photo_caption", photo_id=ph["photo_id"], site_id=ph["site_id"],
                             site=site_names[ph["site_id"]], unit=ph["unit"], job=ph["job"], date=ph["date"],
                             tech=ph["tech"], file=ph["file"],
                             text=f"[Job photo {ph['job']}, {site_names[ph['site_id']]} {ph['unit']}, {ph['date']}] "
                                  f"{cap['caption']}"))
    embed = [f"{x.get('title', '')}\n{x['text']}" for x in base]
    dense = E.encode_texts(embed)
    avgdl = E.avg_len(embed)
    if c.collection_exists("text_caption"):
        c.delete_collection("text_caption")
    c.create_collection("text_caption",
                        vectors_config={"dense": qm.VectorParams(size=dense.shape[1], distance=qm.Distance.COSINE)},
                        sparse_vectors_config={"bm25": qm.SparseVectorParams(modifier=qm.Modifier.IDF)})
    pts = []
    for i, (x, e, v) in enumerate(zip(base, embed, dense)):
        idx, val = E.bm25_doc(e, avgdl)
        pts.append(qm.PointStruct(id=i, vector={"dense": v.tolist(), "bm25": qm.SparseVector(indices=idx, values=val)},
                                  payload=x))
    c.upsert("text_caption", pts)
    print(f"text_caption: {len(pts)} points ({sum(1 for x in base if 'caption' in str(x.get('kind', '')) or x['modality'] == 'photo_caption')} captions)")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["captions", "index"])
    ap.add_argument("--providers", default=None, help="e.g. ollama  or  groq,ollama  (default gemini,groq,ollama)")
    a = ap.parse_args()
    if a.what == "captions":
        caption_all(a.providers.split(",") if a.providers else None)
    else:
        build_index()
