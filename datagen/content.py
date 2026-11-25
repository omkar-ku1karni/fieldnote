"""Split raw LLM answers into content files and validate them against the world spec.

Checks, per file type:
  manuals    title/doc_id, every figure placeholder exactly once, required facts verbatim,
             no figure-only values, no call/bulletin-only facts, no real brands
  bulletins  all three present, required facts verbatim
  calls      header fields, AGENT/TECH lines only, word count, no digits, must_say phrases verbatim

Run:  uv run python -m datagen.content      (exit code 1 if anything fails)
"""
from __future__ import annotations

import json
import re
import sys

from fieldnote.config import CONTENT, SPEC

RAW = CONTENT / "_raw"
FILE_MARK = re.compile(r"^<<<FILE:\s*(\S+)\s*>>>\s*$", re.M)

# Proper nouns, matched case-sensitively ("report damage to the carrier" is fine; "Carrier" is not).
BRANDS = ["Carrier", "Trane", "Lennox", "Daikin", "York", "Copeland", "Honeywell", "Emerson", "White-Rodgers",
          "Goodman", "Rheem", "Bryant", "Ruud", "Mitsubishi", "Danfoss", "Johnson Controls", "Amana"]
CALL_ONLY = ["VPN-0475", "VPN-4471", "VPN-5520", "VPN-3310", "VPN-2208", "VPN-1190", "VPN-6120", "VHS-35",
             "VLA-2", "VTX-2", "VCP-150T", "RDS-1", "firmware", "debounce", "E41", "JP7", "DIP",
             "hard start", "hard-start", "low ambient kit", "low-ambient kit", "2-10 V", "2–10 V", "0-10 V", "0–10 V",
             "set screw", "set-screw", "warranty"]
# number followed by a unit that only figures may carry
FIGURE_VALUE = re.compile(
    r"\b\d[\d,.]*\s*(psig|psi|cfm|kΩ|kohm|k-ohm|ohms?|Ω|oz\s*(per|/)\s*f(oo)?t|amps?\b|A\b(?=.*\b(MCA|MOP|fuse)))",
    re.I)
PERCENT_NEAR_ALT = re.compile(r"(altitude|elevation|derate)[^.\n]{0,80}\b\d+\s*%|\b\d+\s*%[^.\n]{0,80}(altitude|elevation|derate)", re.I)
WIRE_COLOR = re.compile(r"\b(violet|pink|brown|orange|gray|grey|yellow|blue|white|black|red)\s+(wire|lead|conductor)s?\b", re.I)


def norm(s: str) -> str:
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def split_raw() -> None:
    for name, sub in [("bulletins.md", "bulletins"), ("calls_part1.md", "calls"), ("calls_part2.md", "calls")]:
        p = RAW / name
        if not p.exists():
            continue
        text = p.read_text()
        parts = FILE_MARK.split(text)
        out = CONTENT / sub
        out.mkdir(parents=True, exist_ok=True)
        for fname, body in zip(parts[1::2], parts[2::2]):
            (out / fname).write_text(body.strip() + "\n")
    for p in RAW.glob("manual_*.md"):
        (CONTENT / "manuals").mkdir(parents=True, exist_ok=True)
        (CONTENT / "manuals" / f"{p.stem.split('_', 1)[1]}.md").write_text(p.read_text().strip() + "\n")


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, f, msg):
        self.errors.append(f"[{f}] {msg}")

    def warn(self, f, msg):
        self.warnings.append(f"[{f}] {msg}")


def _context(text, m, width=60):
    return text[max(0, m.start() - width): m.end() + width].replace("\n", " ")


def check_common(rep, fname, text, forbid_call_only=True):
    low = text.lower()
    for b in BRANDS:
        if re.search(rf"\b{re.escape(b)}\b", text):
            rep.err(fname, f"real brand mentioned: {b}")
    if forbid_call_only:
        for k in CALL_ONLY:
            if re.search(rf"(?<![\w-]){re.escape(k.lower())}(?![\w-])", low):
                rep.err(fname, f"call/bulletin-only term present: '{k}'")
    for m in FIGURE_VALUE.finditer(text):
        rep.err(fname, f"figure-only value: '...{_context(text, m)}...'")
    for m in PERCENT_NEAR_ALT.finditer(text):
        rep.err(fname, f"altitude derate % in text: '...{_context(text, m)}...'")
    for m in WIRE_COLOR.finditer(text):
        rep.warn(fname, f"possible wire color: '...{_context(text, m)}...'")
    if "```" in text:
        rep.warn(fname, "contains code fences (rendered as monospace blocks)")
    for m in re.finditer(r".\[\[FIGURE:[^\]]+\]\]|\[\[FIGURE:[^\]]+\]\].", text):
        rep.warn(fname, f"inline figure reference (rendered as the figure title): '{m.group()}'")


def check_manuals(world, figs, rep):
    for series in world["series"]:
        p = CONTENT / "manuals" / f"{series}.md"
        if not p.exists():
            rep.err(f"manuals/{series}.md", "missing")
            continue
        text = p.read_text()
        lines = text.splitlines()
        if not lines or not lines[0].startswith("# "):
            rep.err(p.name, "line 1 must be the '# ' title")
        if f"doc_id: {series}-IOM" not in text[:400]:
            rep.err(p.name, "doc_id comment missing on line 2")
        for f in (f for f in figs if f["series"] == series):
            n = len(re.findall(rf"^\[\[FIGURE:{re.escape(f['figure_id'])}\]\]\s*$", text, re.M))
            if n != 1:
                rep.err(p.name, f"placeholder {f['figure_id']} appears {n} times (need exactly 1)")
        unknown = set(re.findall(r"\[\[FIGURE:([^\]]+)\]\]", text)) - {f["figure_id"] for f in figs}
        for u in unknown:
            rep.err(p.name, f"unknown figure placeholder {u}")
        nt = norm(text)
        for mid, m in world["models"].items():
            if m["series"] != series:
                continue
            for k, v in m["text_facts"].items():
                if norm(v) not in nt:
                    rep.err(p.name, f"{mid} fact '{k}' not found verbatim: {v!r}")
        for s in world["series"][series]["text_facts"]:
            if norm(s) not in nt:
                rep.err(p.name, f"series sentence missing: {s!r}")
        words = len(re.findall(r"\w+", text))
        if words < 5500:
            rep.warn(p.name, f"only {words} words (target 6,500–9,000)")
        check_common(rep, p.name, text)


def check_bulletins(world, rep):
    for b in world["bulletins"]:
        p = CONTENT / "bulletins" / f"{b['id']}.md"
        if not p.exists():
            rep.err(f"bulletins/{b['id']}.md", "missing")
            continue
        text = p.read_text()
        for fact in b["facts"]:
            if norm(fact) not in norm(text):
                rep.err(p.name, f"fact missing: {fact!r}")
        allowed = {"VPN-0475"} if b["id"] == "SB-23-014" else {"VPN-6120"} if b["id"] == "SB-24-003" else set()
        low = text.lower()
        for k in CALL_ONLY:
            if k in allowed or k == "warranty":
                continue
            if re.search(rf"(?<![\w-]){re.escape(k.lower())}(?![\w-])", low):
                rep.err(p.name, f"call-only term present: '{k}'")
        check_common(rep, p.name, text, forbid_call_only=False)


HEADER = re.compile(r"^-{3,}[ \t]*\n\s*(.*?)\n\s*-{3,}[ \t]*\n(.*)$", re.S)


def parse_call(path):
    """-> (header dict, [(speaker, text), ...]) or (None, None) if the header block is missing."""
    m = HEADER.match(path.read_text().strip())
    if not m:
        return None, None
    hdr = {k.strip(): v.strip() for k, v in (ln.split(":", 1) for ln in m.group(1).splitlines() if ":" in ln)}
    turns = [(sp, txt.strip()) for sp, txt in re.findall(r"^(AGENT|TECH):\s*(.+)$", m.group(2), re.M)]
    return hdr, (m.group(2).strip(), turns)


def check_calls(world, rep):
    for c in world["calls"]:
        p = CONTENT / "calls" / f"{c['id']}.txt"
        if not p.exists():
            rep.err(f"calls/{c['id']}.txt", "missing")
            continue
        hdr, parsed = parse_call(p)
        if hdr is None:
            rep.err(p.name, "missing --- header block")
            continue
        for k in ("call_id", "date", "site", "unit", "model", "tech", "agent", "topic"):
            if k not in hdr:
                rep.err(p.name, f"header field '{k}' missing")
        if hdr.get("call_id") != c["id"]:
            rep.err(p.name, f"call_id is {hdr.get('call_id')!r}")
        body = parsed[0]
        bad = [ln for ln in body.splitlines() if ln.strip() and not re.match(r"^(AGENT|TECH):\s+\S", ln)]
        for ln in bad[:3]:
            rep.err(p.name, f"non-dialogue line: {ln[:80]!r}")
        if re.search(r"\d", body):
            bits = re.findall(r".{0,25}\d.{0,25}", body)[:2]
            rep.err(p.name, f"digits in dialogue: {bits}")
        words = len(re.findall(r"\w+", body))
        if not 270 <= words <= 620:
            rep.warn(p.name, f"{words} words (target 300–550)")
        nb = re.sub(r"[^\w\s-]", "", norm(body))
        for phrase in c["must_say"]:
            if re.sub(r"[^\w\s-]", "", norm(phrase)) not in nb:
                rep.err(p.name, f"required phrase missing: {phrase!r}")


def main() -> int:
    world = json.loads((SPEC / "world.json").read_text())
    figs = json.loads((SPEC / "figures.json").read_text())
    split_raw()
    rep = Report()
    check_manuals(world, figs, rep)
    check_bulletins(world, rep)
    check_calls(world, rep)
    for w in rep.warnings:
        print("WARN ", w)
    for e in rep.errors:
        print("ERROR", e)
    print(f"\n{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
