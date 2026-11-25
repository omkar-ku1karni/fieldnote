"""Draw the figure-only facts from world.json as manual-style figures.

The values in these images don't exist anywhere else: not in the PDF text layer and not in the
LLM-written prose. That's what makes the 15 image-only eval questions a fair test.

Run:  uv run python -m datagen.figures
"""
from __future__ import annotations

import io
import json
import math
import random
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

from datagen.world import thermistor_r_kohm  # noqa: E402
from fieldnote.config import FIGURES, SPEC  # noqa: E402

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.linewidth": 0.8,
    "axes.edgecolor": "#222", "axes.labelcolor": "#111", "xtick.color": "#111", "ytick.color": "#111",
})
DPI = 170
INK = "#1b1b1b"


def _save(fig, path, seed: int) -> None:
    """Save with light 'scanned manual' degradation: slight skew, blur, paper tint, noise."""
    buf = io.BytesIO()
    fig.savefig(buf, dpi=DPI, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    rng = random.Random(seed)
    img = Image.open(buf).convert("RGB")
    img = img.rotate(rng.uniform(-0.35, 0.35), resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(radius=0.35))
    arr = np.asarray(img).astype(np.float32)
    arr = arr * np.array([0.985, 0.975, 0.95]) + np.random.default_rng(seed).normal(0, 3.0, arr.shape)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path, quality=88, optimize=True)


def _title(ax, text):
    ax.set_title(text, fontsize=10.5, fontweight="bold", loc="left", pad=8)


# ------------------------------------------------------------------ per-model figures

def charging_chart(mid: str, m: dict, path, seed):
    cc = m["figure_facts"]["charging_chart"]
    s = np.linspace(*cc["suction_range"], 50)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    for t in cc["outdoor_temps_f"]:
        y = cc["L0"] + cc["kT"] * (t - 95) + cc["kS"] * (s - 125)
        ax.plot(s, y, color=INK, lw=1.3)
        ax.text(s[-1] + 0.8, y[-1], f"{t}°F", va="center", fontsize=8.5)
    ax.set_xlim(cc["suction_range"][0], cc["suction_range"][1] + 7)
    lo = cc["L0"] + cc["kT"] * (65 - 95) + cc["kS"] * (100 - 125)
    hi = cc["L0"] + cc["kT"] * (115 - 95) + cc["kS"] * (160 - 125)
    ax.set_ylim(10 * math.floor((lo - 15) / 10), 10 * math.ceil((hi + 15) / 10))
    ax.set_xticks(np.arange(100, 161, 5))
    ax.set_yticks(np.arange(*ax.get_ylim(), 20))
    ax.minorticks_on()
    ax.grid(which="major", color="#777", lw=0.6)
    ax.grid(which="minor", color="#bbb", lw=0.3, ls=":")
    ax.set_xlabel("Suction pressure at service valve (psig)")
    ax.set_ylabel("Liquid pressure at service valve (psig)")
    _title(ax, f"{mid}  Cooling Charging Chart  ({m['text_facts']['refrigerant']})")
    ax.text(0.01, -0.16, "Lines = outdoor ambient dry-bulb temperature entering condenser coil. "
            "Charge is correct when the measured\nliquid pressure is within ±8 psig of the chart value. "
            "Indoor airflow must be set per blower table before charging.",
            transform=ax.transAxes, fontsize=7.4, va="top")
    _save(fig, path, seed)


def blower_table(mid: str, m: dict, path, seed):
    bt = m["figure_facts"]["blower_table"]
    cols = [f"{e:.1f}" for e in bt["esp_in_wc"]]
    rows = [[t] + [f"{v:,}" for v in vals] for t, vals in bt["taps"].items()]
    fig, ax = plt.subplots(figsize=(7.4, 2.5))
    ax.axis("off")
    _title(ax, f"{mid}  Indoor Blower Performance — Airflow (CFM), dry coil with filter")
    tbl = ax.table(cellText=rows, colLabels=["Speed tap"] + cols, loc="center", cellLoc="center",
                   colWidths=[0.13] + [0.087] * len(cols))
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.45)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#444")
        if r == 0:
            cell.set_facecolor("#e4e4e4")
            cell.set_text_props(fontweight="bold")
    ax.text(0.5, -0.02, "External static pressure (in. w.c.) across top row.", ha="center",
            transform=ax.transAxes, fontsize=7.4)
    _save(fig, path, seed)


def blower_chart(mid: str, m: dict, path, seed):
    bt = m["figure_facts"]["blower_table"]
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    styles = ["-", "--", "-.", ":", (0, (5, 1))]
    for (tap, vals), ls in zip(bt["taps"].items(), styles):
        ax.plot(bt["esp_in_wc"], vals, color=INK, lw=1.4, ls=ls, marker="o", ms=3, label=tap)
    ax.set_xlabel("External static pressure (in. w.c.)")
    ax.set_ylabel("Airflow (CFM)")
    ax.set_xticks(np.arange(0.1, 1.01, 0.1))
    ax.minorticks_on()
    ax.grid(which="major", color="#777", lw=0.6)
    ax.grid(which="minor", color="#bbb", lw=0.3, ls=":")
    ax.legend(title="Speed tap", fontsize=8, frameon=True, edgecolor="#444")
    _title(ax, f"{mid}  Blower Performance Curves (dry coil, with filter)")
    _save(fig, path, seed)


# ------------------------------------------------------------------ per-series figures

def wiring_diagram(series: str, sd: dict, models: dict, path, seed):
    ff = sd["figure_facts"]
    wires = ff["wiring"]
    n = len(wires)
    fig, ax = plt.subplots(figsize=(7.6, 0.42 * n + 4.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(-34, 4 * n + 8)
    ax.axis("off")
    _title(ax, f"{series} Series  Control Wiring Diagram  ({sd['board']} control board)")
    top = 4 * n + 2
    ax.add_patch(FancyBboxPatch((3, 0), 22, top, boxstyle="round,pad=0.4", fc="#f2f2f2", ec=INK, lw=1.2))
    ax.text(14, top + 2.2, sd["board"], ha="center", fontweight="bold")
    for i, w in enumerate(wires):
        y = top - 3 - 4 * i
        term = w["src"].replace("Board ", "")
        ax.text(21.5, y, term, ha="right", va="center", fontsize=8)
        ax.add_patch(Circle((24, y), 0.7, fc="white", ec=INK, lw=1))
        ax.plot([24.7, 66], [y, y], color=INK, lw=1.1)
        ax.text(45, y + 0.9, w["color"], ha="center", fontsize=7.6,
                bbox=dict(fc="white", ec="none", pad=0.6))
        ax.add_patch(FancyBboxPatch((66, y - 1.4), 30, 2.8, boxstyle="round,pad=0.2", fc="white", ec=INK, lw=0.9))
        ax.text(81, y, w["dst"], ha="center", va="center", fontsize=8)
    # electrical data table
    rows = []
    for mid, m in models.items():
        f = m["figure_facts"]
        if "hps_open_psig" in f:
            rows.append([mid, f"{f['mca_a']}", f"{f['mop_a']}", f"{f['hps_open_psig']} / {f['hps_close_psig']}",
                         f"{f['lps_open_psig']} / {f['lps_close_psig']}"])
            labels = ["Model", "MCA (A)", "MOP (A)", "HPS open / close\n(psig)", "LPS open / close\n(psig)"]
        else:
            rows.append([mid, f"{f['mca_a']}", f"{f['mop_a']}"])
            labels = ["Model", "MCA (A)", "MOP (A)"]
    tbl = ax.table(cellText=rows, colLabels=labels, cellLoc="center", bbox=[0.03, 0.02, 0.94, 0.07 * (len(rows) + 1)])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#444")
        if r == 0:
            cell.set_facecolor("#e4e4e4")
            cell.set_height(cell.get_height() * 1.35)
    ax.text(3, -4, f"ELECTRICAL DATA — 208/230-3-60 (largest-voltage rating shown).  Control circuit fuse: "
            f"{ff['control_fuse_a']} A.\nWire color codes: VIO violet, BLU blue, YEL yellow, ORG orange, BRN brown, "
            "GRY gray, PNK pink, WHT white, BLK black, RED red.", fontsize=7.2, va="top")
    _save(fig, path, seed)


def led_table(series: str, sd: dict, path, seed):
    codes = sd["figure_facts"]["led_codes"]
    n = len(codes)
    fig, ax = plt.subplots(figsize=(7.6, 0.55 * n + 1.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.5, n + 1.4)
    ax.axis("off")
    _title(ax, f"{series} Series  {sd['board']} Status LED Flash Codes")
    hdr = n + 0.4
    for x, t in [(1, "Flash pattern"), (29, "Condition"), (60, "Service action")]:
        ax.text(x, hdr, t, fontweight="bold", fontsize=8.5, va="center")
    ax.plot([0, 100], [hdr - 0.45, hdr - 0.45], color=INK, lw=1)
    for i, c in enumerate(codes):
        y = n - 1 - i
        xs_r = [2 + 2.6 * k for k in range(c["red"])]
        xs_g = [xs_r[-1] + 4.2 + 2.6 * k for k in range(c["green"])]
        ax.scatter(xs_r, [y] * len(xs_r), s=55, c="#c62828", edgecolors=INK, linewidths=0.5, zorder=3)
        if xs_g:
            ax.scatter(xs_g, [y] * len(xs_g), s=55, c="#2e7d32", edgecolors=INK, linewidths=0.5, zorder=3)
        ax.text(29, y, textwrap.fill(c["condition"], 30), va="center", fontsize=7.4, linespacing=1.1)
        ax.text(60, y, textwrap.fill(c["action"], 46), va="center", fontsize=6.9, linespacing=1.1)
        ax.plot([0, 100], [y - 0.5, y - 0.5], color="#999", lw=0.4)
    ax.text(0, -1.2, "Red flashes are followed by a 1-second pause, then green flashes. Pattern repeats every 5 seconds. "
            "Solid green = normal standby.", fontsize=7.0)
    ax.set_aspect("auto")
    _save(fig, path, seed)


def thermistor_curve(series: str, sd: dict, path, seed):
    th = sd["figure_facts"]["thermistor"]
    t = np.linspace(-20, 120, 200)
    r = [thermistor_r_kohm(th["r25_kohm"], th["beta"], x) for x in t]
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.semilogy(t, r, color=INK, lw=1.5)
    ax.set_xlabel("Sensor temperature (°F)")
    ax.set_ylabel("Resistance (kΩ)")
    ax.set_xticks(np.arange(-20, 121, 10))
    ax.grid(which="major", color="#777", lw=0.6)
    ax.grid(which="minor", color="#bbb", lw=0.3, ls=":")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f"{v:g}" if str(v)[0] in "235" else ""))
    _title(ax, f"{series} Series  {th['name']} — Resistance vs. Temperature")
    ax.text(0.01, -0.13, "Measure with sensor disconnected from the board. Readings more than 10% off the curve "
            "indicate a failed sensor.", transform=ax.transAxes, fontsize=7.4, va="top")
    _save(fig, path, seed)


def altitude_derate(series: str, sd: dict, path, seed):
    bands = sd["figure_facts"]["altitude_derate"]
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    xs = np.arange(len(bands))
    ax.bar(xs, [b[1] for b in bands], color="#bdbdbd", edgecolor=INK, width=0.7)
    for x, (_, p) in zip(xs, bands):
        ax.text(x, p + 0.4, f"{p}%", ha="center", fontsize=8.5)
    ax.set_xticks(xs, [b[0] for b in bands], rotation=20, fontsize=7.8)
    ax.set_xlabel("Installation elevation (ft above sea level)")
    ax.set_ylabel("Required reduction in gas input (%)")
    ax.set_ylim(0, max(b[1] for b in bands) + 4)
    ax.grid(axis="y", color="#bbb", lw=0.4)
    _title(ax, f"{series} Series  High-Altitude Gas Input Derate")
    _save(fig, path, seed)


def lineset_adder(series: str, sd: dict, path, seed):
    rows = sd["figure_facts"]["lineset_adder_oz_per_ft"]
    std = sd["figure_facts"]["lineset_standard_ft"]
    fig, ax = plt.subplots(figsize=(6.2, 2.1))
    ax.axis("off")
    _title(ax, f"{series} Series  Additional Refrigerant for Long Line Sets")
    tbl = ax.table(cellText=[[d, f"{r:.2f}"] for d, r in rows],
                   colLabels=["Liquid line O.D.", "Additional charge (oz per ft)"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1, 1.4)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#444")
        if r == 0:
            cell.set_facecolor("#e4e4e4")
    ax.text(0.5, -0.05, f"Add charge only for line length beyond {std} ft (measured one way).", ha="center",
            transform=ax.transAxes, fontsize=7.6)
    _save(fig, path, seed)


FIGURE_TITLES = {
    "CC": "Cooling Charging Chart", "BT": "Indoor Blower Performance", "WD": "Control Wiring Diagram and Electrical Data",
    "LED": "Status LED Flash Codes", "TH": "Sensor Resistance vs. Temperature", "ALT": "High-Altitude Gas Input Derate",
    "LS": "Additional Refrigerant for Long Line Sets",
}


def render_all() -> list[dict]:
    world = json.loads((SPEC / "world.json").read_text())
    FIGURES.mkdir(parents=True, exist_ok=True)
    manifest = []
    seed = 1

    def add(fid, series, model, kind, fn, *args):
        nonlocal seed
        path = FIGURES / f"{fid}.jpg"
        fn(*args, path, seed)
        seed += 1
        title = f"{model or series + ' Series'} {FIGURE_TITLES[kind]}"
        manifest.append(dict(figure_id=fid, series=series, model=model, kind=kind, title=title, file=path.name))

    for series, sd in world["series"].items():
        models = {k: v for k, v in world["models"].items() if v["series"] == series}
        for mid, m in models.items():
            if "charging_chart" in m["figure_facts"]:
                add(f"{mid}-CC", series, mid, "CC", charging_chart, mid, m)
            if "blower_table" in m["figure_facts"]:
                add(f"{mid}-BT", series, mid, "BT", blower_chart if series == "VAH" else blower_table, mid, m)
        add(f"{series}-WD", series, None, "WD", wiring_diagram, series, sd, models)
        add(f"{series}-LED", series, None, "LED", led_table, series, sd)
        if "thermistor" in sd["figure_facts"]:
            add(f"{series}-TH", series, None, "TH", thermistor_curve, series, sd)
        if "altitude_derate" in sd["figure_facts"]:
            add(f"{series}-ALT", series, None, "ALT", altitude_derate, series, sd)
        if "lineset_adder_oz_per_ft" in sd["figure_facts"]:
            add(f"{series}-LS", series, None, "LS", lineset_adder, series, sd)
    (SPEC / "figures.json").write_text(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    mf = render_all()
    print(f"rendered {len(mf)} figures -> {FIGURES}")
