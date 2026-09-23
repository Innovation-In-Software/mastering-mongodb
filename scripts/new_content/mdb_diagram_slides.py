#!/usr/bin/env python3
"""Shared helpers for inserting full-width diagram-image slides into the new decks.

Each module keeps its images in scripts/new_content/diagrams/moduleNN/ named
"NN - Title.png", where NN is the content slide the diagram follows. A module
declares DIAGRAMS = {NN: (title, subtitle, talking_points)} and calls
build_deck(), which interleaves the diagram slides and renumbers every page by
its real position.
"""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageChops

import mdb_deck_kit as K
import mdb_speaker_notes as SN
import mdb_visuals as V


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


def diagram_file(image_dir: Path, n: int) -> Path:
    matches = sorted(image_dir.glob(f"{n:02d} - *.png"))
    assert matches, f"missing diagram image for slide {n} in {image_dir}"
    return matches[0]


def trimmed_image(path: Path):
    """Trim the white margins around a diagram and return (JPEG stream, aspect ratio)."""
    src = Image.open(path)
    if src.mode in ("RGBA", "LA", "P"):
        # Transparent areas would turn black in a plain RGB conversion; lay them on white.
        rgba = src.convert("RGBA")
        img = Image.new("RGB", rgba.size, (255, 255, 255))
        img.paste(rgba, mask=rgba.getchannel("A"))
    else:
        img = src.convert("RGB")
    diff = ImageChops.difference(img, Image.new("RGB", img.size, (255, 255, 255)))
    bbox = diff.convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    if bbox:
        pad = 24
        left, top, right, bottom = bbox
        img = img.crop((max(0, left - pad), max(0, top - pad), min(img.width, right + pad),
                        min(img.height, bottom + pad)))
    stream = io.BytesIO()
    img.save(stream, format="JPEG", quality=92, optimize=True)
    stream.seek(0)
    return stream, img.width / img.height


def add_diagram_slide(prs, layout, *, after: int, image_dir: Path, title: str, subtitle: str,
                      points: list[dict]) -> None:
    slide, top = V.content_slide(prs, layout, number=after, title=title, subtitle=subtitle)
    stream, aspect = trimmed_image(diagram_file(image_dir, after))
    x0, x1 = V.LEFT, 12.30
    y0, y1 = top + 0.06, 6.92
    pad = 0.10
    avail_w, avail_h = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    w = min(avail_w, avail_h * aspect)
    h = w / aspect
    x = x0 + (x1 - x0 - w) / 2
    y = y0 + (y1 - y0 - h) / 2
    V.box(slide, x - pad, y - pad, w + 2 * pad, h + 2 * pad, "", fill=V.WHITE,
          line=V.CARD_LINE, radius=0.03)
    pic = slide.shapes.add_picture(stream, V.I(x), V.I(y), V.I(w), V.I(h))
    pic.name = f"Diagram {after:02d}"
    V.finish(slide, number=after, notes=SN.compose({"talking_points": points}))


def build_deck(prs, layout, slides, diagrams: dict, image_dir: Path) -> None:
    """Build content slides in order, inserting each diagram slide after its slide.

    Page numbers follow each slide's real position in the finished deck.
    """
    base_footer = K.add_rail_and_footer

    def positional_footer(slide, page_num=None):
        base_footer(slide, len(prs.slides) if page_num is not None else None)

    K.add_rail_and_footer = positional_footer
    try:
        for n, build in enumerate(slides, start=1):
            build(prs, layout)
            if n in diagrams:
                title, subtitle, points = diagrams[n]
                add_diagram_slide(prs, layout, after=n, image_dir=image_dir, title=title,
                                  subtitle=subtitle, points=points)
    finally:
        K.add_rail_and_footer = base_footer
