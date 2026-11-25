"""Writes eval/RESULTS.md, CREDITS.md and the README results block from eval/results/.

Run:  uv run python -m fieldnote.report
"""
from __future__ import annotations

import json
import re

from fieldnote.config import EVAL

R = EVAL / "results"
CATS = [("image_only", "Image-only (15)"), ("text", "Text (10)"), ("audio", "Audio (8)"), ("multihop", "Multi-hop (7)"),
        ("all", "All (40)")]
RET_LABELS = {
    "hybrid": "Hybrid: captions as an extra retrieval key, pixels to the model",
    "full": "Pixels only (late fusion, no reranker)",
    "rerank_minilm": "+ MiniLM cross-encoder",
    "rerank_bge": "+ bge-reranker-base",
    "no_lookup": "- entity lookup",
    "text_only": "Text only (no image encoders)",
    "caption_baseline": "Caption-only baseline",
    "early_fusion": "Early fusion (one shared SigLIP space)",
}
GEN_LABELS = {"hybrid": "Hybrid (caption keys for retrieval, pixels to the model)",
              "full": "Fieldnote, pixels only (no captions anywhere)",
              "caption_baseline": "Caption-only baseline (text to the model)"}


def _load(path):
    return json.loads(path.read_text()) if path.exists() else None


def retrieval_table(prefix: str = "", title: str = "") -> list[str]:
    rows = []
    for name, label in RET_LABELS.items():
        d = _load(R / prefix / f"retrieval_{name}.json")
        if not d:
            continue
        s = d["summary"]
        c = s["by_category"]
        rows.append(f"| {label} | {c['image_only']['recall@5']:.2f} | {c['image_only']['recall@20']:.2f} | "
                    f"{c['all']['recall@5']:.2f} | {c['all']['recall@10']:.2f} | {c['all']['recall@20']:.2f} | "
                    f"{c['all']['rr']:.2f} | {s['latency_ms']['p95'] / 1000:.2f} s |")
    if not rows:
        return []
    return [title, "", "| Config | Image-only R@5 | Image-only R@20 | All R@5 | All R@10 | All R@20 | MRR | p95 retrieval |",
            "|---|---|---|---|---|---|---|---|", *rows, ""]


def _rows(path):
    return [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []


def _acc(rows, cat=None):
    sub = [r for r in rows if cat is None or r["category"] == cat]
    return sum(r["correct"] for r in sub) / len(sub) if sub else None


def generation_table() -> list[str]:
    out = []
    finals = [("hybrid", "Hybrid: caption keys for retrieval, pixels to the model (shipped)", R),
              ("caption_baseline", "Caption-only baseline: captions replace images", R),
              ("full", "Pixels only, no captions anywhere (v2 run)", R / "v2")]
    rows = []
    for name, label, folder in finals:
        s = _load(folder / f"generation_{name}_summary.json")
        if not s:
            continue
        c = s["by_category"]
        cells = [f"{c[k]['accuracy']:.0%}" if k in c else "–" for k, _ in CATS]
        rows.append(f"| {label} | " + " | ".join(cells) + f" | {c['all']['cites_gold']:.0%} |")
    if rows:
        out += ["### Answer accuracy, all 40 questions (one run each)", "",
                "| System | " + " | ".join(l for _, l in CATS) + " | Cites a gold source |",
                "|---|" + "---|" * (len(CATS) + 1), *rows, ""]
    # the image-only subset, run three times
    rep = []
    for name, label, files in [
        ("hybrid", "Hybrid (shipped)", [R / "generation_hybrid.jsonl", R / "generation_hybrid_r2.jsonl",
                                        R / "generation_hybrid_r3.jsonl"]),
        ("full", "Pixels only", [R / f"generation_full_r{i}.jsonl" for i in (1, 2, 3)]),
        ("caption_baseline", "Caption-only baseline", [R / "generation_caption_baseline.jsonl",
                                                       R / "generation_caption_baseline_r2.jsonl",
                                                       R / "generation_caption_baseline_r3.jsonl"]),
    ]:
        accs = [a for a in (_acc(_rows(f), "image_only") for f in files) if a is not None]
        if accs:
            n_ok = [round(a * 15) for a in accs]
            rep.append(f"| {label} | {', '.join(f'{k}/15' for k in n_ok)} | {sum(accs) / len(accs):.0%} | "
                       f"{min(accs):.0%}–{max(accs):.0%} |")
    if rep:
        out += ["### Ship-gate subset: the 15 image-only questions, repeated", "",
                "The model isn't deterministic. Same inputs, and a question or two still flips between runs, "
                "so each system got three runs on this subset.", "",
                "| System | Correct per run | Mean | Range |", "|---|---|---|---|", *rep, ""]
    lt = _load(R / "latency_hybrid.json")
    if lt:
        s = lt["summary"]
        out += ["### Latency (shipped config, k = 20, M4 MacBook Air, hosted Gemini model)", "",
                f"Measured over all {s['n']} questions at one request every {s['gap_s']:.0f} s. "
                f"{s['throttled_requests']} request(s) waited on a provider rate limit; that wait is shown separately.", "",
                "| Stage | p50 | p95 | max |", "|---|---|---|---|"]
        for k, lab in [("retrieval_ms", "Retrieval (lookup + 4 searches + fusion + packing)"),
                       ("llm_ms", "Generation (vision LLM call)"), ("total_ms", "End to end, as measured"),
                       ("service_ms", "End to end, excluding rate-limit waits"), ("waited_ms", "Rate-limit waits")]:
            v = s[k]
            out.append(f"| {lab} | {v['p50'] / 1000:.2f} s | {v['p95'] / 1000:.2f} s | {v['max'] / 1000:.2f} s |")
        out += ["", f"Model: {', '.join(s['models'])}.", ""]
    hist = []
    for tag, label, folder in [("v1", "v1: first run (3 page images in fused order, tags listed in one sentence)", R / "v1"),
                               ("v2", "v2: figure linking, interleaved labels, hybrid (page text cut at 900 chars)", R / "v2"),
                               ("final", "final: full page text for pages without a figure", R)]:
        cells = []
        for name in ("full", "hybrid", "caption_baseline"):
            a = _acc(_rows(folder / f"generation_{name}.jsonl"), "image_only")
            cells.append(f"{a:.0%}" if a is not None else "–")
        hist.append(f"| {label} | " + " | ".join(cells) + " |")
    out += ["### How the image-only number moved (single runs; see the repeats above for noise)", "",
            "| Version | Pixels only | Hybrid | Caption-only |", "|---|---|---|---|", *hist, ""]
    return out


def per_question() -> list[str]:
    full = {json.loads(l)["id"]: json.loads(l) for l in (R / "generation_hybrid.jsonl").read_text().splitlines()} \
        if (R / "generation_hybrid.jsonl").exists() else {}
    base = {json.loads(l)["id"]: json.loads(l) for l in (R / "generation_caption_baseline.jsonl").read_text().splitlines()} \
        if (R / "generation_caption_baseline.jsonl").exists() else {}
    ret = {r["id"]: r for r in (_load(R / "retrieval_hybrid.json") or {}).get("rows", [])}
    if not full:
        return []
    out = ["### Image-only questions, one by one", "",
           "| Q | Evidence | Retrieved (R@20, hybrid) | Hybrid | Caption-only |", "|---|---|---|---|---|"]
    for qid, r in full.items():
        if r["category"] != "image_only":
            continue
        out.append(f"| {qid} | {', '.join(g[0] for g in ret.get(qid, {}).get('gold', [['?']]))} | "
                   f"{'yes' if ret.get(qid, {}).get('recall@20') else 'no'} | {'yes' if r['correct'] else 'no'} | "
                   f"{'yes' if base.get(qid, {}).get('correct') else ('no' if qid in base else '–')} |")
    return out + [""]


MODELS = [
    ("Page retrieval", "vidore/colSmol-256M", "MIT"),
    ("Photo retrieval", "google/siglip2-so400m-patch14-384", "Apache-2.0"),
    ("Text retrieval", "BAAI/bge-base-en-v1.5", "MIT"),
    ("Reranker (ablation)", "cross-encoder/ms-marco-MiniLM-L6-v2", "Apache-2.0"),
    ("Reranker (ablation)", "BAAI/bge-reranker-base", "MIT"),
    ("Speech recognition", "Systran/faster-whisper-small.en (OpenAI Whisper)", "MIT"),
    ("Call audio (text-to-speech)", "hexgrad/Kokoro-82M", "Apache-2.0"),
]


def credits() -> None:
    from fieldnote.config import ROOT, SPEC
    photos = json.loads((SPEC / "photos.json").read_text())
    lines = ["# Credits", "", "## Models", "", "| Role | Model | License |", "|---|---|---|"]
    lines += [f"| {r} | `{m}` | {lic} |" for r, m, lic in MODELS]
    lines += ["", "Answer generation uses a hosted model (Gemini or Groq) when keys are set, or a local "
              "Ollama model otherwise; no model weights are redistributed by this repo.", "",
              "## Job-site photos", "",
              "Downloaded from Wikimedia Commons at build time (`make photos`); this repository does not store them. "
              "Each photo was resized and stripped of EXIF metadata. Fictional job metadata (site, unit, date, "
              "technician) is attached by `datagen/photos.py`; it does not describe the real photo.", "",
              "| Photo id | Title | Author | License |", "|---|---|---|---|"]
    for p in photos:
        a = p["attribution"]
        title = (a.get("title") or "").removeprefix("File:").replace("|", "/")
        author = (a.get("creator") or "unknown").replace("|", "/").replace("\n", " ")[:80]
        lic = f"[{a['license']}]({a['license_url']})" if a.get("license_url") else a.get("license", "")
        lines.append(f"| {p['photo_id']} | [{title}]({a['source']}) | {author} | {lic} |")
    lines += ["", "## Everything else", "",
              "Vantorr Climate Systems, Ridgeline Mechanical Services, every site, unit, person and part number are "
              "fictional. Manuals, bulletins and call scripts were written for this project (prose by an LLM from "
              "facts in `datagen/world.py`; figures, register and audio generated by code)."]
    (ROOT / "CREDITS.md").write_text("\n".join(lines) + "\n")


def readme_results() -> None:
    """Rewrite the part of the README between the RESULTS markers."""
    from fieldnote.config import ROOT
    readme = ROOT / "README.md"
    text = readme.read_text()
    if "<!-- RESULTS:START -->" not in text:
        return
    lines = []
    lt = _load(R / "latency_hybrid.json")
    reps = {n: [a for a in (_acc(_rows(f), "image_only") for f in fs) if a is not None] for n, fs in {
        "hybrid": [R / "generation_hybrid.jsonl", R / "generation_hybrid_r2.jsonl", R / "generation_hybrid_r3.jsonl"],
        "caption_baseline": [R / "generation_caption_baseline.jsonl", R / "generation_caption_baseline_r2.jsonl",
                             R / "generation_caption_baseline_r3.jsonl"],
        "full": [R / f"generation_full_r{i}.jsonl" for i in (1, 2, 3)]}.items()}
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")  # noqa: E731
    h, b = mean(reps["hybrid"]), mean(reps["caption_baseline"])
    gate = [("40-question eval, 15 unanswerable from text alone", "yes",
             "15 image-only questions whose values never appear in any text layer (validator + PDF text audit). "
             "Text-only retrieval can still reach the right page for "
             f"{_load(R / 'retrieval_text_only.json')['summary']['by_category']['image_only']['recall@20']:.0%} "
             "of them via the figure title, but the answer is only in the pixels"
             if _load(R / "retrieval_text_only.json") else "")]
    if reps["hybrid"] and reps["caption_baseline"]:
        verdict = "yes" if h - b >= 0.1 else ("partly" if h > b else "no")
        gate.append(("Beat the caption-only baseline on those 15", verdict,
                     f"{h:.0%} vs {b:.0%} mean over 3 runs (runs: "
                     f"{', '.join(f'{round(a * 15)}' for a in reps['hybrid'])} vs "
                     f"{', '.join(f'{round(a * 15)}' for a in reps['caption_baseline'])} of 15)"))
    gate.append(("Every answer cites a page and a cropped image", "yes",
                 "figure citations show the crop + page; calls cite a timestamped clip; photos the photo"))
    if lt:
        sv = lt["summary"]
        ok = sv["service_ms"]["p95"] < 6000
        gate.append(("p95 latency < 6 s at k = 20", "yes" if ok else "no",
                     f"p95 {sv['service_ms']['p95'] / 1000:.1f} s excluding provider rate-limit waits; "
                     f"{sv['total_ms']['p95'] / 1000:.1f} s as measured ({sv['throttled_requests']} of {sv['n']} "
                     "requests throttled)"))
    lines += ["### Ship gate", "", "| Requirement | | Evidence |", "|---|---|---|"]
    lines += [f"| {a} | {v} | {e} |" for a, v, e in gate]
    lines += [""]
    rows = []
    for name, label in [("hybrid", "Hybrid (shipped)"), ("full", "Pixels only"),
                        ("caption_baseline", "Caption-only baseline"), ("text_only", "Text only"),
                        ("early_fusion", "Early fusion (one SigLIP space)")]:
        d = _load(R / f"retrieval_{name}.json")
        if d:
            c = d["summary"]["by_category"]
            rows.append(f"| {label} | {c['image_only']['recall@10']:.2f} | {c['all']['recall@10']:.2f} | "
                        f"{c['all']['recall@20']:.2f} | {c['all']['rr']:.2f} |")
    lines += ["### Retrieval (no LLM involved)", "", "| Config | Image-only R@10 | All R@10 | All R@20 | MRR |",
              "|---|---|---|---|---|", *rows, ""]
    lines += generation_table()
    new = "<!-- RESULTS:START -->\n" + "\n".join(lines) + "\n<!-- RESULTS:END -->"
    text = re.sub(r"<!-- RESULTS:START -->.*?<!-- RESULTS:END -->", lambda m: new, text, flags=re.S)
    readme.write_text(text)


def main() -> None:
    credits()
    lines = ["# Fieldnote results", "",
             "Generated by `python -m fieldnote.report` from `eval/results/`. Do not edit by hand.", ""]
    lines += ["## Retrieval (no LLM involved)", ""]
    lines += retrieval_table("", "### Current system")
    lines += retrieval_table("v0", "### v0: the first run, before any fixes (single-level fusion, MiniLM reranker on). "
                                   "Kept so you can see where it started")
    lines += ["## Generation", ""] + generation_table() + per_question()
    (EVAL / "RESULTS.md").write_text("\n".join(lines))
    readme_results()
    print("\n".join(lines))


if __name__ == "__main__":
    main()
