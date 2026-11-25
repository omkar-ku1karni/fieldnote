"""Generate the 40 eval questions from world.json. Answers are computed, not written by an LLM.

15 image-only, 10 text, 8 audio, 7 multi-hop. Each question lists its gold evidence so retrieval
can be scored on its own, separate from the answer.

Run:  uv run python -m datagen.questions      -> eval/questions.yaml
"""
from __future__ import annotations

import json

import yaml

from datagen.world import thermistor_temp_f
from fieldnote.config import EVAL, SPEC


def liquid_target(cc: dict, t: float, s: float) -> float:
    return round(cc["L0"] + cc["kT"] * (t - 95) + cc["kS"] * (s - 125), 1)


def asset(world, site_id, unit):
    return next(a for a in world["assets"] if a["site_id"] == site_id and a["unit"] == unit)


def build(world: dict) -> list[dict]:
    M, S = world["models"], world["series"]
    q: list[dict] = []

    def add(qid, category, question, answer, evidence, **extra):
        q.append(dict(id=qid, category=category, question=question, answer=answer, evidence=evidence, **extra))

    num = lambda v, tol, unit: dict(type="numeric", value=v, tolerance=tol, unit=unit)  # noqa: E731
    txt = lambda canonical, *keywords: dict(type="keywords", canonical=canonical,  # noqa: E731
                                           must_include=[list(k) if isinstance(k, (list, tuple)) else [k] for k in keywords])
    fig = lambda fid: dict(modality="manual_figure", figure_id=fid)  # noqa: E731
    call = lambda cid: dict(modality="call", call_id=cid)  # noqa: E731
    text = lambda doc, find: dict(modality="manual_text", doc_id=doc, find=find)  # verbatim string on the gold page  # noqa: E731
    reg = lambda site, unit: dict(modality="register", site_id=site, unit=unit)  # noqa: E731
    photo = lambda pid: dict(modality="photo", photo_id=pid)  # noqa: E731
    bull = lambda bid: dict(modality="bulletin", bulletin_id=bid)  # noqa: E731

    # ---------------- 15 image-only (11 manual figures + 4 job photos)
    cc = M["VRT-060"]["figure_facts"]["charging_chart"]
    add("I01", "image_only", "On a VRT-060 it's 95 degrees outside and I'm reading 130 psig suction. What liquid "
        "pressure should I see if the charge is right?", num(liquid_target(cc, 95, 130), 8, "psig"), [fig("VRT-060-CC")])
    cc = M["VCU-036"]["figure_facts"]["charging_chart"]
    add("I02", "image_only", "VCU-036 condenser, 85°F ambient, suction is 120 psig. Target liquid pressure?",
        num(liquid_target(cc, 85, 120), 8, "psig"), [fig("VCU-036-CC")])
    cc = M["VRL-120"]["figure_facts"]["charging_chart"]
    add("I03", "image_only", "Charging a VRL-120 at 105°F outdoor with 135 psig suction — what liquid pressure am I "
        "aiming for?", num(liquid_target(cc, 105, 135), 8, "psig"), [fig("VRL-120-CC")])
    f = M["VRT-060"]["figure_facts"]
    add("I04", "image_only", "At what pressure does the high-pressure switch open on a VRT-060, and when does it close "
        "again?", txt(f"Opens at {f['hps_open_psig']} psig, closes at {f['hps_close_psig']} psig",
                      str(f["hps_open_psig"]), str(f["hps_close_psig"])), [fig("VRT-WD")])
    f = M["VHP-048"]["figure_facts"]
    add("I05", "image_only", "What are the MCA and max overcurrent protection for a VHP-048 on 208/230 three-phase?",
        txt(f"MCA {f['mca_a']} A, MOP {f['mop_a']} A", str(f["mca_a"]), str(f["mop_a"])), [fig("VHP-WD")])
    w = next(x for x in S["VRT"]["figure_facts"]["wiring"] if x["src"] == "Board HP1")
    add("I06", "image_only", "On the VRT control board, what color wire runs from terminal HP1 to the high-pressure "
        "switch?", txt(w["color"], w["color"].split("/")[0]), [fig("VRT-WD")])
    code = next(c for c in S["VRL"]["figure_facts"]["led_codes"] if c["condition"].startswith("Refrigerant leak"))
    add("I07", "image_only", f"VRL board LED is flashing {code['red']} red then {code['green']} green. What does that "
        "mean?", txt(code["condition"], ["leak"], ["refrigerant", "A2L"]), [fig("VRL-LED")])
    bt = M["VAH-036"]["figure_facts"]["blower_table"]
    add("I08", "image_only", "VAH-036 on the Med speed tap with 0.5 in. w.c. external static — about how much airflow?",
        num(bt["taps"]["Med"][bt["esp_in_wc"].index(0.5)], 40, "CFM"), [fig("VAH-036-BT")])
    th = S["VHP"]["figure_facts"]["thermistor"]
    add("I09", "image_only", "The VHP defrost sensor reads 20 kΩ with it unplugged. What temperature does that "
        "correspond to?", num(round(thermistor_temp_f(th["r25_kohm"], th["beta"], 20.0), 1), 3, "°F"), [fig("VHP-TH")])
    add("I10", "image_only", "A VRT going in at 5,200 feet elevation — how much do I need to derate the gas input?",
        num(16, 0, "%"), [fig("VRT-ALT")])
    rate = dict(S["VCU"]["figure_facts"]["lineset_adder_oz_per_ft"])['3/8"']
    std = S["VCU"]["figure_facts"]["lineset_standard_ft"]
    add("I11", "image_only", "VCU with a 50 ft line set and 3/8 inch liquid line. How much refrigerant do I add on top "
        "of the factory charge?", num(round((50 - std) * rate, 2), 0.6, "oz"), [fig("VCU-LS")])
    add("I12", "image_only", "What failed part did Dana photograph on Lakeshore Medical RTU-7 back in July?",
        txt("A failed capacitor — the top is blown out / bulged", "capacitor",
            ["swollen", "bulg", "domed", "bloated", "blown", "burst", "rupture", "exploded", "popped", "failed"]),
        [photo("P-LMOB-RTU7-01")])
    add("I13", "image_only", "Do we have any job photos of a heat pump coil that's completely iced over? Which site and "
        "unit?", txt("Brookhaven Elementary School, RTU-4", "Brookhaven", "RTU-4"), [photo("P-BES-RTU4-01")])
    add("I14", "image_only", "What did the condenser coil look like on Harbor Point RTU-4 at the May service call?",
        txt("Heavily clogged / matted with debris", ["clog", "debris", "dirt", "cottonwood", "matted", "plugged"]),
        [photo("P-HPDC-RTU4-01")])
    add("I15", "image_only", "Find me the photo of a burnt contactor — which site was it from?",
        txt("Northgate Fitness Center, RTU-3", "Northgate"), [photo("P-NFC-RTU3-01")])

    # ---------------- 10 text-only
    tf = lambda mid, k: M[mid]["text_facts"][k]  # noqa: E731
    add("T01", "text", "What's the factory refrigerant charge on a VRT-048?",
        txt(tf("VRT-048", "factory_charge"), tf("VRT-048", "factory_charge")), [text("VRT-IOM", tf("VRT-048", "factory_charge"))])
    add("T02", "text", "What defrost interval settings does the VHP support and what's the factory default?",
        txt(tf("VHP-048", "defrost_interval_options"), "30", "60", "90"), [text("VHP-IOM", tf("VHP-048", "defrost_interval_options"))])
    add("T03", "text", "What's the maximum line length and vertical lift for a VCU condensing unit?",
        txt("100 ft total, 40 ft vertical lift", "100", "40"), [text("VCU-IOM", "The maximum total refrigerant line length is 100 ft")])
    add("T04", "text", "How long do the crankcase heaters need to be on before first start-up on a VRL?",
        txt("At least 24 hours", "24"), [text("VRL-IOM", "Crankcase heaters must be energized at least 24 hours")])
    add("T05", "text", "When does a VAH air handler need a secondary drain pan?",
        txt("When installed above a finished ceiling", ["ceiling"]), [text("VAH-IOM", "A secondary drain pan is required")])
    add("T06", "text", "What filters does a VRT-060 take, and how many?",
        txt(tf("VRT-060", "filter"), "20 x 25 x 2", "3"), [text("VRT-IOM", tf("VRT-060", "filter"))])
    add("T07", "text", "Required clearances around a VHP-036?",
        txt(tf("VHP-036", "clearances_in"), "36", "24", "60"), [text("VHP-IOM", tf("VHP-036", "clearances_in"))])
    add("T08", "text", "After an A2L leak clears, how long does the unit stay in mitigation mode?",
        txt("At least 5 minutes after the reading clears", ["5", "five"]), [bull("SB-24-011")])
    add("T09", "text", "What's the replacement part number for the upgraded condenser fan capacitor on the VRT-060?",
        txt("VPN-0475 (5 µF / 440 VAC)", "0475"), [bull("SB-23-014")])
    add("T10", "text", "What's the minimum outdoor temperature a VRL can cool at without accessories?",
        txt(tf("VRL-120", "min_cooling_ambient_f"), "40"), [text("VRL-IOM", "40 °F")])

    # ---------------- 8 audio-only (support calls)
    add("A01", "audio", "VRL second stage takes forever to come on. Is there a way to shorten the stage delay?",
        txt("Factory delay is 10 minutes; turn DIP switch 4 ON to cut it to 3 minutes", ["dip"], ["4", "four"],
            ["3", "three"]), [call("C04")])
    add("A02", "audio", "What should the hot surface igniter on a VRT measure cold, and when do I replace it?",
        txt("40–75 ohms cold; replace above 100 ohms", ["40", "forty"], ["75", "seventy"], ["100", "hundred"]),
        [call("C16")])
    add("A03", "audio", "The VRL economizer damper won't modulate. Support said something about a jumper?",
        txt("Actuator needs 2–10 V; board ships in 0–10 V mode; move jumper JP7", ["jp7", "jp 7", "jp seven", "j-p seven"]),
        [call("C09")])
    add("A04", "audio", "What should the phase monitor unbalance trip be set to on the Harbor Point VRL-090?",
        txt("Factory 10%; support recommends 8% for that utility", ["8", "eight"]), [call("C13")])
    add("A05", "audio", "VAH blower wheel set screw keeps working loose — what torque?",
        txt("30 inch-pounds", ["30", "thirty"]), [call("C21")])
    add("A06", "audio", "Can I put a generic hard start kit on a VCU compressor?",
        txt("No — only the VHS-35 kit is approved; a generic kit over 200 µF voids the warranty",
            ["vhs-35", "vhs 35", "v-h-s thirty-five", "vhs35", "vhs-thirty-five"]), [call("C03")])
    add("A07", "audio", "How do I change the low-ambient compressor lockout on a VHP that's on a dual-fuel setup?",
        txt("DIP switches 2 and 3; factory 0°F; set 10°F for dual fuel", ["dip"], ["10", "ten"]), [call("C23")])
    add("A08", "audio", "Our VCU keeps tripping on low pressure cooling a server room in winter. What do we need?",
        txt("Low ambient kit VLA-2; allows cooling down to 0°F", ["vla-2", "vla 2", "v-l-a two", "vla2", "vla-two"]),
        [call("C08")])

    # ---------------- 7 multi-hop / cross-modal
    r7 = asset(world, "LMOB", "RTU-7")
    f60 = M["VRT-060"]["figure_facts"]
    add("H01", "multihop", "Lakeshore Medical RTU-7 keeps tripping on high pressure on hot afternoons. What's going on "
        "and what should I check?",
        dict(type="rubric", canonical=(
            f"RTU-7 is a VRT-060, serial {r7['serial']} (inside the SB-23-014 range) on firmware {r7['controller_firmware']}. "
            f"Likely causes: weak/swollen condenser fan capacitor (SB-23-014, replace with VPN-0475) and firmware 2.3 "
            f"lacking HPS debounce (update to 2.4.1). HPS opens at {f60['hps_open_psig']} psig."),
             points=["identifies the capacitor issue / SB-23-014 or VPN-0475",
                     "identifies the firmware 2.3 HPS debounce problem and the 2.4.1 fix",
                     f"states the HPS opens at {f60['hps_open_psig']} psig"]),
        [reg("LMOB", "RTU-7"), bull("SB-23-014"), call("C01"), fig("VRT-WD"), photo("P-LMOB-RTU7-01")])
    add("H02", "multihop", "How much do I derate the gas input on the rooftop units at Northgate Fitness Center?",
        dict(type="rubric", canonical="Northgate is at 5,280 ft (Golden, CO); VRT derate for 5,001–6,000 ft is 16%.",
             points=["uses Northgate's elevation (5,280 ft)", "answers 16%"]),
        [reg("NFC", "RTU-1"), fig("VRT-ALT")])
    add("H03", "multihop", "Brookhaven RTU-2 heats when the thermostat calls for cooling. The thermostat is set up for O. "
        "Why?", dict(type="rubric", canonical="RTU-2 is a VHP-036; the VHP energizes the reversing valve in heating, "
                     "so the thermostat must be set to B, not O.",
                     points=["identifies the unit as a VHP heat pump", "says to configure the thermostat for B (not O)"]),
        [reg("BES", "RTU-2"), call("C12"), fig("VHP-WD")])
    add("H04", "multihop", "What refrigerant is in Harbor Point RTU-4 and what's its factory charge?",
        dict(type="rubric", canonical=f"VRL-150, {M['VRL-150']['text_facts']['refrigerant']}, factory charge "
             f"{M['VRL-150']['text_facts']['factory_charge']}.",
             points=["R-454B", f"factory charge {M['VRL-150']['text_facts']['factory_charge']}"]),
        [reg("HPDC", "RTU-4"), text("VRL-IOM", M["VRL-150"]["text_facts"]["factory_charge"])])
    cc = M["VCU-024"]["figure_facts"]["charging_chart"]
    add("H05", "multihop", "Checking charge on the condensing unit at Lakeshore Medical: 85°F outside, 118 psig suction. "
        "Where should liquid pressure be?",
        dict(type="numeric", value=liquid_target(cc, 85, 118), tolerance=8, unit="psig"),
        [reg("LMOB", "CU-1"), fig("VCU-024-CC")])
    add("H06", "multihop", "The air handler at Riverside Library won't shut the blower off. What part do I order?",
        dict(type="rubric", canonical="AH-1 is a VAH-036; the VAB-50 G relay welds closed — order board kit VPN-5520 "
             "(confirm 24 V at G with the thermostat off).",
             points=["identifies welded G relay on the VAB-50 board", "VPN-5520"]),
        [reg("RPL", "AH-1"), call("C05")])
    add("H07", "multihop", "Elm & 3rd RTU-5 lost the compressor on circuit 2. What's the part, lead time, and can I keep "
        "the unit running meanwhile?",
        dict(type="rubric", canonical="RTU-5 is a VRL-150. Compressor VCP-150T, ~3 week lead time; disable circuit 2 "
             "with DIP switch 6 and run on circuit 1.",
             points=["VCP-150T", "about 3 weeks", "DIP switch 6 to run on circuit 1"]),
        [reg("E3RP", "RTU-5"), call("C24")])
    return q


def main() -> None:
    world = json.loads((SPEC / "world.json").read_text())
    qs = build(world)
    cats = {c: sum(x["category"] == c for x in qs) for c in ("image_only", "text", "audio", "multihop")}
    assert len(qs) == 40 and cats == dict(image_only=15, text=10, audio=8, multihop=7), cats
    EVAL.mkdir(exist_ok=True)
    header = ("# Fieldnote eval set — generated by datagen/questions.py from data/spec/world.json.\n"
              "# Answers are computed from the seeded spec. Review each item; set reviewed: true when checked.\n")
    for x in qs:
        x["reviewed"] = False
    (EVAL / "questions.yaml").write_text(header + yaml.safe_dump(qs, sort_keys=False, allow_unicode=True, width=110))
    print(f"wrote {EVAL / 'questions.yaml'}: {cats}")


if __name__ == "__main__":
    main()
