"""Build the evidence pack, ask the vision model, and pull the citations back out.

Figure crops and photos are sent as images; text chunks, call transcripts and register rows
as text. Each item gets a tag ([S1], [S2], ...) and the model has to cite them, so every claim
in the answer points at a page, a call timestamp or a photo the tech can check.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from functools import lru_cache

from PIL import Image

from fieldnote import llm
from fieldnote.config import GENERATED
from fieldnote.retrieve import Config, Hit, retrieve

TRANSCRIPTS = GENERATED / "transcripts" / "vocab"

SYSTEM = """You are Fieldnote, an assistant for commercial HVAC field technicians.
Answer ONLY from the evidence provided. Evidence items are tagged [S1], [S2], ...; each image is
preceded by its own [S#] label.

Rules:
- Start with ONE short sentence that gives the direct answer (the number, part, setting or cause).
  Then add short supporting detail or numbered steps if useful. Techs read this on a phone on a roof.
- Plain text and simple Markdown only (bold, lists). Never use LaTeX or $...$; write units as 5 µF, 630 psig.
- Cite every factual claim with its tag(s), e.g. "opens at 630 psig [S2]".
- When a value comes from a chart or diagram image, read it carefully from the image and say
  which line/row/column you read. Never guess a value that is not in the evidence.
- Equipment register rows tell you which model a site/unit tag is.
- If the evidence does not contain the answer, say so plainly and say what to check instead."""

MAX_TEXT, MAX_PAGES, MAX_PHOTOS, MAX_CALLS = 6, 4, 3, 3


@dataclass
class Source:
    tag: str
    modality: str
    label: str
    doc_id: str | None = None
    page: int | None = None
    image: str | None = None         # file under data/generated/{pages,crops,photos}
    page_image: str | None = None    # full page, for "open the whole page"
    attribution: dict | None = None  # photo license / author
    figure: bool = False             # True when we show a figure crop rather than page text
    call_id: str | None = None
    start: float | None = None
    end: float | None = None
    photo_id: str | None = None
    text: str | None = None


@dataclass
class Answer:
    question: str
    text: str
    sources: list[Source]
    cited: list[str]
    provider: str
    model: str
    timings: dict = field(default_factory=dict)


def _fmt_ts(s: float) -> str:
    return f"{int(s // 60)}:{int(s % 60):02d}"


@lru_cache(maxsize=64)
def _segments(call_id: str) -> tuple:
    path = TRANSCRIPTS / f"{call_id}.json"
    return tuple(json.loads(path.read_text())) if path.exists() else ()


def _transcript(call_id: str) -> str:
    return " ".join(f"[{_fmt_ts(s['start'])}] {s['text']}" for s in _segments(call_id))


def _ground_call(src: Source, answer_text: str) -> None:
    """Point the audio clip at the transcript segment that best matches what the answer says."""
    segs = _segments(src.call_id)
    if not segs:
        return
    words = lambda t: {w for w in re.findall(r"[a-z0-9]+", t.lower()) if len(w) > 2}  # noqa: E731
    # only the sentences that cite this call say what we took from it
    citing = [x for x in re.split(r"(?<=[.!?])\s+|\n", answer_text) if re.search(rf"\b{src.tag}\b", x)]
    ans = words(" ".join(citing) or answer_text)
    best = max(range(len(segs)), key=lambda i: len(words(segs[i]["text"]) & ans))
    lo, hi = max(0, best - 1), min(len(segs) - 1, best + 1)
    src.start, src.end = segs[lo]["start"], segs[hi]["end"]
    src.label = f"{src.label} at {_fmt_ts(src.start)}"


@lru_cache(maxsize=1)
def _pages_by_key() -> dict:
    """(doc_id, page) -> page payload, so a text hit can pull in the figure on the same page."""
    from fieldnote.retrieve import _client
    out, offset = {}, None
    while True:
        pts, offset = _client().scroll("pages", limit=256, offset=offset, with_payload=True, with_vectors=False)
        for p in pts:
            out[(p.payload["doc_id"], p.payload["page"])] = p.payload
        if offset is None:
            return out


def evidence_pack(hits: list[Hit], pixels: bool = True) -> tuple[list[Source], list[tuple[str, Image.Image]]]:
    """Turn ranked hits into tagged sources plus the images to send.

    pixels=True is the normal mode. Figures and photos go in as images, and a text chunk from a
    page with a figure brings that figure along. Pages with no figure just send their text.
    pixels=False is the caption-only baseline: everything is text and captions replace images.
    """
    sources: list[Source] = []
    images: list[tuple[str, Image.Image]] = []
    seen_pages, seen_calls, seen_photos, seen_text = set(), set(), set(), set()
    counts = dict(text=0, page=0, photo=0, call=0)
    pages = _pages_by_key() if pixels else {}

    def tag():
        return f"S{len(sources) + 1}"

    def add_figure(doc_id, page_no) -> bool:
        pg = pages.get((doc_id, page_no))
        key = (doc_id, page_no)
        if not pg or not pg["figures"] or key in seen_pages or counts["page"] >= MAX_PAGES:
            return False
        seen_pages.add(key)
        counts["page"] += 1
        crop = pg["figures"][0]["crop"]
        src = Source(tag(), "page", f"{doc_id} p.{page_no}", doc_id, page_no, image=f"crops/{crop}",
                     text=pg["text"][:400], page_image=f"pages/{pg['image']}", figure=True)
        sources.append(src)
        images.append((src.tag, Image.open(GENERATED / src.image)))
        return True

    def add_photo(p) -> None:
        if p["photo_id"] in seen_photos or counts["photo"] >= MAX_PHOTOS:
            return
        seen_photos.add(p["photo_id"])
        counts["photo"] += 1
        src = Source(tag(), "photo", f"Job photo {p['job']} — {p['site']} {p['unit']}, {p['date']} ({p['tech']})",
                     photo_id=p["photo_id"], image=f"photos/{p['file']}", attribution=p.get("attribution"))
        sources.append(src)
        images.append((src.tag, Image.open(GENERATED / src.image)))

    def add_text(doc_id, page_no, text, label=None) -> None:
        key = (doc_id, page_no, text[:60])
        if key in seen_text or counts["text"] >= MAX_TEXT:
            return
        seen_text.add(key)
        counts["text"] += 1
        sources.append(Source(tag(), "text", label or f"{doc_id} p.{page_no}", doc_id, page_no, text=text))

    for h in hits:
        p = h.payload
        if h.modality == "register":
            rows = "; ".join(f"{a['unit']} = {a['model']}, serial {a['serial']}, firmware {a['controller_firmware']}"
                             for a in p["assets"])
            sources.append(Source(tag(), "register", f"Equipment register p.{p['page']}", "RMS-REGISTER", p["page"],
                                  text=rows or None))
        elif h.modality == "page":
            if not (pixels and add_figure(p["doc_id"], p["page"])):
                add_text(p["doc_id"], p["page"], p["text"][:3000])  # whole page; bulletins list parts at the end
        elif h.modality == "doc_text":
            is_caption = str(p.get("chunk", "")).startswith("cap-")
            if pixels:
                add_figure(p["doc_id"], p["page"])
                if not is_caption:  # a caption is dropped: the figure itself is the evidence
                    add_text(p["doc_id"], p["page"], p["text"])
            else:
                add_text(p["doc_id"], p["page"], p["text"],
                         f"{p['doc_id']} p.{p['page']}" + (" [figure caption]" if is_caption else ""))
        elif h.modality == "call" and counts["call"] < MAX_CALLS and p["call_id"] not in seen_calls:
            # Calls are only ~500 words, so send the whole timestamped transcript. The useful part is
            # often a minute after the 40 s window that matched.
            seen_calls.add(p["call_id"])
            counts["call"] += 1
            sources.append(Source(tag(), "call", f"Support call {p['call_id']} ({p['date']}), {p['site']} {p['unit']}",
                                  call_id=p["call_id"], start=p["start"], end=p["end"],
                                  text=_transcript(p["call_id"]) or p["text"]))
        elif h.modality == "photo_caption":
            if pixels:
                add_photo(p)  # the caption found it, but the model gets the actual photo
            elif counts["photo"] < MAX_PHOTOS and p["photo_id"] not in seen_photos:
                seen_photos.add(p["photo_id"])
                counts["photo"] += 1
                sources.append(Source(tag(), "photo_caption", f"Job photo {p['job']} — {p['site']} {p['unit']}, "
                                      f"{p['date']} ({p['tech']}) [caption only]", photo_id=p["photo_id"], text=p["text"]))
        elif h.modality == "photo":
            add_photo(p)
    return sources, images


def build_prompt(question: str, sources: list[Source]) -> str:
    lines = [f"Question from a field technician: {question}", "", "Text evidence:"]
    for s in sources:
        if s.modality not in ("page", "photo"):
            lines.append(f"[{s.tag}] {s.label}: {s.text}")
    if any(s.modality in ("page", "photo") for s in sources):
        lines.append("\nImage evidence follows. Each image comes right after its own [S#] label; look at each "
                     "image carefully before answering (count markers, read axes and table cells exactly).")
    return "\n".join(lines)


def image_label(s: Source) -> str:
    kind = "Manual figure" if s.modality == "page" else "Job photo"
    return f"[{s.tag}] {kind} — {s.label}"


def answer(question: str, cfg: Config | None = None) -> Answer:
    cfg = cfg or Config()
    t0 = time.perf_counter()
    hits, info = retrieve(question, cfg)
    pixels = cfg.use_pages or cfg.use_photos
    sources, images = evidence_pack(hits, pixels=pixels)
    by_tag = {s.tag: s for s in sources}
    res = llm.generate(SYSTEM, build_prompt(question, sources), [im for _, im in images],
                       labels=[image_label(by_tag[t]) for t, _ in images])
    tags = [t for grp in re.findall(r"\[([^\]]*?S\d+[^\]]*)\]", res.text) for t in re.findall(r"S\d+", grp)]
    cited = sorted(set(tags), key=lambda t: int(t[1:]))
    for s in sources:
        if s.modality == "call" and s.tag in cited:
            _ground_call(s, res.text)
    timings = dict(info["timings"], llm_ms=res.latency_ms, llm_waited_ms=res.waited_ms,
                   total_ms=(time.perf_counter() - t0) * 1000)
    return Answer(question, res.text, sources, cited, res.provider, res.model, timings)


if __name__ == "__main__":
    import sys
    a = answer(" ".join(sys.argv[1:]) or "Lakeshore Medical RTU-7 keeps tripping on high pressure. Why?")
    print(a.text, "\n")
    for s in a.sources:
        print(("*" if s.tag in a.cited else " "), s.tag, s.label, s.image or "")
    print(json.dumps(a.timings, indent=1), a.provider, a.model)
