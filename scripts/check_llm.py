"""Check that each configured LLM provider works and can actually read a chart.

Sends the VRT-060 charging chart through the same code the app uses and asks for the liquid
pressure at 95 F outdoor / 130 psig suction. The true value comes from world.json.

Run:  uv run python scripts/check_llm.py
"""
from __future__ import annotations

import json
import os
import re
import sys

from PIL import Image

from fieldnote import llm
from fieldnote.config import FIGURES, SPEC

QUESTION = ("This is an HVAC charging chart. Read the 95°F line at a suction pressure of 130 psig. "
            "What liquid pressure (psig) does the chart show? Reply with just the number.")


def main() -> int:
    cc = json.loads((SPEC / "world.json").read_text())["models"]["VRT-060"]["figure_facts"]["charging_chart"]
    gold = cc["L0"] + cc["kS"] * (130 - 125)
    img = Image.open(FIGURES / "VRT-060-CC.jpg")
    print(f"ground truth: {gold:.1f} psig (±8 counts as a correct chart read)\n")
    ok_any = False
    for name, (env, fn) in llm.PROVIDERS.items():
        if env and not os.getenv(env):
            print(f"{name:7s} SKIP  {env} not set")
            continue
        try:
            os.environ["FIELDNOTE_LLM"] = name
            res = llm.generate("You read engineering charts precisely.", QUESTION, [img], retries=1)
        except Exception as e:  # noqa: BLE001
            print(f"{name:7s} FAIL  {str(e).splitlines()[-1][:220]}")
            continue
        m = re.search(r"\d{2,4}(?:\.\d+)?", res.text.replace(",", ""))
        val = float(m.group()) if m else None
        verdict = "chart read OK" if val is not None and abs(val - gold) <= 8 else "WORKS, but misread the chart"
        print(f"{name:7s} OK    {res.model}  {res.latency_ms / 1000:.1f}s  answered {res.text[:30]!r} -> {verdict}")
        ok_any = True
    return 0 if ok_any else 1


if __name__ == "__main__":
    sys.exit(main())
