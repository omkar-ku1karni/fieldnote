"""Paths and env. Import before torch/HF so the model caches end up in the right place."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

_SSD_CACHE = Path("/Volumes/Crucial_1TB/cache")  # my external drive; skipped if it isn't there
if _SSD_CACHE.exists():
    os.environ.setdefault("HF_HOME", str(_SSD_CACHE / "huggingface"))
    os.environ.setdefault("TORCH_HOME", str(_SSD_CACHE / "torch"))

DATA = ROOT / "data"
SPEC = DATA / "spec"
CONTENT = DATA / "content"
GENERATED = DATA / "generated"
FIGURES = GENERATED / "figures"
EVAL = ROOT / "eval"
