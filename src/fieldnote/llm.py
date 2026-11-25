"""Vision LLM calls. Providers are tried in FIELDNOTE_LLM order (default gemini,groq,ollama)
and the first one that's configured and answers wins.

  gemini  GEMINI_API_KEY              GEMINI_MODEL to pin a model
  groq    GROQ_API_KEY                GROQ_MODEL to pin a model
  ollama  local, no key                OLLAMA_HOST, OLLAMA_MODEL (e.g. qwen2.5vl:7b)

With no keys at all everything runs locally through Ollama.
"""
from __future__ import annotations

import base64
import io
import os
import time
from dataclasses import dataclass
from functools import lru_cache

import httpx
from PIL import Image

import fieldnote.config  # noqa: F401


class LLMUnavailable(RuntimeError):
    """Every configured provider failed (no keys, rate-limited, or Ollama not running)."""


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str
    latency_ms: float
    waited_ms: float = 0.0   # time slept on rate limits and retries, not real work


def _b64(img: Image.Image, max_side: int = 1400) -> str:
    img = img.convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()


# Fastest model that passed the chart-reading check goes first. Google retires and overloads
# models often, so a 404 or 503 just moves on to the next one.
GEMINI_MODELS = ["gemini-flash-lite-latest", "gemini-3.5-flash", "gemini-flash-latest"]
_gemini_dead: set[str] = set()


def _gemini(system: str, prompt: str, images: list[Image.Image], labels: list[str]) -> tuple[str, str]:
    key = os.environ["GEMINI_API_KEY"]
    models = [os.environ["GEMINI_MODEL"]] if os.getenv("GEMINI_MODEL") else GEMINI_MODELS
    parts = [{"text": prompt}]
    for i, img in enumerate(images):  # each image goes right after its label
        if i < len(labels):
            parts.append({"text": labels[i]})
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": _b64(img)}})
    body = {"system_instruction": {"parts": [{"text": system}]}, "contents": [{"parts": parts}],
            "generationConfig": {"temperature": 0.1}}
    last = None
    for model in [m for m in models if m not in _gemini_dead] or models:
        r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                       headers={"x-goog-api-key": key}, json=body, timeout=120)
        if r.status_code in (404, 503):
            if r.status_code == 404:
                _gemini_dead.add(model)
            last = r
            continue
        r.raise_for_status()
        cand = r.json()["candidates"][0]
        return model, "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    last.raise_for_status()
    raise RuntimeError("no Gemini model available")


@lru_cache(maxsize=None)
def _groq_model(key: str) -> str:
    if os.getenv("GROQ_MODEL"):
        return os.environ["GROQ_MODEL"]
    ids = [m["id"] for m in httpx.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {key}"},
                                      timeout=30).raise_for_status().json()["data"]]
    # /models doesn't say which ones take images, so match on the families that do.
    vision = sorted(i for i in ids if any(k in i.lower() for k in ("qwen", "scout", "maverick", "vision", "-vl", "llava")))
    if not vision:
        raise RuntimeError("no vision model visible to this Groq key")
    return vision[0]


def _openai_style(url, headers, model, system, prompt, images, labels=(), timeout=120, max_side=1400):
    content = [{"type": "text", "text": prompt}]
    for i, img in enumerate(images):
        if i < len(labels):
            content.append({"type": "text", "text": labels[i]})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_b64(img, max_side)}"}})
    body = {"model": model, "temperature": 0.1,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}]}
    r = httpx.post(url, headers=headers, json=body, timeout=timeout).raise_for_status().json()
    return r["choices"][0]["message"]["content"]


GROQ_MAX_IMAGES = 3  # Groq's qwen3.8-27b rejects requests with more than 3 images


def _groq(system, prompt, images, labels):
    key = os.environ["GROQ_API_KEY"]
    model = _groq_model(key)
    # images come in rank order, so cutting the tail drops the least relevant ones
    return model, _openai_style("https://api.groq.com/openai/v1/chat/completions",
                                {"Authorization": f"Bearer {key}"}, model, system, prompt, images[:GROQ_MAX_IMAGES],
                                labels[:GROQ_MAX_IMAGES], max_side=1024)  # smaller images keep us under the size limit


def _ollama(system, prompt, images, labels):
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL")
    if not model:
        tags = [m["name"] for m in httpx.get(f"{host}/api/tags", timeout=5).raise_for_status().json()["models"]]
        model = next((t for t in tags if "vl" in t or "vision" in t or "gemma3" in t), None)
        if not model:
            raise RuntimeError(f"no vision model pulled in Ollama (have {tags})")
    body = {"model": model, "stream": False, "keep_alive": os.getenv("OLLAMA_KEEP_ALIVE", "2m"),
            "options": {"temperature": 0.1, "num_ctx": 16384},
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt + ("\nImages, in order: " + "; ".join(labels) if labels else ""),
                          "images": [_b64(i, 1024) for i in images]}]}
    r = httpx.post(f"{host}/api/chat", json=body, timeout=600).raise_for_status().json()
    return model, r["message"]["content"]


PROVIDERS = {"gemini": ("GEMINI_API_KEY", _gemini), "groq": ("GROQ_API_KEY", _groq), "ollama": (None, _ollama)}

# Circuit breaker: provider -> time until which we skip it (rate limited or out of quota).
_cooldown: dict[str, float] = {}
SHORT_WAIT_S = 20         # a 429 asking for less than this: wait it out and retry the same provider
DEFAULT_COOLDOWN_S = 600  # a 429 with no hint usually means the daily quota is gone


def available(order: list[str] | None = None) -> list[str]:
    order = order or os.getenv("FIELDNOTE_LLM", "gemini,groq,ollama").split(",")
    return [p for p in order if p in PROVIDERS and (PROVIDERS[p][0] is None or os.getenv(PROVIDERS[p][0]))]


def _retry_after(e: httpx.HTTPStatusError) -> float | None:
    """How long the provider asked us to wait, if it said."""
    h = e.response.headers.get("retry-after")
    if h:
        try:
            return float(h)
        except ValueError:
            pass
    try:  # Gemini: error.details[].retryDelay = "37s"
        for d in e.response.json().get("error", {}).get("details", []):
            if "retryDelay" in d:
                return float(str(d["retryDelay"]).rstrip("s"))
    except Exception:  # noqa: BLE001
        pass
    return None


def generate(system: str, prompt: str, images: list[Image.Image] | None = None, retries: int = 2,
             providers: list[str] | None = None, labels: list[str] | None = None) -> LLMResult:
    errors = []
    t_start = time.perf_counter()
    for name in available(providers):
        if _cooldown.get(name, 0) > time.time():
            errors.append(f"{name}: cooling down {int(_cooldown[name] - time.time())}s more (rate limited)")
            continue
        fn = PROVIDERS[name][1]
        for attempt in range(retries):
            t = time.perf_counter()
            try:
                model, text = fn(system, prompt, images or [], labels or [])
                return LLMResult(text.strip(), name, model, (time.perf_counter() - t) * 1000,
                                 waited_ms=(time.perf_counter() - t_start) * 1000 - (time.perf_counter() - t) * 1000)
            except httpx.HTTPStatusError as e:
                code = e.response.status_code
                errors.append(f"{name}: HTTP {code} {e.response.text[:160]}")
                if code >= 500 and code != 503 and attempt < retries - 1:
                    time.sleep(2)
                    continue
                if code == 429:
                    wait = _retry_after(e)
                    if wait is not None and wait <= SHORT_WAIT_S and attempt < retries - 1:
                        time.sleep(wait + 1)
                        continue
                    _cooldown[name] = time.time() + (wait if wait and wait > SHORT_WAIT_S else DEFAULT_COOLDOWN_S)
                break  # try the next provider
            except (httpx.TimeoutException, httpx.TransportError) as e:
                errors.append(f"{name}: {type(e).__name__}: {str(e)[:160]}")
                if attempt < retries - 1:
                    continue  # network blip, retry once
                break
            except Exception as e:  # noqa: BLE001
                errors.append(f"{name}: {type(e).__name__}: {str(e)[:160]}")
                break
    raise LLMUnavailable("no LLM provider succeeded:\n  " + "\n  ".join(errors or ["none configured"]))
