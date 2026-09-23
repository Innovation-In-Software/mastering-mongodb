#!/usr/bin/env python3
"""Draw one Kahoot cover per module. 1280x720, content kept in the center."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from mongodb_kahoot_questions import MODULE_TITLES  # noqa: E402

OUT = Path(__file__).resolve().parent / "covers"
W, H = 1280, 720

# Deck palette from scripts/new_content/mdb_deck_kit.py
NAVY = (0x00, 0x20, 0x60)
GREEN = (0x2E, 0x7D, 0x32)
WHITE = (255, 255, 255)
ACCENTS = [
    (0x00, 0x6B, 0x4F),  # 1 documents
    (0x0E, 0x7C, 0x7B),  # 2 setup
    (0x5B, 0x3A, 0x9E),  # 3 modeling
    (0xC9, 0x69, 0x0C),  # 4 query
    (0x15, 0x65, 0xC0),  # 5 aggregation
    (0x2E, 0x7D, 0x32),  # 6 indexes
    (0x6A, 0x1B, 0x9A),  # 7 replication
    (0xB7, 0x1C, 0x1C),  # 8 production
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_cover(module: int, title: str) -> Image.Image:
    accent = ACCENTS[(module - 1) % len(ACCENTS)]
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Soft accent panels so a square crop of the center still shows the module number.
    draw.rectangle((0, 0, 28, H), fill=accent)
    draw.rectangle((W - 28, 0, W, H), fill=accent)
    draw.ellipse((980, -160, 1420, 280), fill=accent)
    draw.ellipse((-180, 460, 260, 900), fill=accent)

    num_font = _font(168, bold=True)
    kicker_font = _font(28, bold=True)
    title_font = _font(54, bold=True)
    label = f"{module:02d}"
    num_w = draw.textlength(label, font=num_font)
    num_x = (W - num_w) / 2
    draw.text((num_x, 118), label, font=num_font, fill=WHITE)

    kicker = "MASTERING MONGODB"
    kick_w = draw.textlength(kicker, font=kicker_font)
    draw.text(((W - kick_w) / 2, 78), kicker, font=kicker_font, fill=(0xA5, 0xD6, 0xA7))

    lines = _wrap(draw, title, title_font, 980)
    y = 340
    for line in lines:
        line_w = draw.textlength(line, font=title_font)
        draw.text(((W - line_w) / 2, y), line, font=title_font, fill=WHITE)
        y += 68

    bar_w = 160
    draw.rounded_rectangle(((W - bar_w) / 2, 312, (W + bar_w) / 2, 322), radius=4, fill=accent)
    draw.text((48, H - 56), "Module quiz", font=_font(22, bold=True), fill=(220, 228, 240))
    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for module, title in MODULE_TITLES.items():
        path = OUT / f"module_{module:02d}.png"
        draw_cover(module, title).save(path, "PNG")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
