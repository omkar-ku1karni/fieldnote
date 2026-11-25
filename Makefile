SHELL := /bin/bash
# My machine keeps caches on an external drive. If it isn't mounted, uv's default is used.
ifneq ($(wildcard /Volumes/Crucial_1TB/cache),)
export UV_CACHE_DIR ?= /Volumes/Crucial_1TB/cache/uv
endif
PY := uv run python

.PHONY: setup spec figures questions prompts content pdfs audio photo-candidates photos corpus data check-llm index eval-retrieval ask captions baseline-index eval-generation eval app

setup:            ## install Python deps into .venv
	uv sync

spec:             ## seeded world spec (all ground-truth numbers)
	$(PY) -m datagen.world

figures: spec     ## render figure-only facts into manual-style images
	$(PY) -m datagen.figures

questions: spec   ## 40-question eval set with computed answers
	$(PY) -m datagen.questions

prompts: figures  ## regenerate the external-LLM prose prompts
	$(PY) -m datagen.prompts

content:          ## split + validate the LLM answers saved in data/content/_raw/
	$(PY) -m datagen.content

pdfs: figures     ## manuals + bulletins + equipment register -> PDFs (needs make content)
	$(PY) -m datagen.pdfs

audio:            ## support-call scripts -> phone-quality recordings + ground-truth timestamps
	$(PY) -m datagen.audio

photo-candidates: ## only needed to re-curate photos: search Commons, build contact sheets
	$(PY) -m datagen.photos candidates

photos:           ## download the curated, pinned CC-licensed photo set
	$(PY) -m datagen.photos build

data: figures questions prompts

corpus: content pdfs audio photos  ## everything the indexer needs

check-llm:        ## verify Gemini / Groq / Ollama keys and vision ability
	$(PY) scripts/check_llm.py

index:            ## transcribe calls, encode pages/photos/text, build the Qdrant index (data/index/)
	$(PY) -m fieldnote.ingest

eval-retrieval:   ## recall@k / MRR per question category, plus ablations
	$(PY) -m fieldnote.evaluate retrieval

ask:              ## one question end to end, e.g.  make ask Q="why does Lakeshore RTU-7 trip on high pressure?"
	$(PY) -m fieldnote.answer "$(Q)"

captions:         ## caption figures + photos for the caption-only baseline (cached in eval/captions.json)
	$(PY) -m fieldnote.baseline captions

baseline-index:   ## text index where every image is replaced by its caption
	$(PY) -m fieldnote.baseline index

eval-generation:  ## answer accuracy per category, Fieldnote vs caption-only baseline
	$(PY) -m fieldnote.evaluate generation

eval: eval-retrieval eval-generation

app:              ## the web app on http://localhost:8000
	uv run uvicorn fieldnote.app:app --port 8000
