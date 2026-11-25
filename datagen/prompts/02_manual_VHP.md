# Prompt: write the VHP Series Installation, Operation & Maintenance manual

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

## Your task

Write the complete **Installation, Operation and Maintenance (IOM) manual** for the
**VHP Series Packaged Rooftop Heat Pump**, covering models VHP-036, VHP-048, VHP-060. Control board: VCB-210.
Compressor: single-stage scroll. Refrigerant: R-454B.

Length: **6,500–9,000 words** of prose plus tables. It should read like a real manufacturer IOM:
numbered sections, short procedural steps, WARNING/CAUTION/NOTE callouts, specification and
maintenance tables, and a troubleshooting table.

### Required section outline (use these, in this order; you may add subsections)
1. Safety considerations (include A2L refrigerant safety)
2. Model number nomenclature
3. Specifications (one table per model)
4. Installation and clearances
5. Leveling and condensate
6. Electrical connections (refer to wiring figure)
7. Thermostat and controls
8. Sequence of operation — cooling
9. Sequence of operation — heating and auxiliary heat
10. Defrost operation (state the interval options and default)
11. Defrost / outdoor coil sensor check (refer to the resistance curve figure)
12. Refrigerant charging in cooling mode (one subsection per model with its charging chart)
13. Indoor airflow adjustment (one blower table per model)
14. Refrigerant detection system (A2L)
15. Control board diagnostics (LED figure)
16. Maintenance schedule
17. Troubleshooting

### Required facts — must appear verbatim
Put each model's facts in its Specifications table exactly as written (same numbers, units,
punctuation). You may repeat them in prose, but never contradict them.

**VHP-036**

| Field | Value (copy exactly) |
|---|---|
| Nominal capacity (tons) | 3 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 35,300 |
| Factory refrigerant charge | 4 lb 0 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 2 filters, 16 x 25 x 2 in. |
| Operating weight | 370 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-1-60, 208/230-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

**VHP-048**

| Field | Value (copy exactly) |
|---|---|
| Nominal capacity (tons) | 4 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 46,500 |
| Factory refrigerant charge | 5 lb 1 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 2 filters, 20 x 25 x 2 in. |
| Operating weight | 480 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-1-60, 208/230-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

**VHP-060**

| Field | Value (copy exactly) |
|---|---|
| Nominal capacity (tons) | 5 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 59,300 |
| Factory refrigerant charge | 5 lb 15 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 3 filters, 20 x 25 x 2 in. |
| Operating weight | 580 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-3-60, 460-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

Also include each of these sentences verbatim, in the most appropriate section:
- The unit must be level within 1/4 in. side to side so the condensate and defrost water drain correctly.
- Auxiliary electric heat kits are available in 5, 10 and 15 kW sizes.

### Required figure placeholders — each exactly once, on its own line
These figures are rendered by code and inserted where you place the placeholder. You cannot see
them. Introduce each with a sentence that names the figure by its title, says what it is used
for, and tells the reader how to read it, **without stating any value from it**.
- `[[FIGURE:VHP-036-CC]]` — VHP-036 Cooling Charging Chart
- `[[FIGURE:VHP-036-BT]]` — VHP-036 Indoor Blower Performance
- `[[FIGURE:VHP-048-CC]]` — VHP-048 Cooling Charging Chart
- `[[FIGURE:VHP-048-BT]]` — VHP-048 Indoor Blower Performance
- `[[FIGURE:VHP-060-CC]]` — VHP-060 Cooling Charging Chart
- `[[FIGURE:VHP-060-BT]]` — VHP-060 Indoor Blower Performance
- `[[FIGURE:VHP-WD]]` — VHP Series Control Wiring Diagram and Electrical Data
- `[[FIGURE:VHP-LED]]` — VHP Series Status LED Flash Codes
- `[[FIGURE:VHP-TH]]` — VHP Series Sensor Resistance vs. Temperature

Put per-model figures inside per-model subsections (for example "14.2 Charging the VHP-048").

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

## Output format (strict, parsed by code)
- Line 1: `# Vantorr VHP Series Packaged Rooftop Heat Pump — Installation, Operation and Maintenance Manual`
- Line 2: `<!-- doc_id: VHP-IOM | revision: C | date: 2024-02 -->`
- Sections: `## <n>. <Title>`; subsections: `### <n>.<m> <Title>`. Put `[[PAGEBREAK]]` on its own line before every `##` section except the first.
- Callouts: a line starting with `> **WARNING:**`, `> **CAUTION:**` or `> **NOTE:**`.
- Tables: GitHub pipe tables, at most 5 columns, no merged cells.
- Lists: `-` for bullets, `1.` for numbered steps.
- Figures: the exact placeholder line, e.g. `[[FIGURE:VHP-036-CC]]`, nothing else on that line.
- No images, no links, no HTML except the doc_id comment, no code fences, no emoji.

## Self-check before you answer
- [ ] Every required fact appears verbatim; every placeholder appears exactly once.
- [ ] No figure-only values, no forbidden call/bulletin facts, no invented part numbers or settings.
- [ ] No real brand names. Output starts with the `#` title line and contains nothing else.

Save your whole answer as `data/content/_raw/manual_VHP.md`.
