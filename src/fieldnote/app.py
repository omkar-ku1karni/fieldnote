"""The web app: one question box, an answer, and the evidence behind it.

  GET  /                             static page, no build step
  POST /api/ask {question}           answer + sources + timings
  GET  /api/examples                 example questions
  GET  /api/clip/{call}?start&end    the cited bit of a call as WAV (iOS Safari won't seek in ogg)
  GET  /media/{pages|crops|photos}/{file}

Run:  make app   (or: uv run uvicorn fieldnote.app:app --port 8000)
"""
from __future__ import annotations

import io
import json
import re
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from fieldnote.config import GENERATED

WEB = Path(__file__).parent / "web"
app = FastAPI(title="Fieldnote", docs_url="/api/docs")

EXAMPLES = [
    dict(q="Lakeshore Medical RTU-7 keeps tripping on high pressure on hot afternoons. What's going on and "
           "what should I check?", why="Register, service bulletin, support call, wiring diagram and a job photo"),
    dict(q="On a VRT-060 it's 95 degrees outside and I'm reading 130 psig suction. What liquid pressure should I "
           "see if the charge is right?", why="The answer exists only inside a charging chart"),
    dict(q="VRL board LED is flashing 4 red then 2 green. What does that mean?",
         why="Read from a flash-code diagram"),
    dict(q="The VRL economizer damper won't modulate. Support said something about a jumper?",
         why="Only said out loud on a recorded support call"),
    dict(q="Find me the photo of a burnt contactor. Which site was it from?", why="Searches job photos by what they show"),
]


class Ask(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@app.on_event("startup")
def _warm() -> None:
    from fieldnote import encoders as E
    from fieldnote.ingest import client
    try:
        client()  # fail at startup if something else has the index open, not on the first question
    except RuntimeError as e:
        raise SystemExit("The index at data/index/qdrant is open in another process (an eval, a rebuild or a second "
                         "server). Stop that process, then start the app again.") from e
    E.warmup(rerank_model=False)


@app.post("/api/ask")
def ask(body: Ask):
    from fieldnote.answer import answer
    from fieldnote.llm import LLMUnavailable
    try:
        a = answer(body.question.strip())
    except LLMUnavailable as e:
        raise HTTPException(503, f"No language model answered. {str(e).splitlines()[0]} "
                                 "Check the keys in .env, or start Ollama for the local fallback.") from e
    return dict(question=a.question, answer=a.text, cited=a.cited, provider=a.provider, model=a.model,
                timings={k: round(v) for k, v in a.timings.items()}, sources=[asdict(s) for s in a.sources])


@app.get("/api/examples")
def examples():
    return EXAMPLES


@app.get("/api/clip/{call_id}")
def clip(call_id: str, start: float = Query(0, ge=0), end: float = Query(30, ge=0)):
    if not re.fullmatch(r"C\d{2}", call_id):
        raise HTTPException(404, "Unknown call.")
    path = GENERATED / "calls" / f"{call_id}.ogg"
    if not path.exists():
        raise HTTPException(404, "Recording not found. Run make audio.")
    audio, sr = sf.read(path, dtype="float32")
    a, b = int(max(0, start - 1.5) * sr), int(min(len(audio) / sr, end + 1.0) * sr)
    buf = io.BytesIO()
    sf.write(buf, np.asarray(audio[a:b]), sr, format="WAV", subtype="PCM_16")
    return Response(buf.getvalue(), media_type="audio/wav", headers={"Cache-Control": "max-age=86400"})


@app.get("/api/health")
def health():
    manifest = GENERATED.parent / "index" / "manifest.json"
    return dict(ok=manifest.exists(), index=json.loads(manifest.read_text()) if manifest.exists() else None,
                time=time.strftime("%H:%M:%S"))


for sub in ("pages", "crops", "photos"):
    (GENERATED / sub).mkdir(parents=True, exist_ok=True)
    app.mount(f"/media/{sub}", StaticFiles(directory=GENERATED / sub), name=sub)
app.mount("/static", StaticFiles(directory=WEB), name="static")


@app.get("/")
def index():
    return FileResponse(WEB / "index.html")
