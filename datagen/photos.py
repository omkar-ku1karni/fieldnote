"""Job photos, taken from openly licensed Wikimedia Commons images (CC0, PD, CC BY, CC BY-SA).

  candidates  search Commons, download candidates with their licence info, make contact sheets
  build       download the curated set in data/spec/photos.yaml (pinned by Commons page id, so
              a fork gets the same images), strip EXIF, resize, attach the fake job metadata,
              write data/generated/photos/ and data/spec/photos.json

The metadata is only job id, site, unit, date and tech. There's no description on purpose, so
"what failed?" can only be answered by looking at the photo.

Run:  uv run python -m datagen.photos candidates | build
"""
from __future__ import annotations

import io
import json
import random
import re
import sys
import time

import httpx
import yaml
from PIL import Image, ImageDraw, ImageOps

from fieldnote.config import DATA, GENERATED, SPEC

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "fieldnote-datagen/0.1 (open-source research dataset builder; python-httpx)"}
CAND = DATA / "raw" / "photos"
OUT = GENERATED / "photos"
MAX_SIDE = 1280
ALLOWED = re.compile(r"^(CC0|CC BY(-SA)? \d|CC BY(-SA)?$|Public domain|PD)", re.I)

QUERIES = [
    "air conditioner capacitor", "run capacitor", "swollen capacitor", "bulging capacitor", "dual run capacitor",
    "condenser coil", "air conditioner condenser unit", "condensing unit", "frozen heat pump", "heat pump ice",
    "frozen air conditioner", "contactor air conditioner", "burnt contactor", "burned electrical contacts",
    "rooftop air conditioning unit", "rooftop hvac", "air conditioner compressor", "scroll compressor",
    "air handler", "gas furnace burner", "refrigerant manifold gauge", "hvac technician", "thermostat wiring",
    "blower wheel", "condenser fan motor", "air conditioner disconnect", "dirty air filter", "evaporator coil",
    "heat pump outdoor unit", "ductwork", "corroded condenser coil", "dirty condenser coil",
    "failed capacitor", "capacitor failure", "leaking capacitor", "exploded capacitor", "electrolytic capacitor bulged",
    "motor run capacitor", "relay burnt", "burnt terminal", "melted wire", "arc damage", "burned relay contacts",
    "contactor", "electrical fire damage",
]


def _api(client: httpx.Client, **params) -> dict:
    params = {"action": "query", "format": "json", "prop": "imageinfo",
              "iiprop": "url|extmetadata|size|mime", "iiurlwidth": MAX_SIDE, **params}
    for attempt in range(5):
        r = client.get(API, params=params)
        if r.status_code in (429, 503):
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()
    return {}


def _meta(page: dict) -> dict | None:
    ii = page["imageinfo"][0]
    em = ii.get("extmetadata", {})
    lic = em.get("LicenseShortName", {}).get("value", "")
    if ii.get("mime") not in ("image/jpeg", "image/png") or not ALLOWED.match(lic) or ii.get("width", 0) < 480:
        return None
    strip = lambda v: re.sub(r"<[^>]+>", "", v or "").strip()  # noqa: E731
    return dict(pageid=page["pageid"], title=page["title"], license=lic,
                license_url=em.get("LicenseUrl", {}).get("value"), creator=strip(em.get("Artist", {}).get("value")),
                source=ii.get("descriptionurl"), thumb=ii.get("thumburl") or ii["url"])


def _save_image(content: bytes, path) -> None:
    img = Image.open(io.BytesIO(content))
    img = ImageOps.exif_transpose(img).convert("RGB")  # apply rotation; EXIF is dropped on save
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    img.save(path, quality=88)


def candidates() -> None:
    CAND.mkdir(parents=True, exist_ok=True)
    mpath = CAND / "candidates.json"
    seen = {c["pageid"]: c for c in json.loads(mpath.read_text())} if mpath.exists() else {}
    seen = {k: v for k, v in seen.items() if isinstance(k, int)}
    with httpx.Client(headers=UA, timeout=40, follow_redirects=True) as client:
        for q in QUERIES:
            d = _api(client, generator="search", gsrnamespace=6, gsrsearch=f"{q} filetype:bitmap", gsrlimit=15)
            new = 0
            for page in d.get("query", {}).get("pages", {}).values():
                m = _meta(page)
                if not m or m["pageid"] in seen:
                    continue
                try:
                    r = client.get(m["thumb"])
                    r.raise_for_status()
                    _save_image(r.content, CAND / f"wm{m['pageid']}.jpg")
                except Exception as e:  # noqa: BLE001
                    print(f"  skip {m['pageid']}: {type(e).__name__}")
                    continue
                seen[m["pageid"]] = dict(m, query=q)
                new += 1
                time.sleep(0.2)
            print(f"{q!r}: {new} new (total {len(seen)})")
            mpath.write_text(json.dumps(list(seen.values()), indent=1, ensure_ascii=False))
    contact_sheets(list(seen.values()))


def contact_sheets(items: list[dict], per=30, cols=6, cell=260) -> None:
    sheets = CAND / "sheets"
    sheets.mkdir(exist_ok=True)
    for f in sheets.glob("sheet_*.jpg"):
        f.unlink()
    index = {}
    for s in range(0, len(items), per):
        batch = items[s:s + per]
        rows = (len(batch) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), "white")
        d = ImageDraw.Draw(sheet)
        for i, it in enumerate(batch):
            n = s + i
            index[n] = it["pageid"]
            im = Image.open(CAND / f"wm{it['pageid']}.jpg")
            im.thumbnail((cell - 8, cell - 8))
            x, y = (i % cols) * cell, (i // cols) * (cell + 22)
            sheet.paste(im, (x + 4, y + 4))
            d.rectangle([x, y + cell - 2, x + cell, y + cell + 20], fill="black")
            d.text((x + 6, y + cell + 2), f"#{n}  {it['query'][:28]}", fill="yellow")
        sheet.save(sheets / f"sheet_{s // per:02d}.jpg", quality=80)
    (sheets / "index.json").write_text(json.dumps(index, indent=0))
    print(f"{len(items)} candidates, contact sheets -> {sheets}")


def build() -> None:
    world = json.loads((SPEC / "world.json").read_text())
    curated = yaml.safe_load((SPEC / "photos.yaml").read_text())
    rng = random.Random(world["seed"])
    slots = {s["id"]: s for s in world["photo_slots"]}
    OUT.mkdir(parents=True, exist_ok=True)
    items = curated["photos"]
    metas: dict[int, dict] = {}
    with httpx.Client(headers=UA, timeout=40, follow_redirects=True) as client:
        ids = [it["pageid"] for it in items]
        for i in range(0, len(ids), 40):
            d = _api(client, pageids="|".join(map(str, ids[i:i + 40])))
            for page in d["query"]["pages"].values():
                metas[page["pageid"]] = _meta(page)
        out = []
        for i, it in enumerate(items):
            m = metas.get(it["pageid"])
            if not m:
                print(f"  pageid {it['pageid']} unavailable or license changed — skipped")
                continue
            pid = it.get("slot") or f"P-{i:03d}"
            path = OUT / f"{pid}.jpg"
            cached = CAND / f"wm{it['pageid']}.jpg"
            if cached.exists():
                path.write_bytes(cached.read_bytes())
            else:
                r = client.get(m["thumb"])
                r.raise_for_status()
                _save_image(r.content, path)
                time.sleep(0.2)
            if it.get("slot"):
                s = slots[it["slot"]]
                job = dict(site_id=s["site"], unit=s["unit"], job=s["job"], date=s["date"], tech=s["tech"])
            else:
                a = rng.choice(world["assets"])
                job = dict(site_id=a["site_id"], unit=a["unit"],
                           job=f"J-{rng.choice([24, 25])}-{rng.randint(100, 1299):04d}",
                           date=f"202{rng.choice([4, 5])}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                           tech=rng.choice(world["techs"]))
            out.append(dict(photo_id=pid, file=path.name, **job,
                            attribution={k: m[k] for k in ("title", "creator", "license", "license_url", "source")}))
    (SPEC / "photos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"built {len(out)} photos -> {OUT}")


if __name__ == "__main__":
    {"candidates": candidates, "build": build}[sys.argv[1] if len(sys.argv) > 1 else "candidates"]()
