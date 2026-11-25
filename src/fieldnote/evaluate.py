"""Evals. Retrieval and generation are scored separately.

Gold evidence in eval/questions.yaml is turned into retrieval units:
  manual_figure  -> the page the figure ended up on (recorded by the PDF builder)
  manual_text    -> any page of that doc whose text contains the exact fact
  register       -> the register page with that unit's serial
  bulletin       -> any page of the bulletin
  call           -> call:Cxx
  photo          -> photo:P-...

Everything is reported per category, since an overall number hides how the image-only
questions do.

Run:  uv run python -m fieldnote.evaluate retrieval [--configs full,hybrid,...]
      uv run python -m fieldnote.evaluate generation [--configs hybrid] [--only image_only] [--tag _r2]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import time
from dataclasses import replace

import yaml

from fieldnote.config import EVAL, GENERATED
from fieldnote.retrieve import Config, retrieve

CONFIGS = {
    "full": Config(),
    "rerank_minilm": Config(rerank=True),
    "rerank_bge": Config(rerank=True, rerank_model="BAAI/bge-reranker-base"),
    "no_lookup": Config(entity_lookup=False),
    "text_only": Config(use_pages=False, use_photos=False),
    "caption_baseline": Config(use_pages=False, use_photos=False, text_collection="text_caption"),
    "hybrid": Config(text_collection="text_caption"),  # captions help find images, the model still sees pixels
    "early_fusion": Config(),  # not really used, run_retrieval sends this one to early_fusion.retrieve
}
KS = (5, 10, 20)
RESULTS = EVAL / "results"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("–", "-").replace("—", "-")).strip().lower()


def page_texts() -> dict[tuple[str, int], str]:
    from fieldnote.retrieve import _client
    out, offset = {}, None
    while True:
        pts, offset = _client().scroll("pages", limit=256, offset=offset, with_payload=True, with_vectors=False)
        for p in pts:
            out[(p.payload["doc_id"], p.payload["page"])] = _norm(p.payload["text"])
        if offset is None:
            return out


def gold_units(q: dict, pages: dict, fig_pages: dict, world: dict) -> list[set[str]]:
    """One set per evidence item. An item counts as found if any unit in its set is retrieved."""
    out = []
    for ev in q["evidence"]:
        m = ev["modality"]
        if m == "manual_figure":
            doc = ev["figure_id"].split("-")[0] + "-IOM"
            out.append({f"{doc}#p{fig_pages[doc][ev['figure_id']]['page']}"})
        elif m == "manual_text":
            needle = _norm(ev["find"])
            out.append({f"{d}#p{p}" for (d, p), t in pages.items() if d == ev["doc_id"] and needle in t})
        elif m == "bulletin":
            out.append({f"{d}#p{p}" for (d, p) in pages if d == ev["bulletin_id"]})
        elif m == "register":
            a = next(a for a in world["assets"] if a["site_id"] == ev["site_id"] and a["unit"] == ev["unit"])
            out.append({f"RMS-REGISTER#p{p}" for (d, p), t in pages.items()
                        if d == "RMS-REGISTER" and a["serial"].lower() in t})
        elif m == "call":
            out.append({f"call:{ev['call_id']}"})
        elif m == "photo":
            out.append({f"photo:{ev['photo_id']}"})
        if not out[-1]:
            raise ValueError(f"{q['id']}: could not resolve gold unit for {ev}")
    return out


def score(ranked_units: list[str], gold: list[set[str]]) -> dict:
    res = {}
    for k in KS:
        top = set(ranked_units[:k])
        hit = [bool(g & top) for g in gold]
        res[f"recall@{k}"] = sum(hit) / len(gold)
        res[f"hit@{k}"] = float(any(hit))
    first = next((i for i, u in enumerate(ranked_units) if any(u in g for g in gold)), None)
    res["rr"] = 0.0 if first is None else 1 / (first + 1)
    return res


def run_retrieval(config_names: list[str]) -> dict:
    world = json.loads((EVAL.parent / "data" / "spec" / "world.json").read_text())
    qs = yaml.safe_load((EVAL / "questions.yaml").read_text())
    pages = page_texts()
    fig_pages = {d["doc_id"]: d["figure_pages"] for d in json.loads((GENERATED / "docs.json").read_text())}
    golds = {q["id"]: gold_units(q, pages, fig_pages, world) for q in qs}
    retrieve("warm up the encoders", Config())  # so model loading isn't timed
    summary = {}
    RESULTS.mkdir(parents=True, exist_ok=True)
    for name in config_names:
        cfg = CONFIGS[name]
        rows = []
        for q in qs:
            t = time.perf_counter()
            if name == "early_fusion":
                from fieldnote.early_fusion import retrieve as ef_retrieve
                hits, info = ef_retrieve(q["question"], k=20)
            else:
                hits, info = retrieve(q["question"], replace(cfg, k=20))
            ms = (time.perf_counter() - t) * 1000
            units = list(dict.fromkeys(h.key for h in hits))
            rows.append(dict(id=q["id"], category=q["category"], latency_ms=round(ms), **score(units, golds[q["id"]]),
                             top5=units[:5], gold=[sorted(g) for g in golds[q["id"]]]))
        by_cat = {}
        for cat in ("image_only", "text", "audio", "multihop", "all"):
            sub = [r for r in rows if cat == "all" or r["category"] == cat]
            by_cat[cat] = {m: round(statistics.mean(r[m] for r in sub), 3)
                           for m in [f"recall@{k}" for k in KS] + ["rr"]} | dict(n=len(sub))
        lat = sorted(r["latency_ms"] for r in rows if not r.get("error")) or [0]
        summary[name] = dict(errors=sum(bool(r.get("error")) for r in rows), by_category=by_cat, latency_ms=dict(p50=lat[len(lat) // 2],
                                                                  p95=lat[min(len(lat) - 1, int(0.95 * len(lat)))]))
        (RESULTS / f"retrieval_{name}.json").write_text(json.dumps(dict(summary=summary[name], rows=rows), indent=1))
        print(f"\n== {name} ==  p50 {summary[name]['latency_ms']['p50']} ms  p95 {summary[name]['latency_ms']['p95']} ms")
        for cat, m in by_cat.items():
            print(f"  {cat:11s} n={m['n']:2d}  R@5 {m['recall@5']:.2f}  R@10 {m['recall@10']:.2f}  "
                  f"R@20 {m['recall@20']:.2f}  MRR {m['rr']:.2f}")
    return summary


# --- generation

NUM = re.compile(r"(?<![\w.])-?\d+(?:,\d{3})*(?:\.\d+)?")
JUDGE = """You grade an HVAC assistant's answer against a rubric. For each rubric point, decide if the
answer clearly states it (paraphrase is fine; numbers must match). Reply with JSON only:
{"points": [true/false, ...]} in rubric order."""


def _numbers(text: str) -> list[float]:
    return [float(x.replace(",", "")) for x in NUM.findall(text)]


def grade(q: dict, answer_text: str) -> dict:
    a, low = q["answer"], answer_text.lower()
    if a["type"] == "numeric":
        asked = set(_numbers(q["question"]))
        cands = [n for n in _numbers(answer_text) if n not in asked]
        ok = any(abs(n - a["value"]) <= a["tolerance"] + 1e-9 for n in cands)
        return dict(correct=ok, score=float(ok))
    if a["type"] == "keywords":
        groups = [any(alt.lower() in low for alt in g) for g in a["must_include"]]
        return dict(correct=all(groups), score=sum(groups) / len(groups))
    from fieldnote import llm
    prompt = (f"Question: {q['question']}\nReference answer: {a['canonical']}\nRubric points:\n"
              + "\n".join(f"{i + 1}. {pt}" for i, pt in enumerate(a["points"]))
              + f"\n\nAssistant answer:\n{answer_text}")
    res = llm.generate(JUDGE, prompt)
    m = re.search(r"\{.*\}", res.text, re.S)
    pts = json.loads(m.group())["points"] if m else []
    pts = (pts + [False] * len(a["points"]))[:len(a["points"])]
    return dict(correct=all(pts), score=sum(map(bool, pts)) / len(pts), judge=pts)


def run_generation(config_names: list[str], only: str | None = None, pause_s: float = 4.0, tag: str = "") -> dict:
    from fieldnote.answer import answer
    from fieldnote.llm import LLMUnavailable
    world = json.loads((EVAL.parent / "data" / "spec" / "world.json").read_text())
    qs = yaml.safe_load((EVAL / "questions.yaml").read_text())
    if only:
        qs = [q for q in qs if q["id"] in only.split(",") or q["category"] == only]
    pages = page_texts()
    fig_pages = {d["doc_id"]: d["figure_pages"] for d in json.loads((GENERATED / "docs.json").read_text())}
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name in config_names:
        cfg = CONFIGS[name]
        out_path = RESULTS / f"generation_{name}{tag}.jsonl"
        done = {json.loads(l)["id"]: json.loads(l) for l in out_path.read_text().splitlines()} if out_path.exists() else {}
        for q in qs:
            if q["id"] in done:
                continue
            gold = gold_units(q, pages, fig_pages, world)
            try:
                ans = answer(q["question"], replace(cfg, k=20))
            except LLMUnavailable as e:  # counts as wrong; keep the error so it shows up in the results
                row = dict(id=q["id"], category=q["category"], correct=False, score=0.0, cites_gold=False,
                           has_citation=False, answer="", error=str(e)[:400], provider="none", model="none",
                           latency_ms=0, retrieval_ms=0, sources=[])
                done[q["id"]] = row
                with out_path.open("a") as f:
                    f.write(json.dumps(row) + "\n")
                print(f"  [{name}] {q['id']} ERR  {str(e).splitlines()[0]}", flush=True)
                continue
            g = grade(q, ans.text)
            cited_units = set()
            for s in ans.sources:
                if s.tag in ans.cited:
                    if s.doc_id:
                        cited_units.add(f"{s.doc_id}#p{s.page}")
                    if s.call_id:
                        cited_units.add(f"call:{s.call_id}")
                    if s.photo_id:
                        cited_units.add(f"photo:{s.photo_id}")
            row = dict(id=q["id"], category=q["category"], **g, cites_gold=any(cited_units & u for u in gold),
                       has_citation=bool(ans.cited), answer=ans.text, provider=ans.provider, model=ans.model,
                       latency_ms=round(ans.timings["total_ms"]), retrieval_ms=round(ans.timings["total_ms"] - ans.timings["llm_ms"]),
                       sources=[dict(tag=s.tag, label=s.label, image=s.image) for s in ans.sources])
            done[q["id"]] = row
            with out_path.open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(f"  [{name}] {q['id']} {'OK ' if g['correct'] else 'NO '} {row['latency_ms']:>6} ms  {ans.text[:70]!r}",
                  flush=True)
            time.sleep(pause_s)
        rows = [done[q["id"]] for q in qs if q["id"] in done]
        by_cat = {}
        for cat in ("image_only", "text", "audio", "multihop", "all"):
            sub = [r for r in rows if cat == "all" or r["category"] == cat]
            if sub:
                by_cat[cat] = dict(n=len(sub), accuracy=round(statistics.mean(r["correct"] for r in sub), 3),
                                   partial=round(statistics.mean(r["score"] for r in sub), 3),
                                   cites_gold=round(statistics.mean(r["cites_gold"] for r in sub), 3))
        lat = sorted(r["latency_ms"] for r in rows if not r.get("error")) or [0]
        summary[name] = dict(errors=sum(bool(r.get("error")) for r in rows), by_category=by_cat, latency_ms=dict(
            p50=lat[len(lat) // 2], p95=lat[min(len(lat) - 1, int(0.95 * len(lat)))]),
            providers=sorted({f"{r['provider']}:{r['model']}" for r in rows if not r.get("error")}))
        (RESULTS / f"generation_{name}{tag}_summary.json").write_text(json.dumps(summary[name], indent=1))
        print(f"\n== {name} ==  p50 {summary[name]['latency_ms']['p50']} ms  p95 {summary[name]['latency_ms']['p95']} ms")
        for cat, m in by_cat.items():
            print(f"  {cat:11s} n={m['n']:2d}  accuracy {m['accuracy']:.2f}  partial {m['partial']:.2f}  "
                  f"cites gold {m['cites_gold']:.2f}")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["retrieval", "generation"])
    ap.add_argument("--configs", default=None)
    ap.add_argument("--only", default=None, help="comma-separated ids or a category")
    ap.add_argument("--tag", default="", help="suffix for result files, e.g. _r2 for a repeat run")
    a = ap.parse_args()
    if a.what == "retrieval":
        run_retrieval((a.configs or "full,rerank_minilm,rerank_bge,no_lookup,text_only,caption_baseline").split(","))
    else:
        run_generation((a.configs or "full,caption_baseline").split(","), a.only, tag=a.tag)
