"""Assemble the document corpus as PDFs.

  manuals    data/content/manuals/<SERIES>.md  + figure images -> <SERIES>-IOM.pdf
  bulletins  data/content/bulletins/<id>.md                    -> <id>.pdf
  register   world.json assets/sites (code-generated)          -> RMS-REGISTER.pdf

Records where every figure lands (doc, page) in data/generated/docs.json, which the eval
uses to score page-level retrieval and citations. Figure captions carry only the figure
title, never its values.

Run:  uv run python -m datagen.pdfs
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from fieldnote.config import CONTENT, FIGURES, GENERATED, SPEC

DOCS = GENERATED / "docs"
_FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DejaVu", str(_FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(_FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", str(_FONT_DIR / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuMono", str(_FONT_DIR / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu-Oblique",
                              boldItalic="DejaVu-Bold")

BODY = ParagraphStyle("body", fontName="DejaVu", fontSize=9.2, leading=12.4, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=BODY, fontName="DejaVu-Bold", fontSize=17, leading=21, spaceAfter=10)
H2 = ParagraphStyle("h2", parent=BODY, fontName="DejaVu-Bold", fontSize=12.5, leading=16, spaceBefore=8, spaceAfter=6)
H3 = ParagraphStyle("h3", parent=BODY, fontName="DejaVu-Bold", fontSize=10.2, leading=13, spaceBefore=6, spaceAfter=4)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8, leading=10, spaceAfter=0)
CAPTION = ParagraphStyle("cap", parent=BODY, fontName="DejaVu-Oblique", fontSize=8.4, alignment=TA_CENTER, spaceAfter=10)
CALLOUT_COLORS = {"WARNING": "#b71c1c", "CAUTION": "#e65100", "NOTE": "#1565c0"}


FIG_TITLES: dict[str, str] = {}
MONO = ParagraphStyle("mono", parent=BODY, fontName="DejaVuMono", fontSize=7.4, leading=9.2, leftIndent=8,
                      spaceBefore=4, spaceAfter=8)


def inline(text: str) -> str:
    # an inline (mid-sentence / table-cell) placeholder is a reference, not a figure: use its title
    text = re.sub(r"`?\[\[FIGURE:([^\]]+)\]\]`?", lambda m: f"the *{FIG_TITLES.get(m.group(1), m.group(1))}* figure",
                  text)
    t = escape(text)
    t = re.sub(r"&lt;br\s*/?&gt;", "<br/>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    return t


class FigureMarker(Flowable):
    """Zero-size flowable that records the page a figure is drawn on."""

    def __init__(self, fid, sink, img_w, img_h, frame_w):
        super().__init__()
        self.fid, self.sink, self.img_w, self.img_h, self.frame_w = fid, sink, img_w, img_h, frame_w
        self.width = self.height = 0

    def draw(self):
        x, y = self.canv.absolutePosition(0, 0)  # frame left edge, top of the image (PDF points)
        x0 = x + (self.frame_w - self.img_w) / 2  # Image flowables are centered
        page_h = self.canv._pagesize[1]
        # bbox in top-left-origin points: [x0, y0, x1, y1]
        self.sink[self.fid] = dict(page=self.canv.getPageNumber(),
                                   bbox=[round(x0, 1), round(page_h - y, 1), round(x0 + self.img_w, 1),
                                         round(page_h - y + self.img_h, 1)])


def _table(rows: list[list[str]], width: float) -> Table:
    ncol = max(len(r) for r in rows)
    data = [[Paragraph(inline(c), CELL) for c in r + [""] * (ncol - len(r))] for r in rows]
    t = Table(data, colWidths=[width / ncol] * ncol, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#555555")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4e4e4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _callout(kind: str, text: str, width: float) -> Table:
    p = Paragraph(f"<b>{kind}:</b> {inline(text)}", BODY)
    t = Table([[p]], colWidths=[width])
    c = colors.HexColor(CALLOUT_COLORS.get(kind, "#333333"))
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, c), ("LINEBEFORE", (0, 0), (0, -1), 4, c),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def markdown_to_flowables(md: str, figs: dict, fig_pages: dict, width: float) -> list:
    """Parse the constrained Markdown dialect the prompts specify."""
    out: list = []
    lines = md.splitlines()
    i, fig_no = 0, 0
    para: list[str] = []

    def flush():
        if para:
            out.append(Paragraph(inline(" ".join(para)), BODY))
            para.clear()

    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if s.startswith("```"):
            flush()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            out.append(Preformatted("\n".join(block), MONO))
        elif not s or s.startswith("<!--"):
            flush()
        elif s == "[[PAGEBREAK]]":
            flush()
            out.append(PageBreak())
        elif m := re.match(r"^\[\[FIGURE:([^\]]+)\]\]$", s):
            flush()
            fid = m.group(1)
            fig_no += 1
            meta = figs[fid]
            img_path = FIGURES / meta["file"]
            from PIL import Image as PILImage
            w, h = PILImage.open(img_path).size
            scale = min(width / w, 6.3 * inch / h)
            out.append(KeepTogether([FigureMarker(fid, fig_pages, w * scale, h * scale, width),
                                     Image(str(img_path), w * scale, h * scale),
                                     Paragraph(f"Figure {fig_no}. {escape(meta['title'])}", CAPTION)]))
        elif s.startswith("### "):
            flush()
            out.append(Paragraph(inline(s[4:]), H3))
        elif s.startswith("## "):
            flush()
            out.append(Paragraph(inline(s[3:]), H2))
        elif s.startswith("# "):
            flush()
            out.append(Paragraph(inline(s[2:]), H1))
        elif m := re.match(r"^>\s*\*\*(WARNING|CAUTION|NOTE):\*\*\s*(.*)$", s):
            flush()
            text = [m.group(2)]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith(">") and "**" not in lines[i + 1][:6]:
                i += 1
                text.append(lines[i].strip().lstrip("> "))
            out.append(_callout(m.group(1), " ".join(text), width))
            out.append(Spacer(1, 6))
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            i -= 1
            out.append(_table(rows, width))
            out.append(Spacer(1, 8))
        elif re.match(r"^(-|\d+\.)\s+", s):
            flush()
            bullet = "•" if s.startswith("-") else re.match(r"^(\d+)\.", s).group(1) + "."
            text = re.sub(r"^(-|\d+\.)\s+", "", s)
            out.append(Paragraph(inline(text), BODY, bulletText=bullet))
            out[-1].style = ParagraphStyle("li", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=2)
        else:
            para.append(s)
        i += 1
    flush()
    return out


def _footer(doc_label: str):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("DejaVu", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.75 * inch, 0.5 * inch, doc_label)
        canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def build_pdf(md: str, out_path: Path, label: str, figs: dict) -> dict:
    fig_pages: dict = {}
    doc = SimpleDocTemplate(str(out_path), pagesize=LETTER, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.8 * inch, title=label)
    story = markdown_to_flowables(md, figs, fig_pages, doc.width)
    doc.build(story, onFirstPage=_footer(label), onLaterPages=_footer(label))
    return fig_pages


def register_markdown(world: dict) -> str:
    md = ["# Ridgeline Mechanical Services — Customer Equipment Register",
          "<!-- doc_id: RMS-REGISTER -->",
          "Internal reference for Ridgeline field technicians. One section per customer site. Unit tags match the "
          "labels painted on the equipment. Controller firmware is the version recorded at the last service visit.",
          "## Sites", "| Site | City | Elevation (ft) | Units |", "|---|---|---|---|"]
    for s in world["sites"]:
        n = sum(a["site_id"] == s["id"] for a in world["assets"])
        md.append(f"| {s['name']} | {s['city']} | {s['elevation_ft']:,} | {n} |")
    for s in world["sites"]:
        md += ["", f"## {s['name']}",
               f"{s['city']}. Site elevation {s['elevation_ft']:,} ft above sea level.",
               "| Unit tag | Model | Serial number | Controller firmware | Installed |", "|---|---|---|---|---|"]
        for a in (a for a in world["assets"] if a["site_id"] == s["id"]):
            md.append(f"| {a['unit']} | {a['model']} | {a['serial']} | {a['controller_firmware']} | {a['installed']} |")
    return "\n".join(md)


def main() -> None:
    world = json.loads((SPEC / "world.json").read_text())
    figs = {f["figure_id"]: f for f in json.loads((SPEC / "figures.json").read_text())}
    FIG_TITLES.update({k: v["title"] for k, v in figs.items()})
    DOCS.mkdir(parents=True, exist_ok=True)
    manifest = []
    jobs = [("RMS-REGISTER", "register", register_markdown(world),
             "Ridgeline Mechanical Services · Customer Equipment Register")]
    for series in world["series"]:
        p = CONTENT / "manuals" / f"{series}.md"
        if p.exists():
            jobs.append((f"{series}-IOM", "manual", p.read_text(),
                         f"Vantorr Climate Systems (fictional) · {series} Series IOM · Rev C"))
        else:
            print(f"skip {series}: no manual content yet")
    for b in world["bulletins"]:
        p = CONTENT / "bulletins" / f"{b['id']}.md"
        if p.exists():
            jobs.append((b["id"], "bulletin", p.read_text(), f"Vantorr Climate Systems (fictional) · {b['id']}"))
    for doc_id, kind, md, label in jobs:
        out = DOCS / f"{doc_id}.pdf"
        fig_pages = build_pdf(md, out, label, figs)
        from pypdf import PdfReader
        manifest.append(dict(doc_id=doc_id, kind=kind, file=out.name, pages=len(PdfReader(out).pages),
                             figure_pages=fig_pages))
        print(f"{doc_id}: {manifest[-1]['pages']} pages, {len(fig_pages)} figures")
    (GENERATED / "docs.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
