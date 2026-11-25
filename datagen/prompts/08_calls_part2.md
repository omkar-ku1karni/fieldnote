# Prompt: write 12 recorded technical-support phone calls (part 2 of 2)

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

Write **12 phone-call transcripts** between a Ridgeline field technician (usually on a
roof or in a mechanical room) and a Vantorr Technical Support agent. These scripts will be turned
into audio with text-to-speech and then transcribed back with a speech recognizer, so write the
way people **talk**, not the way they write.

### Calls to write
- **C13** — Phase monitor nuisance trips
  - date: 2025-07-02 | site: Harbor Point Distribution Center (Kenosha, WI) | unit: RTU-1
  - model: VRL-090 (spoken: "V-R-L ninety") | serial on rating plate: 2201V00185
  - tech: Marcus Bell (Ridgeline Mechanical Services) | agent: Alicia (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "factory unbalance trip is ten percent"
    - "the dial goes from five to fifteen percent"
    - "set it to eight percent on that utility"
- **C14** — Pairing a condenser with an air handler — metering device
  - date: 2025-05-12 | site: Lakeshore Medical Office Building (Milwaukee, WI) | unit: CU-1
  - model: VCU-024 (spoken: "V-C-U twenty-four") | serial on rating plate: 2116V01821
  - tech: Dana Ortiz (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the V-C-U oh-two-four ships with a fixed orifice"
    - "with the V-A-H oh-two-four you install TXV kit V-T-X two"
    - "remove the fixed orifice"
- **C15** — Electric heat staging timing
  - date: 2025-11-18 | site: Northgate Fitness Center (Golden, CO) | unit: RTU-4
  - model: VAH-048 (spoken: "V-A-H forty-eight") | serial on rating plate: 2431V01785
  - tech: Sam Okafor (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the V-A-B fifty board stages the heat strips thirty seconds apart"
- **C16** — Gas valve has 24 volts but no flame
  - date: 2025-11-03 | site: Brookhaven Elementary School (Madison, WI) | unit: RTU-3
  - model: VRT-048 (spoken: "V-R-T forty-eight") | serial on rating plate: 2120V00102
  - tech: Priya Raman (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "igniter part V-P-N eleven ninety"
    - "forty to seventy-five ohms cold"
    - "over a hundred ohms replace it"
- **C17** — Defrost interval for a snowy site
  - date: 2025-12-15 | site: Elm & 3rd Retail Plaza (Waukesha, WI) | unit: RTU-3
  - model: VHP-048 (spoken: "V-H-P forty-eight") | serial on rating plate: 2105V00910
  - tech: Luis Herrera (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "in heavy snow we recommend thirty minutes instead of the default sixty"
- **C18** — Unit will not start after a winter power outage
  - date: 2025-02-10 | site: Riverside Public Library (Racine, WI) | unit: RTU-1
  - model: VRL-120 (spoken: "V-R-L one-twenty") | serial on rating plate: 2409V01504
  - tech: Jen Kowalski (Ridgeline Mechanical Services) | agent: Alicia (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the V-C-B four hundred board enforces a four hour warm-up delay"
    - "after a cold power-up below fifty degrees outside"
- **C19** — Follow-up after firmware update and capacitor replacement
  - date: 2025-07-22 | site: Lakeshore Medical Office Building (Milwaukee, WI) | unit: RTU-7
  - model: VRT-060 (spoken: "V-R-T sixty") | serial on rating plate: 2310V00412
  - tech: Dana Ortiz (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases either speaker (the tech reports the result, the agent explains the code) must say, word for word (inside longer natural sentences is fine):
    - "running fine since the update and the new capacitor"
    - "high-pressure trips now show up as event code E forty-one in the history log"
- **C20** — Slow refrigerant leak search
  - date: 2025-09-09 | site: Riverside Public Library (Racine, WI) | unit: CU-1
  - model: VCU-036 (spoken: "V-C-U thirty-six") | serial on rating plate: 2339V00300
  - tech: Jen Kowalski (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "known leak point at the liquid service valve braze joint on the twenty twenty-one builds"
- **C21** — Rattling noise from air handler
  - date: 2025-03-25 | site: Brookhaven Elementary School (Madison, WI) | unit: AH-1
  - model: VAH-024 (spoken: "V-A-H twenty-four") | serial on rating plate: 2340V01542
  - tech: Priya Raman (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "blower wheel set screw works loose"
    - "torque it to thirty inch-pounds"
- **C22** — Refrigerant detection sensor fault, blower will not shut off
  - date: 2025-08-27 | site: Northgate Fitness Center (Golden, CO) | unit: RTU-3
  - model: VRT-036 (spoken: "V-R-T thirty-six") | serial on rating plate: 2317V01584
  - tech: Sam Okafor (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the R-D-S one sensor has a five year service life"
    - "a sensor fault forces the blower on in mitigation mode"
- **C23** — Heat pump compressor locked out in cold weather
  - date: 2025-12-01 | site: Harbor Point Distribution Center (Kenosha, WI) | unit: RTU-5
  - model: VHP-060 (spoken: "V-H-P sixty") | serial on rating plate: 2105V00428
  - tech: Marcus Bell (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "low ambient compressor lockout is zero degrees from the factory"
    - "DIP switches two and three"
    - "with dual fuel set it to ten degrees"
- **C24** — Failed compressor on circuit two — interim operation
  - date: 2025-10-07 | site: Elm & 3rd Retail Plaza (Waukesha, WI) | unit: RTU-5
  - model: VRL-150 (spoken: "V-R-L one-fifty") | serial on rating plate: 2233V01848
  - tech: Luis Herrera (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "replacement compressor part V-C-P one-fifty-T"
    - "about a three week lead time"
    - "disable circuit two with DIP switch six and run on circuit one"

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
- C19 is a follow-up to C01 (same tech, same unit, a week later); refer back to that call.

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

Save your whole answer as `data/content/_raw/calls_part2.md`.
