# CPU-only image. Runs the app and the evals; it can rebuild the corpus and index too, just slowly.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    HF_HOME=/cache/huggingface \
    TORCH_HOME=/cache/torch \
    FIELDNOTE_DEVICE=cpu

RUN apt-get update && apt-get install -y --no-install-recommends make libsndfile1 espeak-ng curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-install-project
COPY . .
RUN uv sync --frozen

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "fieldnote.app:app", "--host", "0.0.0.0", "--port", "8000"]
