"""Write the prompts I gave an outside LLM to write the prose parts of the corpus.

The LLM only writes prose and dialogue. Facts it has to include come from world.json, and the
figure-only and call-only facts are left out and explicitly banned.

Run:  uv run python -m datagen.prompts      -> datagen/prompts/*.md
"""
from __future__ import annotations

import json

from fieldnote.config import ROOT, SPEC

OUT = ROOT / "datagen" / "prompts"
RAW = "data/content/_raw"

NUM_WORDS = {24: "twenty-four", 36: "thirty-six", 48: "forty-eight", 60: "sixty", 90: "ninety",
             120: "one-twenty", 150: "one-fifty"}

COMMON_CONTEXT = """\
## Context (read fully before writing)

You are writing part of a **synthetic, fully fictional** document corpus for an open-source
portfolio project called *Fieldnote*: a retrieval-augmented assistant for commercial HVAC field
technicians. The corpus will be published on GitHub, so it must be realistic and technically
plausible but must not copy or imitate any real company.

The fictional world:
- **Manufacturer:** Vantorr Climate Systems ("Vantorr"). Technical support line: "Vantorr Technical Support".
- **Contractor whose technicians use the assistant:** Ridgeline Mechanical Services ("Ridgeline").
- **Product series:** VRT (packaged rooftop, gas heat), VHP (packaged rooftop heat pump), VCU (split
  condensing unit), VAH (air handler), VRL (large two-stage packaged rooftop).
- **Control boards:** VCB-200 (VRT), VCB-210 (VHP), VCB-110 (VCU), VAB-50 (VAH), VCB-400 (VRL).
- **Refrigerants:** R-454B for VRT, VHP and VRL; R-410A for VCU and VAH.

Hard rules that apply to everything you write:
1. **Never mention real brands, companies, products or people** (e.g. no Carrier, Trane, Lennox,
   Daikin, York, Copeland, Honeywell, Emerson, White-Rodgers, Goodman, Rheem). Generic part types
   ("scroll compressor", "TXV", "contactor") are fine.
2. **Never invent part numbers, firmware versions, DIP-switch or jumper settings, case/ticket
   numbers, or numeric specifications** beyond what this prompt gives you. If a realistic document
   would show a number you were not given, refer the reader to the named figure or to the unit
   rating plate instead.
3. The corpus is used to **test whether a system can read charts and diagrams**. Some values exist
   only inside figure images, which you cannot see. You will be told which ones. Never state them,
   estimate them, or give "typical" values for them.
4. Write in US English, imperial units, the tone of a real manufacturer document or real phone call.
5. Output **only** the requested content in the exact format specified. No preamble, no closing
   remarks, no Markdown code fences around the output.
"""

FORBIDDEN_FIGURE = """\
### Forbidden: figure-only values (never write these, not even approximately)
- Any **charging pressures** (target liquid or suction pressures, subcooling/superheat targets).
- Any **high- or low-pressure switch** open/close setpoints.
- Any **MCA, MOP, fuse size, breaker size**, or full-load amps.
- Any **blower airflow (CFM)** numbers or static-pressure/airflow pairs.
- Any **sensor/thermistor resistance** values (kΩ / ohms) or resistance–temperature pairs.
- Any **high-altitude derate percentages**.
- Any **additional refrigerant per foot** for long line sets.
- Any **wire colors** or terminal-to-terminal wiring descriptions.
- Any **LED flash-code patterns or their meanings** (say "see the Status LED Flash Codes figure").
- Do not describe whether the reversing valve is energized in heating or cooling, or whether the
  thermostat should be configured for O or B.

When you need one of these, write a sentence like "Find the target liquid pressure on the
*VRT-048 Cooling Charging Chart* (figure below)" and place the figure placeholder.
"""

FORBIDDEN_CALLS = """\
### Forbidden: facts that belong to support calls or service bulletins (never mention)
Firmware versions of any board; HPS input debounce; lockout-after-three-trips behavior; event or
error codes like "E41"; part numbers VPN-0475, VPN-4471, VPN-5520, VPN-3310, VPN-2208, VPN-1190,
VPN-6120, VHS-35, VLA-2, VTX-2, VCP-150T, RDS-1; hard-start kits; low-ambient kits; TXV kits or
fixed-orifice sizes; stage-delay times or DIP switches/jumpers of any kind (including JP7);
economizer actuator signal ranges (2–10 V / 0–10 V); phase-monitor trip percentages; heat-strip
staging delays; igniter resistance values; recommended defrost settings for snowy climates;
warm-up delays after power loss; known leak locations; blower set-screw torque; sensor service
life; low-ambient compressor lockout temperatures; warranty terms; capacitor ratings or capacitor
failures; how long A2L mitigation mode lasts after a leak clears; fan-blade cracking.
"""

MANUAL_SECTIONS = {
    "VRT": ["Safety considerations (include A2L refrigerant safety)", "Model number nomenclature",
            "Specifications (one Markdown table per model with the required facts)", "Receiving and rigging",
            "Roof curb and installation (clearances, slope requirement)", "Condensate drain",
            "Gas piping and venting", "High-altitude installation (refer to the derate figure)",
            "Electrical connections (refer to the wiring diagram figure)", "Thermostat and controls",
            "Sequence of operation — cooling", "Sequence of operation — gas heating", "Start-up checklist",
            "Refrigerant charging (one subsection per model, each with that model's charging chart)",
            "Indoor airflow adjustment (one blower table per model)", "Refrigerant detection system (A2L)",
            "Control board diagnostics (refer to the LED flash code figure)", "Maintenance schedule",
            "Troubleshooting (symptom / possible cause / check table, no forbidden values)"],
    "VHP": ["Safety considerations (include A2L refrigerant safety)", "Model number nomenclature",
            "Specifications (one table per model)", "Installation and clearances", "Leveling and condensate",
            "Electrical connections (refer to wiring figure)", "Thermostat and controls",
            "Sequence of operation — cooling", "Sequence of operation — heating and auxiliary heat",
            "Defrost operation (state the interval options and default)",
            "Defrost / outdoor coil sensor check (refer to the resistance curve figure)",
            "Refrigerant charging in cooling mode (one subsection per model with its charging chart)",
            "Indoor airflow adjustment (one blower table per model)", "Refrigerant detection system (A2L)",
            "Control board diagnostics (LED figure)", "Maintenance schedule", "Troubleshooting"],
    "VCU": ["Safety considerations", "Model number nomenclature", "Specifications (one table per model)",
            "Location and clearances", "Refrigerant piping (line length and lift limits, brazing, evacuation)",
            "Long line sets (refer to the additional refrigerant figure; do not give values)",
            "Electrical connections (wiring figure)", "Outdoor air sensor check (resistance curve figure)",
            "Sequence of operation", "Start-up", "Refrigerant charging (one subsection per model with its chart)",
            "Control board diagnostics (LED figure)", "Maintenance", "Troubleshooting"],
    "VAH": ["Safety considerations", "Model number nomenclature", "Specifications (one table per model)",
            "Installation positions (upflow, downflow, horizontal left/right)", "Condensate and secondary drain pan",
            "Ductwork", "Electrical connections and electric heat (wiring figure)",
            "Refrigerant detection sensor (A2L-ready; general description only)",
            "Blower performance (one blower chart per model)", "Sequence of operation",
            "Control board diagnostics (LED figure)", "Maintenance", "Troubleshooting"],
    "VRL": ["Safety considerations (A2L)", "Model number nomenclature", "Specifications (one table per model)",
            "Rigging and roof curb", "Clearances", "Condensate", "Electrical and three-phase power (wiring figure)",
            "Crankcase heaters and pre-start", "Economizer (general operation, changeover setpoint is field adjustable)",
            "Sequence of operation — two-stage cooling", "Start-up checklist",
            "Refrigerant charging (both circuits; one subsection per model with its charging chart)",
            "Indoor airflow (one blower table per model)", "Refrigerant detection system (A2L)",
            "Control board diagnostics (LED figure)", "Maintenance", "Troubleshooting"],
}

FACT_LABELS = {
    "nominal_tons": "Nominal capacity (tons)", "refrigerant": "Refrigerant",
    "cooling_capacity_btuh": "Cooling capacity (Btuh)", "factory_charge": "Factory refrigerant charge",
    "min_cooling_ambient_f": "Minimum outdoor temperature for cooling", "anti_short_cycle_delay": "Anti-short-cycle delay",
    "filter": "Return air filters", "operating_weight_lb": "Operating weight", "clearances_in": "Required clearances",
    "voltage_options": "Voltage options", "defrost_interval_options": "Defrost interval",
    "heating_input_btuh": "Gas heating input (Btuh)", "stages": "Cooling stages",
}


def manual_prompt(world: dict, series: str, figs: list[dict]) -> str:
    sd = world["series"][series]
    models = {k: v for k, v in world["models"].items() if v["series"] == series}
    fig_lines = "\n".join(f"- `[[FIGURE:{f['figure_id']}]]` — {f['title']}" for f in figs)
    facts = []
    for mid, m in models.items():
        facts.append(f"\n**{mid}**\n\n| Field | Value (copy exactly) |\n|---|---|")
        facts += [f"| {FACT_LABELS[k]} | {v} |" for k, v in m["text_facts"].items()]
    series_sentences = "\n".join(f"- {s}" for s in sd["text_facts"])
    sections = "\n".join(f"{i}. {s}" for i, s in enumerate(MANUAL_SECTIONS[series], 1))
    return f"""\
# Prompt: write the {series} Series Installation, Operation & Maintenance manual

{COMMON_CONTEXT}
## Your task

Write the complete **Installation, Operation and Maintenance (IOM) manual** for the
**{sd['title']}**, covering models {", ".join(models)}. Control board: {sd['board']}.
Compressor: {sd['compressor'] or "none (air handler)"}. Refrigerant: {sd['refrigerant']}.

Length: **6,500–9,000 words** of prose plus tables. It should read like a real manufacturer IOM:
numbered sections, short procedural steps, WARNING/CAUTION/NOTE callouts, specification and
maintenance tables, and a troubleshooting table.

### Required section outline (use these, in this order; you may add subsections)
{sections}

### Required facts — must appear verbatim
Put each model's facts in its Specifications table exactly as written (same numbers, units,
punctuation). You may repeat them in prose, but never contradict them.
{chr(10).join(facts)}

Also include each of these sentences verbatim, in the most appropriate section:
{series_sentences}

### Required figure placeholders — each exactly once, on its own line
These figures are rendered by code and inserted where you place the placeholder. You cannot see
them. Introduce each with a sentence that names the figure by its title, says what it is used
for, and tells the reader how to read it, **without stating any value from it**.
{fig_lines}

Put per-model figures inside per-model subsections (for example "14.2 Charging the {list(models)[1]}").

{FORBIDDEN_FIGURE}
{FORBIDDEN_CALLS}
## Output format (strict, parsed by code)
- Line 1: `# Vantorr {sd['title']} — Installation, Operation and Maintenance Manual`
- Line 2: `<!-- doc_id: {series}-IOM | revision: C | date: 2024-02 -->`
- Sections: `## <n>. <Title>`; subsections: `### <n>.<m> <Title>`. Put `[[PAGEBREAK]]` on its own line before every `##` section except the first.
- Callouts: a line starting with `> **WARNING:**`, `> **CAUTION:**` or `> **NOTE:**`.
- Tables: GitHub pipe tables, at most 5 columns, no merged cells.
- Lists: `-` for bullets, `1.` for numbered steps.
- Figures: the exact placeholder line, e.g. `[[FIGURE:{figs[0]['figure_id']}]]`, nothing else on that line.
- No images, no links, no HTML except the doc_id comment, no code fences, no emoji.

## Self-check before you answer
- [ ] Every required fact appears verbatim; every placeholder appears exactly once.
- [ ] No figure-only values, no forbidden call/bulletin facts, no invented part numbers or settings.
- [ ] No real brand names. Output starts with the `#` title line and contains nothing else.

Save your whole answer as `{RAW}/manual_{series}.md`.
"""


def bulletins_prompt(world: dict) -> str:
    blocks = []
    for b in world["bulletins"]:
        facts = "\n".join(f"  - {f}" for f in b["facts"])
        blocks.append(f"- **{b['id']}** — {b['title']}\n  - Date: {b['date']}\n  - Applies to: {b['applies_to']}\n"
                      f"  - Facts to include verbatim:\n{facts}")
    return f"""\
# Prompt: write three Vantorr service bulletins

{COMMON_CONTEXT}
## Your task

Write three short **technical service bulletins** from Vantorr Climate Systems. Each is
**250–450 words**. Use only the facts given; add realistic procedure steps (safety lockout,
inspection, replacement, verification, documentation) that do not introduce new numbers, part
numbers or settings.

{chr(10).join(blocks)}

Each bulletin's structure:
1. `# Service Bulletin <id>: <title>`
2. `<!-- doc_id: <id> | date: <date> -->`
3. A 2-column pipe table with rows: Bulletin No., Date, Subject, Applies To, Category (choose "Product improvement" or "Field service guidance").
4. `## Purpose`, `## Background`, `## Identification`, `## Procedure` (numbered steps), `## Parts`, `## Warranty and Documentation`.
5. Safety callouts as lines beginning `> **WARNING:**` or `> **NOTE:**`.

Bulletin-specific rules: do not mention any firmware, debounce, lockout counts, or other call-only
facts. SB-23-014 must not describe charging pressures or HPS setpoints. Only SB-23-014 may mention
capacitors.

{FORBIDDEN_FIGURE}
## Output format (strict, parsed by code)
Output the three bulletins one after another, each preceded by a marker line exactly like
`<<<FILE: SB-23-014.md>>>`. No other text before, between, or after.

Save your whole answer as `{RAW}/bulletins.md`.
"""


def spoken_model(mid: str) -> str:
    series, size = mid.split("-")
    return f"{'-'.join(series)} {NUM_WORDS[int(size)]}"


def calls_prompt(world: dict, calls: list[dict], part: int) -> str:
    sites = {s["id"]: s for s in world["sites"]}
    blocks = []
    for c in calls:
        a = next(x for x in world["assets"] if x["site_id"] == c["site"] and x["unit"] == c["unit"])
        must = "\n".join(f'    - "{m}"' for m in c["must_say"])
        speaker = "either speaker (the tech reports the result, the agent explains the code)" \
            if c["id"] == "C19" else "the AGENT"
        blocks.append(f"""\
- **{c['id']}** — {c['topic']}
  - date: {c['date']} | site: {sites[c['site']]['name']} ({sites[c['site']]['city']}) | unit: {c['unit']}
  - model: {a['model']} (spoken: "{spoken_model(a['model'])}") | serial on rating plate: {a['serial']}
  - tech: {c['tech']} (Ridgeline Mechanical Services) | agent: {c['agent']} (Vantorr Technical Support)
  - Phrases {speaker} must say, word for word (inside longer natural sentences is fine):
{must}""")
    return f"""\
# Prompt: write {len(calls)} recorded technical-support phone calls (part {part} of 2)

{COMMON_CONTEXT}
## Your task

Write **{len(calls)} phone-call transcripts** between a Ridgeline field technician (usually on a
roof or in a mechanical room) and a Vantorr Technical Support agent. These scripts will be turned
into audio with text-to-speech and then transcribed back with a speech recognizer, so write the
way people **talk**, not the way they write.

### Calls to write
{chr(10).join(blocks)}

### Dialogue requirements
- **300–550 words per call, 14–30 turns.** The agent answers with a greeting naming Vantorr Technical Support.
- The tech gives the site, unit tag, model (spoken form) and reads the serial number aloud
  character by character (for example "two three one oh, V, zero zero four one two").
- The tech describes symptoms. The agent asks 2–4 sensible diagnostic questions, then delivers the
  required phrases. Each phrase must appear **exactly as written** (same words; case and
  surrounding punctuation may differ).
- Natural speech: short sentences, "uh", "okay", "hang on", a little background mention (wind,
  ladder, a running unit), the agent putting the tech on a short hold, a polite close.
- **No digits anywhere in the dialogue.** Say all numbers, model names and units as words (for
  example "four sixty volt", "R four fifty-four B", "V-C-B two hundred").
- The only extra facts allowed are harmless conversational ones. Do not add numeric specs, part
  numbers, settings or case numbers beyond the required phrases. Do not mention figure-only values.
- Each call is about its own topic only. Do not leak another call's facts.
{"- C19 is a follow-up to C01 (same tech, same unit, a week later); refer back to that call." if part == 2 else ""}

{FORBIDDEN_FIGURE}
## Output format (strict, parsed by code)
For each call, output exactly:

<<<FILE: C01.txt>>>
---
call_id: C01
date: 2025-07-14
site: <site name>
unit: <unit tag>
model: <model, e.g. VRT-060>
tech: <name>
agent: <name>
topic: <topic>
---
AGENT: <words>
TECH: <words>
...

Every dialogue line starts with `AGENT:` or `TECH:`. No stage directions, no blank speaker lines,
no other text before, between or after the calls.

Save your whole answer as `{RAW}/calls_part{part}.md`.
"""


README = f"""\
# Content-generation prompts

These prompts produce the **prose and dialogue only**. Every number the eval depends on is
generated by code (`datagen/world.py`) and rendered into figures (`datagen/figures.py`).
The LLM never sees figure-only values, so it cannot leak them into the text layer.

## How to run (8 prompts, no back-and-forth needed)
1. Use any strong long-output model (Claude, GPT, Gemini). **Start a fresh chat for each prompt.**
2. Paste the **entire** prompt file. Copy the **entire** answer, unedited.
3. Save the answer to the path at the bottom of each prompt (all under `{RAW}/`):

| Prompt | Save answer as |
|---|---|
| 01_manual_VRT.md | `{RAW}/manual_VRT.md` |
| 02_manual_VHP.md | `{RAW}/manual_VHP.md` |
| 03_manual_VCU.md | `{RAW}/manual_VCU.md` |
| 04_manual_VAH.md | `{RAW}/manual_VAH.md` |
| 05_manual_VRL.md | `{RAW}/manual_VRL.md` |
| 06_bulletins.md | `{RAW}/bulletins.md` |
| 07_calls_part1.md | `{RAW}/calls_part1.md` |
| 08_calls_part2.md | `{RAW}/calls_part2.md` |

4. Run `make content`. It splits the files and runs the validator. Any failure names the file, the
   rule and the offending text, so you can re-run just that prompt or hand-fix one line.

If an answer gets cut off (output limit), reply "continue exactly where you stopped" in the same
chat and append the continuation to the same file.
"""


def main() -> None:
    world = json.loads((SPEC / "world.json").read_text())
    figs = json.loads((SPEC / "figures.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {"README.md": README}
    for i, series in enumerate(["VRT", "VHP", "VCU", "VAH", "VRL"], 1):
        files[f"0{i}_manual_{series}.md"] = manual_prompt(world, series, [f for f in figs if f["series"] == series])
    files["06_bulletins.md"] = bulletins_prompt(world)
    files["07_calls_part1.md"] = calls_prompt(world, world["calls"][:12], 1)
    files["08_calls_part2.md"] = calls_prompt(world, world["calls"][12:], 2)
    for name, body in files.items():
        (OUT / name).write_text(body)
    print("wrote", ", ".join(files), "->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
