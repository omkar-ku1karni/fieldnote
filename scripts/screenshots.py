"""Screenshots of the running app (desktop + phone, light + dark) for the README.

Uses your installed Google Chrome through Playwright (channel="chrome"), so no browser download.
Start the app first (make app), then:

  uv run python scripts/screenshots.py [--q "question"] [--out docs/img] [--only home]
"""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

VIEWS = {
    "desktop": dict(viewport={"width": 1280, "height": 900}, device_scale_factor=1),
    "phone": dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8000/")
    ap.add_argument("--q", default=None)
    ap.add_argument("--out", default="docs/img")
    ap.add_argument("--name", default=None)
    ap.add_argument("--schemes", default="light,dark")
    ap.add_argument("--full", action="store_true", help="full-page screenshot")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    name = a.name or ("answer" if a.q else "home")
    url = a.url + (f"?q={quote(a.q)}" if a.q else "")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for view, opts in VIEWS.items():
            for scheme in a.schemes.split(","):
                ctx = browser.new_context(color_scheme=scheme, **opts)
                page = ctx.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                if a.q:
                    page.wait_for_function(
                        "document.querySelector('#answer').innerHTML.length > 0 || "
                        "document.querySelector('#status').classList.contains('error')", timeout=180_000)
                    page.wait_for_load_state("networkidle")
                path = out / f"{name}_{view}_{scheme}.png"
                page.screenshot(path=str(path), full_page=a.full)
                print(path)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
