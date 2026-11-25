"""Record docs/img/demo.gif: type a question, get the answer, tap a citation, land on the cited chart.

Drives the installed Google Chrome through Playwright and stitches screenshots with Pillow (no ffmpeg).
Start the app first (make app), then:  uv run python scripts/demo_gif.py
"""
from __future__ import annotations

import argparse
import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

QUESTION = "On a VRT-060 it's 95 degrees outside and I'm reading 130 psig suction. What liquid pressure should I see?"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8000/")
    ap.add_argument("--q", default=QUESTION)
    ap.add_argument("--out", default="docs/img/demo.gif")
    ap.add_argument("--width", type=int, default=900)
    a = ap.parse_args()
    frames: list[tuple[Image.Image, int]] = []   # (frame, duration ms)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_context(viewport={"width": 900, "height": 1000}, color_scheme="light").new_page()

        def snap(ms: int) -> None:
            img = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
            img.thumbnail((a.width, a.width * 2))
            frames.append((img, ms))

        page.goto(a.url, wait_until="networkidle")
        snap(900)
        page.click("#q")
        for i in range(0, len(a.q), 6):                       # typing, a few characters per frame
            page.keyboard.type(a.q[i:i + 6], delay=0)
            snap(70)
        snap(500)
        page.click("#go")
        page.wait_for_timeout(250)
        snap(700)                                             # "Searching manuals, calls and photos..."
        page.wait_for_function("document.querySelector('#answer').innerHTML.length > 0", timeout=180_000)
        page.wait_for_load_state("networkidle")
        page.evaluate("document.querySelector('#answer').scrollIntoView({block: 'start'})")
        page.wait_for_timeout(300)
        snap(2600)                                            # the answer with its yellow tags
        cite = page.locator("#answer button.cite").first
        if cite.count():
            cite.click()
            page.wait_for_timeout(500)
            snap(400)
            page.wait_for_timeout(500)
            snap(3200)                                        # the cited figure crop, flashing
        page.evaluate("window.scrollTo(0, 0)")
        browser.close()

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f, _ in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=[d for _, d in frames], loop=0, optimize=True)
    print(f"{out}  {len(frames)} frames  {out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
