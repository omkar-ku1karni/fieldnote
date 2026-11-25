"""Latency check for the p95 < 6 s target at k = 20.

Runs each eval question once with the shipped config, one question every 12 s by default so the
provider rate limits don't take over. Any time spent waiting on a rate limit is recorded and
reported on its own line.

Run:  uv run python scripts/latency.py [--config hybrid] [--gap 12]
"""
from __future__ import annotations

import argparse
import json
import statistics
import time

import yaml

from fieldnote.answer import answer
from fieldnote.config import EVAL
from fieldnote.evaluate import CONFIGS


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="hybrid")
    ap.add_argument("--gap", type=float, default=12.0)
    a = ap.parse_args()
    qs = yaml.safe_load((EVAL / "questions.yaml").read_text())
    answer("warm up", CONFIGS[a.config])
    rows = []
    for q in qs:
        t = time.perf_counter()
        ans = answer(q["question"], CONFIGS[a.config])
        tm = ans.timings
        rows.append(dict(id=q["id"], total_ms=tm["total_ms"], retrieval_ms=tm["total_ms"] - tm["llm_ms"],
                         llm_ms=tm["llm_ms"], waited_ms=tm.get("llm_waited_ms", 0), model=ans.model))
        print(f"{q['id']} total {tm['total_ms']:.0f} ms (llm {tm['llm_ms']:.0f}, waited {tm.get('llm_waited_ms', 0):.0f})",
              flush=True)
        time.sleep(max(0.0, a.gap - (time.perf_counter() - t)))
    out = {}
    for k in ("retrieval_ms", "llm_ms", "total_ms", "waited_ms"):
        v = [r[k] for r in rows]
        out[k] = dict(p50=round(pct(v, 50)), p95=round(pct(v, 95)), max=round(max(v)), mean=round(statistics.mean(v)))
    service = [r["total_ms"] - r["waited_ms"] for r in rows]
    out["service_ms"] = dict(p50=round(pct(service, 50)), p95=round(pct(service, 95)), max=round(max(service)))
    out["throttled_requests"] = sum(r["waited_ms"] > 50 for r in rows)
    out["config"], out["gap_s"], out["n"] = a.config, a.gap, len(rows)
    out["models"] = sorted({r["model"] for r in rows})
    (EVAL / "results" / f"latency_{a.config}.json").write_text(json.dumps(dict(summary=out, rows=rows), indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
