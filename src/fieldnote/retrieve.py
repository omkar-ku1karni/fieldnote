"""Retrieval: resolve the site/unit, search each modality in parallel, then fuse the rankings.

Each modality has its own encoder, so the raw scores mean different things (a ColSmol MaxSim
of 14 vs a SigLIP cosine of 0.15). We never compare them, only merge ranks with weighted RRF.
"""
from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import lru_cache

from fieldnote import encoders as E
from fieldnote.config import SPEC


@dataclass
class Config:
    k: int = 20                      # the p95 latency gate is measured at k=20
    per_list: int = 20               # depth of each per-modality search
    # Off by default. MiniLM didn't move recall on our eval, and bge-reranker-base bought ~2 points
    # of R@20 for ~3 s of CPU time. Numbers are in the README.
    rerank: bool = False
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L6-v2"
    entity_lookup: bool = True
    use_pages: bool = True
    use_photos: bool = True
    use_text: bool = True
    rrf_k: int = 60
    text_collection: str = "text"    # "text_caption" = caption-only baseline
    # Guaranteed slots in the final k. Without these, text chunks push photos and pages out.
    quotas: dict = field(default_factory=lambda: dict(photo=3, page=4))
    weights: dict = field(default_factory=lambda: dict(text=1.0, pages=1.0, photos=0.8, lookup=2.0))


@dataclass
class Hit:
    modality: str                    # page | doc_text | call | photo | register
    key: str                         # unit of retrieval used for scoring
    score: float
    payload: dict
    sources: list = field(default_factory=list)


def unit_key(modality: str, p: dict) -> str:
    if modality in ("page", "doc_text", "register"):
        return f"{p['doc_id']}#p{p['page']}"
    if modality == "call":
        return f"call:{p['call_id']}"
    return f"photo:{p['photo_id']}"     # photo or photo_caption: same retrieval unit


# --- entity lookup

@lru_cache(maxsize=1)
def _world():
    return json.loads((SPEC / "world.json").read_text())


@lru_cache(maxsize=1)
def _site_aliases() -> list[tuple[re.Pattern, str]]:
    out = []
    for s in _world()["sites"]:
        name = s["name"]
        words = name.replace("&", "and").split()
        aliases = {name, name.replace("&", "and"), " ".join(words[:2]), words[0]}
        if words[0].lower() == "elm":  # people write this one every possible way
            aliases |= {"Elm & 3rd", "Elm and 3rd", "Elm and Third"}
        for a in aliases:
            out.append((re.compile(rf"\b{re.escape(a)}\b", re.I), s["id"]))
    return out


UNIT_RE = re.compile(r"\b(RTU|CU|AH)[\s-]?(\d{1,2})\b", re.I)
TYPE_WORDS = [(re.compile(r"\b(condensing unit|condenser unit|split condenser)\b", re.I), "CU"),
              (re.compile(r"\b(air[ -]?handler|AHU)\b", re.I), "AH")]


def lookup(query: str) -> dict:
    """Find site and unit mentions in the query and match them to rows in the equipment register."""
    sites = {sid for pat, sid in _site_aliases() if pat.search(query)}
    units = {f"{m.group(1).upper()}-{int(m.group(2))}" for m in UNIT_RE.finditer(query)}
    world = _world()
    if sites and not units:  # "the condensing unit at Lakeshore" -> CU-1 when the site has exactly one
        for pat, prefix in TYPE_WORDS:
            if pat.search(query):
                cands = [a["unit"] for a in world["assets"] if a["site_id"] in sites and a["unit"].startswith(prefix)]
                if len(cands) == 1:
                    units.add(cands[0])
    assets = [a for a in world["assets"] if a["site_id"] in sites and (not units or a["unit"] in units)]
    site_objs = [s for s in world["sites"] if s["id"] in sites]
    return dict(sites=site_objs, units=sorted(units), assets=assets)


@lru_cache(maxsize=1)
def _register_pages() -> dict:
    """(site, unit) -> page of the register PDF, found by searching the register's text."""
    from fieldnote.ingest import client
    c = client()
    pts, _ = c.scroll("text", scroll_filter=_flt(doc_id="RMS-REGISTER"), limit=200, with_payload=True)
    out = {}
    for a in _world()["assets"]:
        for p in pts:
            if a["serial"] in p.payload["text"]:
                out[(a["site_id"], a["unit"])] = p.payload["page"]
    for s in _world()["sites"]:
        for p in sorted(pts, key=lambda p: p.payload["page"]):
            if f"Site elevation {s['elevation_ft']:,}" in p.payload["text"]:
                out[(s["id"], None)] = p.payload["page"]
                break
    return out


def _flt(**kv):
    from qdrant_client import models as qm
    return qm.Filter(must=[qm.FieldCondition(key=k, match=qm.MatchValue(value=v)) for k, v in kv.items()])


# --- search

@lru_cache(maxsize=1)
def _client():
    from fieldnote.ingest import client
    return client()


def _search_text(q: str, n: int, flt=None, coll: str = "text") -> tuple[list[Hit], list[Hit]]:
    from qdrant_client import models as qm
    c = _client()
    dense = c.query_points(coll, query=E.encode_text_query(q).tolist(), using="dense", limit=n,
                           query_filter=flt, with_payload=True).points
    idx, val = E.bm25_query(q)
    sparse = c.query_points(coll, query=qm.SparseVector(indices=idx, values=val), using="bm25", limit=n,
                            query_filter=flt, with_payload=True).points
    mk = lambda pts, src: [Hit(p.payload["modality"], unit_key(p.payload["modality"], p.payload), p.score,  # noqa: E731
                               p.payload, [src]) for p in pts]
    return mk(dense, "text-dense"), mk(sparse, "text-bm25")


def _search_pages(q: str, n: int) -> list[Hit]:
    pts = _client().query_points("pages", query=E.encode_page_query(q).tolist(), using="colsmol", limit=n,
                                 with_payload=True).points
    return [Hit("page", unit_key("page", p.payload), p.score, p.payload, ["pages-colsmol"]) for p in pts]


def _search_photos(q: str, n: int, flt=None) -> list[Hit]:
    pts = _client().query_points("photos", query=E.encode_photo_query(q).tolist(), using="siglip", limit=n,
                                 query_filter=flt, with_payload=True).points
    return [Hit("photo", unit_key("photo", p.payload), p.score, p.payload, ["photos-siglip"]) for p in pts]


def _rrf(lists: list[tuple[list[Hit], float]], k: int) -> dict[str, Hit]:
    fused: dict[str, Hit] = {}
    for hits, w in lists:
        for rank, h in enumerate(hits):
            key = f"{h.modality}|{h.key}|{h.payload.get('chunk', h.payload.get('start', ''))}"
            add = w / (k + rank + 1)
            if key in fused:
                fused[key].score += add
                fused[key].sources += h.sources
            else:
                fused[key] = Hit(h.modality, h.key, add, h.payload, list(h.sources))
    return fused


# Field techs say "high-pressure switch"; diagrams print "HPS". Expand both ways before searching.
GLOSSARY = [("high-pressure switch", "HPS"), ("high pressure switch", "HPS"), ("low-pressure switch", "LPS"),
            ("low pressure switch", "LPS"), ("minimum circuit ampacity", "MCA"), ("overcurrent protection", "MOP"),
            ("external static pressure", "ESP"), ("refrigerant detection sensor", "RDS"),
            ("rooftop unit", "RTU"), ("air handler", "AHU")]


def glossary_terms(q: str) -> str:
    low, add = q.lower(), []
    for long, short in GLOSSARY:
        if long in low and short.lower() not in low.split():
            add.append(short)
        elif re.search(rf"\b{short}\b", q) and long not in low:
            add.append(long)
    return " ".join(dict.fromkeys(add))


def retrieve(query: str, cfg: Config | None = None) -> tuple[list[Hit], dict]:
    cfg = cfg or Config()
    E.warmup(pages=cfg.use_pages, photos=cfg.use_photos, text=True, rerank_model=cfg.rerank and cfg.rerank_model)  # no-op once loaded
    _client()  # open qdrant here; two worker threads opening it at once is an error
    t0 = time.perf_counter()
    timings = {}
    ent = lookup(query) if cfg.entity_lookup else dict(sites=[], units=[], assets=[])
    expansion = " ".join(sorted({a["model"] for a in ent["assets"]})) if len(ent["assets"]) <= 3 else ""
    expansion = f"{expansion} {glossary_terms(query)}".strip()
    q_exp = f"{query} {expansion}".strip()

    jobs = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        if cfg.use_text:
            jobs["text"] = ex.submit(_search_text, q_exp, cfg.per_list, None, cfg.text_collection)
        if cfg.use_pages:
            jobs["pages"] = ex.submit(_search_pages, q_exp, cfg.per_list)
        if cfg.use_photos:
            jobs["photos"] = ex.submit(_search_photos, query, cfg.per_list)
        for a in ent["assets"][:3] if ent["units"] else []:
            jobs[f"unit:{a['unit']}"] = ex.submit(_unit_scoped, query, a, cfg)
        results = {k: f.result() for k, f in jobs.items()}
    timings["search_ms"] = (time.perf_counter() - t0) * 1000

    # Level 1: merge dense + BM25 into a single text ranking (optionally rerank the top 30).
    text_list: list[Hit] = []
    if "text" in results:
        dense, sparse = results["text"]
        text_list = sorted(_rrf([(dense, 1.0), (sparse, 1.0)], cfg.rrf_k).values(), key=lambda h: -h.score)
        if cfg.rerank and text_list:
            t1 = time.perf_counter()
            head, tail = text_list[:30], text_list[30:]
            ce = E.rerank(query, [h.payload["text"] for h in head], cfg.rerank_model)
            for h, sc in zip(head, ce):
                h.payload = dict(h.payload, ce_score=float(sc))
            text_list = [head[i] for i in ce.argsort()[::-1]] + tail
            timings["rerank_ms"] = (time.perf_counter() - t1) * 1000

    # Level 2: one vote per modality, plus the lists scoped to the resolved unit.
    lists = [(text_list, cfg.weights["text"])]
    if "pages" in results:
        lists.append((results["pages"], cfg.weights["pages"]))
    if "photos" in results:
        lists.append((results["photos"], cfg.weights["photos"]))
    for k, v in results.items():
        if k.startswith("unit:"):
            lists.append((v, cfg.weights["lookup"]))

    # the register rows go in as evidence too (they're what says RTU-7 is a VRT-060)
    reg = []
    if ent["assets"] or ent["sites"]:
        rp = _register_pages()
        keys = {(a["site_id"], a["unit"]) for a in ent["assets"][:3]} if ent["units"] else \
            {(s["id"], None) for s in ent["sites"]}
        for site_id, unit in keys:
            if (site_id, unit) in rp:
                reg.append(Hit("register", f"RMS-REGISTER#p{rp[(site_id, unit)]}", 1.0,
                               dict(doc_id="RMS-REGISTER", page=rp[(site_id, unit)], site_id=site_id, unit=unit,
                                    assets=[a for a in ent["assets"] if a["site_id"] == site_id]), ["lookup"]))
    lists.append((reg, cfg.weights["lookup"] * 2))

    fused = sorted(_rrf(lists, cfg.rrf_k).values(), key=lambda h: -h.score)
    # one hit per page/call/photo: five chunks of the same page aren't five sources
    seen, unique = set(), []
    for h in fused:
        if (h.modality, h.key) not in seen:
            seen.add((h.modality, h.key))
            unique.append(h)

    timings["total_ms"] = (time.perf_counter() - t0) * 1000
    return apply_quotas(unique, cfg.k, cfg.quotas), dict(entities=ent, expansion=expansion, timings=timings)


def apply_quotas(fused: list[Hit], k: int, quotas: dict) -> list[Hit]:
    """Top k by fused rank, except each modality in `quotas` always keeps its best n hits."""
    reserved = []
    for mod, n in quotas.items():
        reserved += [i for i, h in enumerate(fused) if h.modality == mod][:n]
    rest = [i for i in range(len(fused)) if i not in set(reserved)]
    keep = sorted(set(reserved) | set(rest[:max(0, k - len(set(reserved)))]))
    return [fused[i] for i in keep][:k]


def _unit_scoped(query: str, asset: dict, cfg: Config) -> list[Hit]:
    """Calls and photos filed against this exact unit, the way a CMMS would scope them."""
    pts = _client().query_points(cfg.text_collection, query=E.encode_text_query(query).tolist(), using="dense",
                                 limit=3, query_filter=_flt(site_id=asset["site_id"], unit=asset["unit"]),
                                 with_payload=True).points
    hits = [Hit(p.payload["modality"], unit_key(p.payload["modality"], p.payload), p.score, p.payload,
                ["unit-scoped"]) for p in pts]
    if not cfg.use_photos:
        return hits
    photos = _search_photos(query, 3, _flt(site_id=asset["site_id"], unit=asset["unit"]))
    for h in photos:
        h.sources = ["unit-scoped"]
    return hits + photos
