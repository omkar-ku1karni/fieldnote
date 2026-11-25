"""The seeded world spec everything else is generated from.

Every value an eval question depends on is made here with a fixed seed, so the answers never
come from an LLM. There are three kinds of facts and they never mix:

  text_facts   can appear in manual prose (the LLM is told to copy them exactly)
  figure data  only ever drawn into images (the LLM never sees these values)
  call facts   only ever spoken in the support-call audio

Run:  uv run python -m datagen.world
"""
from __future__ import annotations

import json
import math
import random

from fieldnote.config import SPEC

SEED = 20261122
MANUFACTURER = "Vantorr Climate Systems"
CONTRACTOR = "Ridgeline Mechanical Services"

SERIES = {
    "VRT": dict(
        title="VRT Series Packaged Rooftop Unit — Gas Heat / Electric Cooling",
        kind="rtu_gas", refrigerant="R-454B", sizes=[36, 48, 60], board="VCB-200",
        compressor="single-stage scroll",
    ),
    "VHP": dict(
        title="VHP Series Packaged Rooftop Heat Pump",
        kind="rtu_hp", refrigerant="R-454B", sizes=[36, 48, 60], board="VCB-210",
        compressor="single-stage scroll",
    ),
    "VCU": dict(
        title="VCU Series Split-System Condensing Unit",
        kind="condenser", refrigerant="R-410A", sizes=[24, 36, 48], board="VCB-110",
        compressor="single-stage scroll",
    ),
    "VAH": dict(
        title="VAH Series Multi-Position Air Handler",
        kind="air_handler", refrigerant="R-410A", sizes=[24, 36, 48], board="VAB-50",
        compressor=None,
    ),
    "VRL": dict(
        title="VRL Series Large Packaged Rooftop Unit — Two-Stage Cooling",
        kind="rtu_large", refrigerant="R-454B", sizes=[90, 120, 150], board="VCB-400",
        compressor="two tandem scroll compressors on two independent circuits",
    ),
}

# ---------------------------------------------------------------- helpers

def r5(x: float) -> int:
    return int(5 * round(x / 5))


def model_id(series: str, size: int) -> str:
    return f"{series}-{size:03d}"


# ---------------------------------------------------------------- text facts (allowed in prose)

def text_facts(rng: random.Random, series: str, size: int) -> dict:
    s = SERIES[series]
    tons = size / 12
    f: dict = {
        "nominal_tons": f"{tons:g}",
        "refrigerant": s["refrigerant"],
    }
    if s["kind"] != "air_handler":
        f["cooling_capacity_btuh"] = f"{int(round(size * 1000 * rng.uniform(0.965, 0.995), -2)):,}"
        oz_total = int(size * rng.uniform(1.55, 1.85))  # oz per kBtuh-ish
        f["factory_charge"] = f"{oz_total // 16} lb {oz_total % 16} oz"
        f["min_cooling_ambient_f"] = "35 °F" if series != "VRL" else "40 °F"
        f["anti_short_cycle_delay"] = "5 minutes"
    filt = {
        24: ("16 x 20 x 1 in.", 1), 36: ("16 x 25 x 2 in.", 2), 48: ("20 x 25 x 2 in.", 2),
        60: ("20 x 25 x 2 in.", 3), 90: ("20 x 25 x 2 in.", 4), 120: ("24 x 24 x 2 in.", 4),
        150: ("24 x 24 x 2 in.", 6),
    }[size]
    if series != "VCU":  # condensing unit has no filter
        f["filter"] = f"{filt[1]} filter{'s' if filt[1] > 1 else ''}, {filt[0]}"
    base_wt = {"VRT": 9.6, "VHP": 9.9, "VCU": 4.1, "VAH": 2.6, "VRL": 11.8}[series]
    f["operating_weight_lb"] = f"{int(round(size * base_wt * rng.uniform(0.95, 1.05), -1))} lb"
    f["clearances_in"] = {
        "VRT": "service side 36 in., condenser coil side 18 in., top 60 in. unobstructed",
        "VHP": "service side 36 in., coil side 24 in., top 60 in. unobstructed",
        "VCU": "service side 24 in., other sides 12 in., top 60 in. unobstructed",
        "VAH": "front service access 24 in.; zero clearance to combustibles on sides",
        "VRL": "service side 48 in., condenser side 36 in., top 72 in. unobstructed",
    }[series]
    f["voltage_options"] = "208/230-1-60, 208/230-3-60" if size <= 48 else "208/230-3-60, 460-3-60"
    if series == "VHP":
        f["defrost_interval_options"] = "30, 60 or 90 minutes (factory default 60 minutes)"
    if series == "VRT":
        f["heating_input_btuh"] = f"{ {36: 60000, 48: 80000, 60: 100000}[size]:,}"
    if series == "VRL":
        f["stages"] = "two stages of cooling (circuit 1 = Y1, circuit 2 = Y2)"
    return f


SERIES_TEXT_FACTS = {
    "VRT": ["Filters should be inspected monthly during the cooling season and replaced at least every 3 months.",
            "The condenser coil must be cleaned at least once a year.",
            "The unit is not approved for installation on roofs with a slope greater than 1/4 in. per foot unless a level curb is used."],
    "VHP": ["The unit must be level within 1/4 in. side to side so the condensate and defrost water drain correctly.",
            "Auxiliary electric heat kits are available in 5, 10 and 15 kW sizes."],
    "VCU": ["The maximum total refrigerant line length is 100 ft, with a maximum vertical lift of 40 ft.",
            "Factory charge covers the standard line set length of 25 ft."],
    "VAH": ["The air handler can be installed upflow, downflow, horizontal left or horizontal right.",
            "A secondary drain pan is required when the unit is installed above a finished ceiling."],
    "VRL": ["Crankcase heaters must be energized at least 24 hours before the first start-up.",
            "Economizer operation is controlled by a dry-bulb changeover setpoint that is field adjustable."],
}

# ---------------------------------------------------------------- figure-only data

LED_CONDITIONS = [
    ("High-pressure switch open", "Check condenser airflow, fan motor and capacitor; verify charge"),
    ("Low-pressure switch open", "Check for loss of charge, restricted filter-drier or low indoor airflow"),
    ("Outdoor ambient sensor open/short", "Check sensor wiring and resistance against the sensor curve"),
    ("Five-strike lockout (repeated pressure trips)", "Correct root cause, then cycle power to reset"),
    ("Refrigerant detection sensor fault", "Replace refrigerant detection sensor; blower runs in mitigation mode"),
    ("Refrigerant leak detected (A2L mitigation active)", "Ventilate area, locate and repair leak before restart"),
    ("Compressor contactor feedback fault", "Inspect contactor contacts and coil; check 24 V at Y"),
    ("Indoor blower proving fault", "Check blower motor, belt or wheel and airflow switch"),
    ("Flame rollout switch open", "Inspect inducer, vent and heat exchanger before resetting rollout switch"),
    ("Ignition lockout (3 failed trials)", "Check gas supply, igniter and flame sensor"),
    ("Freeze protection (indoor coil below 30 °F)", "Check airflow, filters and charge"),
    ("Phase loss or reversal", "Check incoming three-phase power and rotation"),
    ("Discharge temperature limit", "Check charge and expansion device; compressor may be overheating"),
    ("Communication loss with thermostat", "Check thermostat wiring and terminal connections"),
]

SERIES_LED_FAULTS = {  # which conditions each board family reports
    "VRT": [0, 1, 2, 3, 4, 5, 6, 8, 9, 10],
    "VHP": [0, 1, 2, 3, 4, 5, 6, 10, 11, 13],
    "VCU": [0, 1, 2, 3, 6, 11, 12],
    "VAH": [4, 5, 7, 10, 13],
    "VRL": [0, 1, 2, 3, 4, 5, 6, 7, 11, 12],
}

WIRE_COLORS = ["VIO", "BLU", "YEL", "ORG", "BRN", "GRY", "PNK", "WHT/BLK", "YEL/BLK", "BLU/WHT", "RED/WHT", "BLK"]

SERIES_WIRING = {  # (from terminal, to device terminal)
    "VRT": [("Board HP1", "HPS-1"), ("Board HP2", "HPS-2"), ("Board LP1", "LPS-1"), ("Board LP2", "LPS-2"),
            ("Board Y-OUT", "Contactor A1"), ("Board CF", "Cond. fan relay"), ("Board IND", "Inducer motor"),
            ("Board GV", "Gas valve MV"), ("Board HSI", "Igniter"), ("Board RS", "Rollout switch"),
            ("Board FS", "Flame sensor"), ("Board RDS", "Refrig. detection sensor")],
    "VHP": [("Board HP1", "HPS-1"), ("Board HP2", "HPS-2"), ("Board LP1", "LPS-1"), ("Board LP2", "LPS-2"),
            ("Board Y-OUT", "Contactor A1"), ("Board CF", "Cond. fan relay"), ("Board RV", "Reversing valve (B)"),
            ("Board DFT", "Defrost sensor"), ("Board OAT", "Outdoor air sensor"), ("Board W2-OUT", "Heat kit relay"),
            ("Board RDS", "Refrig. detection sensor")],
    "VCU": [("Board HP1", "HPS-1"), ("Board HP2", "HPS-2"), ("Board LP1", "LPS-1"), ("Board LP2", "LPS-2"),
            ("Board Y-OUT", "Contactor A1"), ("Board CF", "Cond. fan motor"), ("Board OAT", "Outdoor air sensor"),
            ("Board DT", "Discharge temp sensor")],
    "VAH": [("Board G", "Blower relay"), ("Board W1", "Heat seq. 1"), ("Board W2", "Heat seq. 2"),
            ("Board FS", "Float switch"), ("Board RDS", "Refrig. detection sensor"), ("Board EEV", "Expansion valve")],
    "VRL": [("Board HP1-A", "HPS circuit 1"), ("Board HP1-B", "HPS circuit 2"), ("Board LP1-A", "LPS circuit 1"),
            ("Board LP1-B", "LPS circuit 2"), ("Board Y1-OUT", "Contactor C1"), ("Board Y2-OUT", "Contactor C2"),
            ("Board PM", "Phase monitor"), ("Board ECON", "Economizer actuator"), ("Board CF1", "Cond. fan 1"),
            ("Board CF2", "Cond. fan 2"), ("Board RDS", "Refrig. detection sensor")],
}

ALTITUDE_DERATE = [  # VRT gas input derate bands (figure only)
    ("0 – 2,000", 0), ("2,001 – 3,000", 6), ("3,001 – 4,000", 9), ("4,001 – 5,000", 13),
    ("5,001 – 6,000", 16), ("6,001 – 7,000", 20), ("7,001 – 8,000", 23),
]

LINESET_ADDER = [  # VCU additional charge per ft beyond 25 ft (figure only)
    ('1/4"', 0.31), ('5/16"', 0.47), ('3/8"', 0.71), ('1/2"', 1.26),
]

THERMISTORS = {  # series -> (sensor name, R25 kOhm, beta)
    "VHP": ("Defrost / outdoor coil sensor", 15.0, 3720),
    "VCU": ("Outdoor air sensor", 10.0, 3560),
}


def thermistor_r_kohm(r25: float, beta: float, temp_f: float) -> float:
    t_k = (temp_f - 32) * 5 / 9 + 273.15
    return r25 * math.exp(beta * (1 / t_k - 1 / 298.15))


def thermistor_temp_f(r25: float, beta: float, r_kohm: float) -> float:
    inv_t = 1 / 298.15 + math.log(r_kohm / r25) / beta
    return (1 / inv_t - 273.15) * 9 / 5 + 32


def figure_facts(rng: random.Random, series: str, size: int) -> dict:
    s = SERIES[series]
    f: dict = {}
    if s["kind"] != "air_handler":
        # charging chart: liquid psig = L0 + kT*(T-95) + kS*(suction-125)
        base = 395 if s["refrigerant"] == "R-454B" else 385
        f["charging_chart"] = dict(
            L0=round(base + rng.uniform(-18, 18), 1),
            kT=round(rng.uniform(2.6, 3.3), 3),
            kS=round(rng.uniform(0.55, 1.0), 3),
            outdoor_temps_f=[65, 75, 85, 95, 105, 115],
            suction_range=[100, 160],
        )
        f["hps_open_psig"] = r5(rng.uniform(600, 650))
        f["hps_close_psig"] = r5(f["hps_open_psig"] - rng.uniform(160, 210))
        f["lps_open_psig"] = r5(rng.uniform(40, 60))
        f["lps_close_psig"] = r5(f["lps_open_psig"] + rng.uniform(35, 55))
    amps = size * rng.uniform(0.62, 0.72)
    f["mca_a"] = round(amps, 1)
    f["mop_a"] = min((x for x in (15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125) if x >= amps * 1.6),
                     default=125)
    if series in ("VRT", "VHP", "VRL", "VAH"):
        nominal = size * 400 / 12
        taps = ["Low", "Med-Low", "Med", "Med-High", "High"]
        tap_factor = [0.72, 0.84, 0.95, 1.06, 1.17]
        k = rng.uniform(0.33, 0.45)
        esp = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        f["blower_table"] = dict(
            esp_in_wc=esp,
            taps={t: [int(round(nominal * tf * (1 - k * e ** 1.4) / 5) * 5) for e in esp]
                  for t, tf in zip(taps, tap_factor)},
        )
    return f


def series_figure_facts(rng: random.Random, series: str) -> dict:
    f: dict = {}
    # LED flash codes: unique (red, green) combos
    combos = [(r, g) for r in range(1, 7) for g in range(0, 4)]
    rng.shuffle(combos)
    f["led_codes"] = [
        dict(red=r, green=g, condition=LED_CONDITIONS[i][0], action=LED_CONDITIONS[i][1])
        for (r, g), i in zip(combos, SERIES_LED_FAULTS[series])
    ]
    f["led_codes"].sort(key=lambda d: (d["red"], d["green"]))
    colors = WIRE_COLORS[:]
    rng.shuffle(colors)
    f["wiring"] = [dict(src=a, dst=b, color=colors[i % len(colors)]) for i, (a, b) in enumerate(SERIES_WIRING[series])]
    f["control_fuse_a"] = rng.choice([3, 5])
    if series == "VRT":
        f["altitude_derate"] = ALTITUDE_DERATE
    if series == "VCU":
        f["lineset_adder_oz_per_ft"] = LINESET_ADDER
        f["lineset_standard_ft"] = 25
    if series in THERMISTORS:
        name, r25, beta = THERMISTORS[series]
        f["thermistor"] = dict(name=name, r25_kohm=r25, beta=beta)
    return f


# ---------------------------------------------------------------- sites / asset register (text)

SITES = [
    dict(id="LMOB", name="Lakeshore Medical Office Building", city="Milwaukee, WI", elevation_ft=620),
    dict(id="BES", name="Brookhaven Elementary School", city="Madison, WI", elevation_ft=860),
    dict(id="HPDC", name="Harbor Point Distribution Center", city="Kenosha, WI", elevation_ft=610),
    dict(id="E3RP", name="Elm & 3rd Retail Plaza", city="Waukesha, WI", elevation_ft=820),
    dict(id="RPL", name="Riverside Public Library", city="Racine, WI", elevation_ft=630),
    dict(id="NFC", name="Northgate Fitness Center", city="Golden, CO", elevation_ft=5280),
]

# unit -> (series, size, serial, firmware). Hand-placed so multi-hop questions are coherent.
ASSETS = {
    "LMOB": [("RTU-1", "VRT", 48), ("RTU-2", "VRT", 48), ("RTU-3", "VHP", 60), ("RTU-4", "VRT", 60),
             ("RTU-5", "VRT", 60), ("RTU-6", "VHP", 48), ("RTU-7", "VRT", 60), ("CU-1", "VCU", 24),
             ("AH-1", "VAH", 24)],
    "BES": [("RTU-1", "VHP", 48), ("RTU-2", "VHP", 36), ("RTU-3", "VRT", 48), ("RTU-4", "VHP", 48),
            ("AH-1", "VAH", 24), ("CU-1", "VCU", 24)],
    "HPDC": [("RTU-1", "VRL", 90), ("RTU-2", "VRL", 120), ("RTU-3", "VRL", 120), ("RTU-4", "VRL", 150),
             ("RTU-5", "VHP", 60)],
    "E3RP": [("RTU-1", "VRT", 36), ("RTU-2", "VRT", 36), ("RTU-3", "VHP", 48), ("RTU-4", "VRT", 48),
             ("RTU-5", "VRL", 150), ("CU-1", "VCU", 36)],
    "RPL": [("RTU-1", "VRL", 120), ("AH-1", "VAH", 36), ("CU-1", "VCU", 36), ("CU-2", "VCU", 48)],
    "NFC": [("RTU-1", "VRT", 48), ("RTU-2", "VRT", 60), ("RTU-3", "VRT", 36), ("RTU-4", "VAH", 48)],
}
# Pinned serials/firmware for units that eval questions hinge on.
PINNED = {
    ("LMOB", "RTU-7"): ("2310V00412", "2.3"),
    ("LMOB", "RTU-4"): ("2304V00188", "2.4.1"),
    ("LMOB", "RTU-5"): ("2314V00733", "2.4.1"),
    ("NFC", "RTU-2"): ("2308V01127", "2.3"),
}


def build_assets(rng: random.Random) -> list[dict]:
    out = []
    for site in SITES:
        for unit, series, size in ASSETS[site["id"]]:
            yy = rng.choice([21, 22, 23, 24])
            ww = rng.randint(1, 52)
            serial = f"{yy}{ww:02d}V{rng.randint(10, 1999):05d}"
            fw = rng.choice(["2.2", "2.3", "2.4.1"]) if series in ("VRT", "VHP") else rng.choice(["1.8", "1.9"])
            # keep the capacitor-bulletin serial range (2307V–2312V, VRT-060) exclusive to pinned units
            if series == "VRT" and size == 60 and (site["id"], unit) not in PINNED:
                serial = f"24{ww:02d}V{rng.randint(10, 1999):05d}"
            serial, fw = PINNED.get((site["id"], unit), (serial, fw))
            out.append(dict(site_id=site["id"], site=site["name"], unit=unit, model=model_id(series, size),
                            serial=serial, controller_firmware=fw,
                            installed=f"20{serial[:2]}-{min(12, max(1, int(serial[2:4]) // 4 + 1)):02d}"))
    return out


# ---------------------------------------------------------------- service bulletins (text; LLM writes prose)

BULLETINS = [
    dict(id="SB-23-014", date="2023-11-06", title="VRT-060 condenser fan motor run capacitor — early failures",
         applies_to="VRT-060 units with serial numbers 2307V00001 through 2312V99999",
         facts=["Original condenser fan run capacitor is rated 5 µF / 370 VAC and can swell and lose capacitance after one to two cooling seasons.",
                "Replace with upgraded capacitor part number VPN-0475 (5 µF / 440 VAC).",
                "A weak capacitor reduces condenser fan speed, which raises head pressure on hot days and can cause high-pressure switch trips.",
                "Warranty labor allowance: 0.5 hours."]),
    dict(id="SB-24-003", date="2024-03-18", title="VRL-150 condenser fan blade inspection",
         applies_to="VRL-150 units built in 2023",
         facts=["Inspect condenser fan blades for hairline cracks at the hub during every spring start-up.",
                "Replace cracked blades with fan blade kit VPN-6120; torque hub set screws to 160 in-lb.",
                "Do not operate the unit with a cracked blade."]),
    dict(id="SB-24-011", date="2024-09-02", title="A2L refrigerant detection system — field service guidance",
         applies_to="All R-454B units (VRT, VHP, VRL)",
         facts=["When the refrigerant detection sensor senses a leak, the board shuts off the compressor and runs the indoor blower continuously (mitigation mode).",
                "Mitigation mode continues for at least 5 minutes after the sensor reading clears.",
                "Never bypass or jumper the refrigerant detection sensor."]),
]

# ---------------------------------------------------------------- support calls (audio-only facts)

TECHS = ["Dana Ortiz", "Marcus Bell", "Priya Raman", "Luis Herrera", "Jen Kowalski", "Sam Okafor"]
AGENTS = ["Tom", "Alicia", "Raj", "Megan"]

CALLS = [
    dict(id="C01", site="LMOB", unit="RTU-7", tech="Dana Ortiz", agent="Tom", date="2025-07-14",
         topic="Repeated high-pressure lockouts on hot afternoons",
         must_say=["firmware two point three", "no debounce on the high-pressure switch input",
                   "locks out hard after three trips in one hour", "fixed in firmware two point four point one",
                   "update it with the service app over the USB-C port", "check the condenser fan capacitor"]),
    dict(id="C02", site="BES", unit="RTU-1", tech="Priya Raman", agent="Alicia", date="2025-01-22",
         topic="Heat pump defrost not terminating",
         must_say=["the A version of the defrost sensor drifts low after about two years",
                   "part number V-P-N forty-four seventy-one B", "the B version supersedes the A version"]),
    dict(id="C03", site="E3RP", unit="CU-1", tech="Luis Herrera", agent="Raj", date="2025-06-03",
         topic="Compressor hums but will not start",
         must_say=["the only approved hard start kit is the V-H-S thirty-five",
                   "a generic kit with a start capacitor over two hundred microfarads voids the compressor warranty"]),
    dict(id="C04", site="HPDC", unit="RTU-2", tech="Marcus Bell", agent="Megan", date="2025-08-11",
         topic="Second stage of cooling never energizes",
         must_say=["factory stage delay is ten minutes", "DIP switch four", "turn DIP switch four on to cut it to three minutes"]),
    dict(id="C05", site="RPL", unit="AH-1", tech="Jen Kowalski", agent="Tom", date="2025-02-27",
         topic="Air handler blower runs constantly",
         must_say=["the G relay on the V-A-B fifty board can weld closed",
                   "replacement board kit V-P-N fifty-five twenty", "check for twenty-four volts at G with the thermostat off"]),
    dict(id="C06", site="NFC", unit="RTU-1", tech="Sam Okafor", agent="Alicia", date="2025-04-16",
         topic="Flame rollout switch tripping",
         must_say=["bird nests blocking the inducer venturi", "common on the twenty twenty-two builds",
                   "inducer screen kit V-P-N thirty-three ten"]),
    dict(id="C07", site="LMOB", unit="RTU-3", tech="Dana Ortiz", agent="Raj", date="2025-12-09",
         topic="Auxiliary heat not coming on",
         must_say=["only the fifteen kilowatt kit has a manual reset limit",
                   "it is behind access panel four"]),
    dict(id="C08", site="RPL", unit="CU-2", tech="Jen Kowalski", agent="Megan", date="2025-01-08",
         topic="Low-pressure trips while cooling a server room in winter",
         must_say=["you need the low ambient kit V-L-A two", "it lets the unit cool down to zero degrees outside"]),
    dict(id="C09", site="HPDC", unit="RTU-4", tech="Marcus Bell", agent="Tom", date="2025-05-20",
         topic="Economizer damper not modulating",
         must_say=["the actuator needs a two to ten volt signal", "the board ships in zero to ten volt mode",
                   "move jumper J-P seven"]),
    dict(id="C10", site="E3RP", unit="RTU-1", tech="Luis Herrera", agent="Alicia", date="2025-06-30",
         topic="Condensate overflow switch tripping with dry pan",
         must_say=["on the oh-three-six built before week forty of twenty twenty-two the float switch is mounted too low",
                   "relocation kit V-P-N twenty-two oh eight"]),
    dict(id="C11", site="NFC", unit="RTU-2", tech="Sam Okafor", agent="Megan", date="2025-03-04",
         topic="Compressor warranty question",
         must_say=["ten year compressor warranty if the unit is registered within sixty days",
                   "otherwise it is five years"]),
    dict(id="C12", site="BES", unit="RTU-2", tech="Priya Raman", agent="Raj", date="2025-10-21",
         topic="Heat pump heats when calling for cooling",
         must_say=["the V-H-P energizes the reversing valve in heating", "set the thermostat to B, not O"]),
    dict(id="C13", site="HPDC", unit="RTU-1", tech="Marcus Bell", agent="Alicia", date="2025-07-02",
         topic="Phase monitor nuisance trips",
         must_say=["factory unbalance trip is ten percent", "the dial goes from five to fifteen percent",
                   "set it to eight percent on that utility"]),
    dict(id="C14", site="LMOB", unit="CU-1", tech="Dana Ortiz", agent="Megan", date="2025-05-12",
         topic="Pairing a condenser with an air handler — metering device",
         must_say=["the V-C-U oh-two-four ships with a fixed orifice", "with the V-A-H oh-two-four you install TXV kit V-T-X two",
                   "remove the fixed orifice"]),
    dict(id="C15", site="NFC", unit="RTU-4", tech="Sam Okafor", agent="Tom", date="2025-11-18",
         topic="Electric heat staging timing",
         must_say=["the V-A-B fifty board stages the heat strips thirty seconds apart"]),
    dict(id="C16", site="BES", unit="RTU-3", tech="Priya Raman", agent="Megan", date="2025-11-03",
         topic="Gas valve has 24 volts but no flame",
         must_say=["igniter part V-P-N eleven ninety", "forty to seventy-five ohms cold", "over a hundred ohms replace it"]),
    dict(id="C17", site="E3RP", unit="RTU-3", tech="Luis Herrera", agent="Raj", date="2025-12-15",
         topic="Defrost interval for a snowy site",
         must_say=["in heavy snow we recommend thirty minutes instead of the default sixty"]),
    dict(id="C18", site="RPL", unit="RTU-1", tech="Jen Kowalski", agent="Alicia", date="2025-02-10",
         topic="Unit will not start after a winter power outage",
         must_say=["the V-C-B four hundred board enforces a four hour warm-up delay",
                   "after a cold power-up below fifty degrees outside"]),
    dict(id="C19", site="LMOB", unit="RTU-7", tech="Dana Ortiz", agent="Tom", date="2025-07-22",
         topic="Follow-up after firmware update and capacitor replacement",
         must_say=["running fine since the update and the new capacitor",
                   "high-pressure trips now show up as event code E forty-one in the history log"]),
    dict(id="C20", site="RPL", unit="CU-1", tech="Jen Kowalski", agent="Raj", date="2025-09-09",
         topic="Slow refrigerant leak search",
         must_say=["known leak point at the liquid service valve braze joint on the twenty twenty-one builds"]),
    dict(id="C21", site="BES", unit="AH-1", tech="Priya Raman", agent="Tom", date="2025-03-25",
         topic="Rattling noise from air handler",
         must_say=["blower wheel set screw works loose", "torque it to thirty inch-pounds"]),
    dict(id="C22", site="NFC", unit="RTU-3", tech="Sam Okafor", agent="Raj", date="2025-08-27",
         topic="Refrigerant detection sensor fault, blower will not shut off",
         must_say=["the R-D-S one sensor has a five year service life",
                   "a sensor fault forces the blower on in mitigation mode"]),
    dict(id="C23", site="HPDC", unit="RTU-5", tech="Marcus Bell", agent="Megan", date="2025-12-01",
         topic="Heat pump compressor locked out in cold weather",
         must_say=["low ambient compressor lockout is zero degrees from the factory",
                   "DIP switches two and three", "with dual fuel set it to ten degrees"]),
    dict(id="C24", site="E3RP", unit="RTU-5", tech="Luis Herrera", agent="Tom", date="2025-10-07",
         topic="Failed compressor on circuit two — interim operation",
         must_say=["replacement compressor part V-C-P one-fifty-T", "about a three week lead time",
                   "disable circuit two with DIP switch six and run on circuit one"]),
]

# ---------------------------------------------------------------- job-site photo slots (image-only content)

PHOTO_SLOTS = [
    dict(id="P-LMOB-RTU7-01", site="LMOB", unit="RTU-7", job="J-25-0714", date="2025-07-14", tech="Dana Ortiz",
         must_show="a failed cylindrical capacitor with a ruptured / bulged top, still in its enclosure",
         label="failed capacitor with a blown, bulged top"),
    dict(id="P-HPDC-RTU4-01", site="HPDC", unit="RTU-4", job="J-25-0520", date="2025-05-20", tech="Marcus Bell",
         must_show="a condenser coil heavily clogged with debris, cottonwood or dirt",
         label="clogged condenser coil"),
    dict(id="P-BES-RTU4-01", site="BES", unit="RTU-4", job="J-25-0203", date="2025-02-03", tech="Priya Raman",
         must_show="an outdoor heat pump coil covered in ice",
         label="iced-over outdoor coil"),
    dict(id="P-NFC-RTU3-01", site="NFC", unit="RTU-3", job="J-25-0827", date="2025-08-27", tech="Sam Okafor",
         must_show="a burnt / pitted contactor or a burnt wire terminal",
         label="burnt contactor"),
]


def build_world() -> dict:
    rng = random.Random(SEED)
    models = {}
    for series, s in SERIES.items():
        for size in s["sizes"]:
            mid = model_id(series, size)
            models[mid] = dict(series=series, size=size, text_facts=text_facts(rng, series, size),
                               figure_facts=figure_facts(rng, series, size))
    series_out = {}
    for series, s in SERIES.items():
        series_out[series] = dict(**s, text_facts=SERIES_TEXT_FACTS[series],
                                  figure_facts=series_figure_facts(rng, series))
    return dict(
        seed=SEED, manufacturer=MANUFACTURER, contractor=CONTRACTOR,
        series=series_out, models=models, sites=SITES, assets=build_assets(rng),
        bulletins=BULLETINS, techs=TECHS, agents=AGENTS, calls=CALLS, photo_slots=PHOTO_SLOTS,
    )


def main() -> None:
    SPEC.mkdir(parents=True, exist_ok=True)
    world = build_world()
    (SPEC / "world.json").write_text(json.dumps(world, indent=2, ensure_ascii=False))
    print(f"wrote {SPEC / 'world.json'}: {len(world['models'])} models, {len(world['assets'])} assets, "
          f"{len(world['calls'])} calls")


if __name__ == "__main__":
    main()
