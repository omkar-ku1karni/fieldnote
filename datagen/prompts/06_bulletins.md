# Prompt: write three Vantorr service bulletins

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

Write three short **technical service bulletins** from Vantorr Climate Systems. Each is
**250–450 words**. Use only the facts given; add realistic procedure steps (safety lockout,
inspection, replacement, verification, documentation) that do not introduce new numbers, part
numbers or settings.

- **SB-23-014** — VRT-060 condenser fan motor run capacitor — early failures
  - Date: 2023-11-06
  - Applies to: VRT-060 units with serial numbers 2307V00001 through 2312V99999
  - Facts to include verbatim:
  - Original condenser fan run capacitor is rated 5 µF / 370 VAC and can swell and lose capacitance after one to two cooling seasons.
  - Replace with upgraded capacitor part number VPN-0475 (5 µF / 440 VAC).
  - A weak capacitor reduces condenser fan speed, which raises head pressure on hot days and can cause high-pressure switch trips.
  - Warranty labor allowance: 0.5 hours.
- **SB-24-003** — VRL-150 condenser fan blade inspection
  - Date: 2024-03-18
  - Applies to: VRL-150 units built in 2023
  - Facts to include verbatim:
  - Inspect condenser fan blades for hairline cracks at the hub during every spring start-up.
  - Replace cracked blades with fan blade kit VPN-6120; torque hub set screws to 160 in-lb.
  - Do not operate the unit with a cracked blade.
- **SB-24-011** — A2L refrigerant detection system — field service guidance
  - Date: 2024-09-02
  - Applies to: All R-454B units (VRT, VHP, VRL)
  - Facts to include verbatim:
  - When the refrigerant detection sensor senses a leak, the board shuts off the compressor and runs the indoor blower continuously (mitigation mode).
  - Mitigation mode continues for at least 5 minutes after the sensor reading clears.
  - Never bypass or jumper the refrigerant detection sensor.

Each bulletin's structure:
1. `# Service Bulletin <id>: <title>`
2. `<!-- doc_id: <id> | date: <date> -->`
3. A 2-column pipe table with rows: Bulletin No., Date, Subject, Applies To, Category (choose "Product improvement" or "Field service guidance").
4. `## Purpose`, `## Background`, `## Identification`, `## Procedure` (numbered steps), `## Parts`, `## Warranty and Documentation`.
5. Safety callouts as lines beginning `> **WARNING:**` or `> **NOTE:**`.

Bulletin-specific rules: do not mention any firmware, debounce, lockout counts, or other call-only
facts. SB-23-014 must not describe charging pressures or HPS setpoints. Only SB-23-014 may mention
capacitors.

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

## Output format (strict, parsed by code)
Output the three bulletins one after another, each preceded by a marker line exactly like
`<<<FILE: SB-23-014.md>>>`. No other text before, between, or after.

Save your whole answer as `data/content/_raw/bulletins.md`.
