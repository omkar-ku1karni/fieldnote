"""Turn the call scripts into recordings with Kokoro TTS (runs locally).

The agent is on a headset; the tech is on a phone on a roof: 300-3400 Hz band, 8 kHz, mu-law,
plus wind and equipment hum. So the speech recognizer gets audio about as rough as a real call.

Writes data/generated/calls/<id>.ogg and <id>.json with the true turn timestamps, which the
eval uses to check timestamp citations.

Run:  uv run python -m datagen.audio [C01 C02 ...]
"""
from __future__ import annotations

import json
import sys

import numpy as np
import soundfile as sf
from scipy import signal

from datagen.content import parse_call
from fieldnote.config import CONTENT, GENERATED, SPEC

SR = 24000          # Kokoro output rate
OUT_SR = 16000      # what ASR consumes
OUT = GENERATED / "calls"

VOICES = {  # fixed voice per fictional character
    "Dana Ortiz": "af_nicole", "Marcus Bell": "am_michael", "Priya Raman": "af_bella", "Luis Herrera": "am_eric",
    "Jen Kowalski": "af_sarah", "Sam Okafor": "am_puck",
    "Tom": "am_adam", "Alicia": "af_heart", "Raj": "am_liam", "Megan": "af_sky",
}


def phone_channel(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Tech side: rooftop noise, then a narrowband phone line."""
    n = len(x)
    wind = signal.lfilter([1], [1, -0.995], rng.normal(0, 1, n))           # brown noise ~ wind
    wind *= 0.5 + 0.5 * np.abs(np.sin(np.linspace(0, rng.uniform(2, 6) * np.pi, n)))  # gusts
    hum = 0.3 * np.sin(2 * np.pi * rng.uniform(55, 62) * np.arange(n) / SR)  # running equipment
    noise = wind / (np.std(wind) + 1e-9) + hum
    speech_rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    snr_db = rng.uniform(14, 22)
    x = x + noise * speech_rms / (10 ** (snr_db / 20)) / (np.sqrt(np.mean(noise ** 2)) + 1e-9)
    sos = signal.butter(4, [300, 3400], btype="band", fs=SR, output="sos")
    x = signal.sosfilt(sos, x)
    x8 = signal.resample_poly(x, 1, 3)                                       # 24k -> 8k
    mu = 255.0
    peak = np.max(np.abs(x8)) + 1e-9
    y = np.sign(x8 / peak) * np.log1p(mu * np.abs(x8 / peak)) / np.log1p(mu)
    y = np.round(y * 127) / 127                                              # 8-bit mu-law quantization
    x8 = np.sign(y) * (np.expm1(np.abs(y) * np.log1p(mu)) / mu) * peak
    return signal.resample_poly(x8, 3, 1)                                    # back to 24k for mixing


def render_call(pipe, call_id: str, rng: np.random.Generator) -> dict:
    hdr, (_, turns) = parse_call(CONTENT / "calls" / f"{call_id}.txt")
    tech, agent = hdr["tech"].split(" (")[0], hdr["agent"].split(" (")[0]
    chunks, timeline, t = [], [], 0.0
    lead = np.zeros(int(SR * 0.6))
    chunks.append(lead)
    t += len(lead) / SR
    for speaker, text in turns:
        voice = VOICES.get(tech if speaker == "TECH" else agent, "am_adam" if speaker == "AGENT" else "af_sarah")
        speed = rng.uniform(1.0, 1.12) if speaker == "TECH" else rng.uniform(0.95, 1.05)
        audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice=voice, speed=speed)])
        if speaker == "TECH":
            audio = phone_channel(audio.astype(np.float64), rng)
        audio = audio / (np.max(np.abs(audio)) + 1e-9) * (0.55 if speaker == "TECH" else 0.7)
        timeline.append(dict(speaker=speaker, text=text, start=round(t, 2), end=round(t + len(audio) / SR, 2)))
        chunks.append(audio)
        t += len(audio) / SR
        gap = rng.uniform(0.2, 0.65) + (2.0 if "hold" in text.lower() and speaker == "AGENT" else 0)
        chunks.append(np.zeros(int(SR * gap)))
        t += gap
    full = np.concatenate(chunks)
    full = full + rng.normal(0, 0.0015, len(full))                           # line hiss
    full = signal.resample_poly(full, 2, 3)                                  # 24k -> 16k
    OUT.mkdir(parents=True, exist_ok=True)
    sf.write(OUT / f"{call_id}.ogg", np.clip(full, -1, 1).astype(np.float32), OUT_SR, format="OGG", subtype="VORBIS")
    meta = dict(call_id=call_id, **{k: hdr[k] for k in ("date", "site", "unit", "model", "tech", "agent", "topic")},
                duration_s=round(t, 2), turns=timeline)
    (OUT / f"{call_id}.json").write_text(json.dumps(meta, indent=1))
    return meta


def main(ids: list[str]) -> None:
    from kokoro import KPipeline  # heavy import: keep it out of module import time
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    world = json.loads((SPEC / "world.json").read_text())
    ids = ids or [c["id"] for c in world["calls"]]
    for cid in ids:
        if not (CONTENT / "calls" / f"{cid}.txt").exists():
            print(f"{cid}: no script yet, skipping")
            continue
        rng = np.random.default_rng(int(cid[1:]) + world["seed"])
        meta = render_call(pipe, cid, rng)
        print(f"{cid}: {meta['duration_s']:.0f}s, {len(meta['turns'])} turns")


if __name__ == "__main__":
    main(sys.argv[1:])
