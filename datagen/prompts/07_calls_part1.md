# Prompt: write 12 recorded technical-support phone calls (part 1 of 2)

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
- **C01** — Repeated high-pressure lockouts on hot afternoons
  - date: 2025-07-14 | site: Lakeshore Medical Office Building (Milwaukee, WI) | unit: RTU-7
  - model: VRT-060 (spoken: "V-R-T sixty") | serial on rating plate: 2310V00412
  - tech: Dana Ortiz (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "firmware two point three"
    - "no debounce on the high-pressure switch input"
    - "locks out hard after three trips in one hour"
    - "fixed in firmware two point four point one"
    - "update it with the service app over the USB-C port"
    - "check the condenser fan capacitor"
- **C02** — Heat pump defrost not terminating
  - date: 2025-01-22 | site: Brookhaven Elementary School (Madison, WI) | unit: RTU-1
  - model: VHP-048 (spoken: "V-H-P forty-eight") | serial on rating plate: 2108V00973
  - tech: Priya Raman (Ridgeline Mechanical Services) | agent: Alicia (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the A version of the defrost sensor drifts low after about two years"
    - "part number V-P-N forty-four seventy-one B"
    - "the B version supersedes the A version"
- **C03** — Compressor hums but will not start
  - date: 2025-06-03 | site: Elm & 3rd Retail Plaza (Waukesha, WI) | unit: CU-1
  - model: VCU-036 (spoken: "V-C-U thirty-six") | serial on rating plate: 2410V01510
  - tech: Luis Herrera (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the only approved hard start kit is the V-H-S thirty-five"
    - "a generic kit with a start capacitor over two hundred microfarads voids the compressor warranty"
- **C04** — Second stage of cooling never energizes
  - date: 2025-08-11 | site: Harbor Point Distribution Center (Kenosha, WI) | unit: RTU-2
  - model: VRL-120 (spoken: "V-R-L one-twenty") | serial on rating plate: 2329V01623
  - tech: Marcus Bell (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "factory stage delay is ten minutes"
    - "DIP switch four"
    - "turn DIP switch four on to cut it to three minutes"
- **C05** — Air handler blower runs constantly
  - date: 2025-02-27 | site: Riverside Public Library (Racine, WI) | unit: AH-1
  - model: VAH-036 (spoken: "V-A-H thirty-six") | serial on rating plate: 2152V00610
  - tech: Jen Kowalski (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the G relay on the V-A-B fifty board can weld closed"
    - "replacement board kit V-P-N fifty-five twenty"
    - "check for twenty-four volts at G with the thermostat off"
- **C06** — Flame rollout switch tripping
  - date: 2025-04-16 | site: Northgate Fitness Center (Golden, CO) | unit: RTU-1
  - model: VRT-048 (spoken: "V-R-T forty-eight") | serial on rating plate: 2324V01668
  - tech: Sam Okafor (Ridgeline Mechanical Services) | agent: Alicia (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "bird nests blocking the inducer venturi"
    - "common on the twenty twenty-two builds"
    - "inducer screen kit V-P-N thirty-three ten"
- **C07** — Auxiliary heat not coming on
  - date: 2025-12-09 | site: Lakeshore Medical Office Building (Milwaukee, WI) | unit: RTU-3
  - model: VHP-060 (spoken: "V-H-P sixty") | serial on rating plate: 2130V01192
  - tech: Dana Ortiz (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "only the fifteen kilowatt kit has a manual reset limit"
    - "it is behind access panel four"
- **C08** — Low-pressure trips while cooling a server room in winter
  - date: 2025-01-08 | site: Riverside Public Library (Racine, WI) | unit: CU-2
  - model: VCU-048 (spoken: "V-C-U forty-eight") | serial on rating plate: 2106V00057
  - tech: Jen Kowalski (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "you need the low ambient kit V-L-A two"
    - "it lets the unit cool down to zero degrees outside"
- **C09** — Economizer damper not modulating
  - date: 2025-05-20 | site: Harbor Point Distribution Center (Kenosha, WI) | unit: RTU-4
  - model: VRL-150 (spoken: "V-R-L one-fifty") | serial on rating plate: 2212V01255
  - tech: Marcus Bell (Ridgeline Mechanical Services) | agent: Tom (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the actuator needs a two to ten volt signal"
    - "the board ships in zero to ten volt mode"
    - "move jumper J-P seven"
- **C10** — Condensate overflow switch tripping with dry pan
  - date: 2025-06-30 | site: Elm & 3rd Retail Plaza (Waukesha, WI) | unit: RTU-1
  - model: VRT-036 (spoken: "V-R-T thirty-six") | serial on rating plate: 2412V01667
  - tech: Luis Herrera (Ridgeline Mechanical Services) | agent: Alicia (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "on the oh-three-six built before week forty of twenty twenty-two the float switch is mounted too low"
    - "relocation kit V-P-N twenty-two oh eight"
- **C11** — Compressor warranty question
  - date: 2025-03-04 | site: Northgate Fitness Center (Golden, CO) | unit: RTU-2
  - model: VRT-060 (spoken: "V-R-T sixty") | serial on rating plate: 2308V01127
  - tech: Sam Okafor (Ridgeline Mechanical Services) | agent: Megan (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "ten year compressor warranty if the unit is registered within sixty days"
    - "otherwise it is five years"
- **C12** — Heat pump heats when calling for cooling
  - date: 2025-10-21 | site: Brookhaven Elementary School (Madison, WI) | unit: RTU-2
  - model: VHP-036 (spoken: "V-H-P thirty-six") | serial on rating plate: 2435V00518
  - tech: Priya Raman (Ridgeline Mechanical Services) | agent: Raj (Vantorr Technical Support)
  - Phrases the AGENT must say, word for word (inside longer natural sentences is fine):
    - "the V-H-P energizes the reversing valve in heating"
    - "set the thermostat to B, not O"

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

Save your whole answer as `data/content/_raw/calls_part1.md`.
