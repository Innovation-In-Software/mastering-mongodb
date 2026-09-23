#!/usr/bin/env python3
"""Shared PowerPoint chrome/rendering primitives for the Mastering MongoDB decks.

Palette, fonts, geometry, and every chrome-drawing function (rail, footer,
rotated page number, auto-shrinking title block, key-takeaway bar, panel
bullet/table styling, chapter/cover slide layout, fitted image placement) are
ported verbatim from the sibling MD287 project's
``scripts/md287_deck_kit.py`` -- the Innovation In Software house visual
system. Only the course name and content are specific to Mastering MongoDB;
every color, font, and layout constant below is a byte-for-byte copy of the
reference so the two course families render as one visual family.
"""
from __future__ import annotations

import io
import time
from pathlib import Path

from PIL import Image, ImageChops
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------------------
# Slide geometry -- ported verbatim from md287_deck_kit.py
# ---------------------------------------------------------------------------
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

RAIL_X = Inches(13.125)
RAIL_W = Inches(0.208)
RAIL_SPLIT_Y = Inches(1.5)

CONTENT_X = Inches(0.50)
CONTENT_W = Inches(12.05)  # stops clear of the rotated page number
TITLE_X = Inches(0.60)
TITLE_W = Inches(12.00)

# Minimum on-slide font size. The copyright footer (FOOTER_FONT_SIZE) is the
# only text allowed below it.
MIN_PT = 18.0  # body text size

FOOTER_FONT_SIZE = 14
FOOTER_BOX = (Inches(0.667), Inches(7.098), Inches(5.00), Inches(0.31))
NUMBER_BOX = (Inches(12.492), Inches(6.807), Inches(0.72), Inches(0.50))
# Everything above the copyright line (body content and the takeaway bar)
# ends here.
CONTENT_BOTTOM = Inches(7.02)
TAKEAWAY_H = Inches(0.56)
TAKEAWAY_Y = Inches(7.02 - 0.56)  # top of a one-line takeaway bar

SUBTITLE_Y = Inches(0.82)
SUBTITLE_W = Inches(12.30)
SUBTITLE_LINE_H = Inches(0.34)
CONTENT_TOP_MIN = Inches(0.66)
CONTENT_TOP_MAX = Inches(1.46)

# ---------------------------------------------------------------------------
# Brand constants -- Innovation In Software house theme (ported verbatim,
# hex-for-hex, from md287_deck_kit.py). Only COURSE_NAME differs.
# ---------------------------------------------------------------------------
FOOTER_TEXT = "© 2026 by Innovation In Software Corporation"
COURSE_NAME = "MASTERING MONGODB"

TITLE_FONT = "Leelawadee"
BODY_FONT = "Nirmala UI"
CODE_FONT = "Consolas"

RED = RGBColor(0xD1, 0x28, 0x2E)
NAVY = RGBColor(0x00, 0x20, 0x60)
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x80, 0x80, 0x80)
INK = RGBColor(0x00, 0x00, 0x00)
MUTED = RGBColor(0x59, 0x59, 0x59)
CARD_BG = RGBColor(0xF5, 0xF5, 0xF5)
CARD_LINE = RGBColor(0xE0, 0xE0, 0xE0)
TAKEAWAY_BG = RGBColor(0xFF, 0xF3, 0xE0)
TABLE_HEADER_BG = NAVY
GREEN = RGBColor(0x2E, 0x7D, 0x32)
PURPLE = RGBColor(0x5B, 0x3A, 0x9E)
ORANGE = RGBColor(0xC9, 0x69, 0x0C)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
BADGE_COLORS = (NAVY, GREEN, ORANGE, PURPLE, TEAL, RED)
TITLE_BADGE_COLORS = (PURPLE, NAVY, TEAL, GREEN)

NUMBER_SHAPE_NAME = "Diagram Page Number"


# ---------------------------------------------------------------------------
# Presentation / slide setup
# ---------------------------------------------------------------------------
def new_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_layout(prs: Presentation):
    return prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]


def _strip_placeholders(slide) -> None:
    for shape in list(slide.placeholders):
        shape._element.getparent().remove(shape._element)


def new_slide(prs: Presentation, layout):
    slide = prs.slides.add_slide(layout)
    _strip_placeholders(slide)
    return slide


# ---------------------------------------------------------------------------
# Low-level text/shape helpers
# ---------------------------------------------------------------------------
def add_textbox(slide, left, top, width, height, *, anchor=MSO_ANCHOR.TOP, wrap=True):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    for attr in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, attr, 0)
    return box


def add_run(paragraph, text, *, size, bold=False, italic=False, color=INK, font=BODY_FONT):
    run = paragraph.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if font:
        run.font.name = font
    return run


def add_rich_run(paragraph, segments, *, size, color=INK, font=BODY_FONT):
    """segments: list of (text, {'bold':bool,'italic':bool,'code':bool})."""
    for text, style in segments:
        if not text:
            continue
        add_run(
            paragraph, text,
            size=size,
            bold=style.get("bold", False),
            italic=style.get("italic", False),
            color=color,
            font=CODE_FONT if style.get("code") else font,
        )


def add_text(slide, left, top, width, height, text, *, size, bold=False, italic=False,
             color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=BODY_FONT):
    box = add_textbox(slide, left, top, width, height, anchor=anchor)
    lines = (text or "").split("\n") or [""]
    for i, line in enumerate(lines):
        p = box.text_frame.paragraphs[0] if i == 0 else box.text_frame.add_paragraph()
        p.alignment = align
        add_run(p, line, size=size, bold=bold, italic=italic, color=color, font=font)
    return box


def set_fill(shape, color, *, line_color=None, line_w=None):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_w or 0.75)


def set_notes(slide, text: str | None) -> None:
    if not text:
        return
    slide.notes_slide.notes_text_frame.text = text


# ---------------------------------------------------------------------------
# Rail / footer / rotated page number -- ported verbatim
# ---------------------------------------------------------------------------
def add_rail_and_footer(slide, page_num: int | None = None) -> None:
    top_rail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, RAIL_X, Emu(0), RAIL_W, RAIL_SPLIT_Y)
    set_fill(top_rail, RED)

    bottom_rail = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, RAIL_X, RAIL_SPLIT_Y, RAIL_W, Inches(6.0)
    )
    set_fill(bottom_rail, BLACK)

    if page_num is not None:
        footer = add_text(slide, *FOOTER_BOX, FOOTER_TEXT, size=FOOTER_FONT_SIZE, color=GRAY)
        footer.text_frame.word_wrap = False

        number_text = str(page_num)
        number_size = 23 if len(number_text) <= 2 else MIN_PT
        number = add_text(
            slide, *NUMBER_BOX, number_text, size=number_size, color=RED, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )
        number.text_frame.word_wrap = False
        number.rotation = 270
        number.name = NUMBER_SHAPE_NAME


# ---------------------------------------------------------------------------
# Title block with auto-shrink -- ported verbatim
# ---------------------------------------------------------------------------
def subtitle_line_count(subtitle: str | None) -> int:
    """Lines a 20pt italic subtitle wraps to across SUBTITLE_W."""
    if not subtitle:
        return 0
    chars_per_line = max(20, int(int(SUBTITLE_W) / 914400 / 0.146))
    return max(1, -(-len(subtitle) // chars_per_line))


TITLE_CHAR_W = 0.0095
TITLE_SIZES = (24, 22, 20)  # never below MIN_PT; a long title may take 3 lines at 20pt
MAX_TITLE_LINES = 2


def title_chars_per_line(size: float) -> int:
    return max(12, int(int(TITLE_W) / 914400 / (TITLE_CHAR_W * size)))


def title_line_count(header: str, size: float) -> int:
    return max(1, -(-len(header or "") // title_chars_per_line(size)))


def title_font_size(header: str) -> float:
    """Largest size that keeps the title within MAX_TITLE_LINES; floor MIN_PT."""
    for size in TITLE_SIZES:
        if title_line_count(header, size) <= MAX_TITLE_LINES:
            return size
    return TITLE_SIZES[-1]


def title_bottom(title: str | None) -> int:
    """Bottom edge of the title block -- long titles can run to two lines."""
    header = (title or "").upper()
    if not header:
        return int(Inches(0.84))
    size = title_font_size(header)
    line_h = int(Inches(size / 72 * 1.25))
    return int(Inches(0.14)) + title_line_count(header, size) * line_h


def content_top_for(subtitle: str | None, title: str | None = None) -> int:
    """Y where body content may start without colliding with title or subtitle."""
    top = int(CONTENT_TOP_MIN)
    lines = subtitle_line_count(subtitle)
    if lines:
        top = max(top, int(SUBTITLE_Y) + lines * int(SUBTITLE_LINE_H) + int(Inches(0.08)))
    else:
        top = max(top, title_bottom(title) + int(Inches(0.12)))
    return top


def add_title_block(slide, *, title, subtitle=None):
    header = (title or "").upper()
    size = title_font_size(header)
    add_text(
        slide, TITLE_X, Inches(0.14), TITLE_W, Inches(0.70), header,
        size=size, color=RED, bold=True, font=TITLE_FONT, anchor=MSO_ANCHOR.TOP,
    )
    if subtitle:
        lines = subtitle_line_count(subtitle)
        add_text(
            slide, TITLE_X, SUBTITLE_Y, SUBTITLE_W,
            max(int(Inches(0.42)), lines * int(SUBTITLE_LINE_H)), subtitle,
            size=MIN_PT, italic=True, color=MUTED,
        )
    return content_top_for(subtitle, title)


# ---------------------------------------------------------------------------
# Key takeaway bar -- ported verbatim
# ---------------------------------------------------------------------------
TAKEAWAY_PT = MIN_PT


def takeaway_height(text: str) -> int:
    """Bar height for this takeaway -- grows so long text is never clipped."""
    chars_per_line = max(30, int((int(CONTENT_W) - int(Inches(0.44))) / 914400 / (0.0072 * TAKEAWAY_PT)))
    lines = max(1, -(-(len(text or "") + 16) // chars_per_line))
    line_h = int(Inches(TAKEAWAY_PT / 72 * 1.25))
    return max(int(TAKEAWAY_H), line_h * lines + int(Inches(0.22)))


def add_key_takeaway(slide, text: str, top=None) -> int:
    """Cream rounded-rect bar bottom-anchored at CONTENT_BOTTOM; grows upward."""
    h = takeaway_height(text)
    y = int(CONTENT_BOTTOM) - h if top is None else int(top)
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, CONTENT_X, y, CONTENT_W, h)
    set_fill(bar, TAKEAWAY_BG)
    try:
        bar.adjustments[0] = 0.08
    except Exception:
        pass
    box = add_textbox(slide, int(CONTENT_X) + int(Inches(0.22)), y,
                      int(CONTENT_W) - int(Inches(0.44)), h, anchor=MSO_ANCHOR.MIDDLE)
    p = box.text_frame.paragraphs[0]
    add_run(p, "KEY TAKEAWAY   ", size=TAKEAWAY_PT, bold=True, color=RED)
    add_run(p, text, size=TAKEAWAY_PT, color=INK)
    return h


# ---------------------------------------------------------------------------
# Small circular icon badge -- ported verbatim
# ---------------------------------------------------------------------------
def icon_badge(slide, left, top, d, icon, bg, scale: float = 1.0):
    oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, d, d)
    set_fill(oval, bg)
    if icon:
        add_text(
            slide, left, top, d, d, icon, size=max(MIN_PT, 12 * scale), bold=True, color=WHITE,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=None,
        )


# ---------------------------------------------------------------------------
# Generic bullet-panel heading -- small colored dot badge + bold RED all-caps
# label (e.g. "KEY POINTS", "YOU WILL BE ABLE TO"), matching the reference
# theme's add_panel_bullets icon-badge pattern, ported here for the plain
# content-slide bullet panels that don't otherwise carry a heading.
# ---------------------------------------------------------------------------
PANEL_HEADING_H = int(Inches(0.42))
PANEL_HEADING_GAP = int(Inches(0.14))


def add_panel_heading(slide, x, y, width, label, *, badge_color=None, icon: str = "") -> int:
    """Small icon badge + bold RED label above a bullet panel. Returns height.

    ``icon`` is an actual emoji glyph (e.g. "🎯"), not text in the house font --
    icon_badge renders it with font=None so PowerPoint falls back to the
    system emoji font instead of coercing it into Nirmala UI (which has no
    color-emoji glyphs and would otherwise show a tofu box or nothing)."""
    badge_color = badge_color or RED
    d = int(Inches(0.40))
    dot_y = int(y) + (PANEL_HEADING_H - d) // 2
    icon_badge(slide, x, dot_y, d, icon, badge_color)
    text_x = int(x) + d + int(Inches(0.10))
    add_text(
        slide, text_x, y, max(int(Inches(1.0)), int(width) - d - int(Inches(0.10))),
        PANEL_HEADING_H, label, size=MIN_PT, bold=True, color=RED, anchor=MSO_ANCHOR.MIDDLE,
    )
    return PANEL_HEADING_H


# ---------------------------------------------------------------------------
# Callout cards -- light CARD_BG rounded-rect treatment for a standalone
# "**Label:** value" line (e.g. "Example:", "Use cases:", "Misconception:")
# that would otherwise float as a lone plain-text line in empty space. Short
# comma/·-separated values get their own chip row instead of one run-on line.
# ---------------------------------------------------------------------------
def _tint(color: RGBColor, amount: float = 0.80) -> RGBColor:
    """Blend `color` toward white by `amount` (0=no change, 1=white)."""
    r = int(color[0] + (255 - color[0]) * amount)
    g = int(color[1] + (255 - color[1]) * amount)
    b = int(color[2] + (255 - color[2]) * amount)
    return RGBColor(r, g, b)


CALLOUT_PAD = int(Inches(0.12))
CALLOUT_LABEL_PT = MIN_PT
# Callout-card value text is body text like any bullet/paragraph, so it
# shares the new 20pt default (was a fixed 13pt) -- CALLOUT_CHAR_W_PER_PT
# below is the same "0.082 in/char at 13pt" constant this used to hardcode,
# just re-expressed per-point so chars_per_line still scales correctly now
# that the font size can change.
CALLOUT_BODY_PT = MIN_PT
CALLOUT_CHAR_W_PER_PT = 0.082 / 13.0


def estimate_callout_text_height(width, label: str, plain_len: int, pt: float = CALLOUT_BODY_PT) -> int:
    inner_w = max(int(Inches(1.0)), int(width) - 2 * CALLOUT_PAD)
    chars_per_line = max(12, int(inner_w / 914400 / (CALLOUT_CHAR_W_PER_PT * pt)))
    total_len = int(len(label) * 1.15) + 4 + plain_len  # label is bold caps
    lines = max(1, -(-total_len // chars_per_line))
    line_h = int(Inches(pt / 72 * 1.22))
    return max(int(Inches(0.42)), lines * line_h + 2 * CALLOUT_PAD)


def add_callout_text_card(slide, x, y, width, label: str, segments, *, accent=None,
                          pt: float = CALLOUT_BODY_PT) -> int:
    """Card with an inline "LABEL   value" run (value as pre-split rich segments)."""
    accent = accent or RED
    plain_len = sum(len(t) for t, _ in segments)
    h = estimate_callout_text_height(width, label, plain_len, pt)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, h)
    set_fill(card, CARD_BG, line_color=CARD_LINE, line_w=0.75)
    try:
        card.adjustments[0] = 0.06
    except Exception:
        pass
    box = add_textbox(slide, int(x) + CALLOUT_PAD, y, int(width) - 2 * CALLOUT_PAD, h,
                       anchor=MSO_ANCHOR.MIDDLE)
    p = box.text_frame.paragraphs[0]
    add_run(p, f"{label.upper()}   ", size=pt, bold=True, color=accent)
    add_rich_run(p, segments, size=pt, color=INK)
    return h


CHIP_H = int(Inches(0.46))
CHIP_GAP_X = int(Inches(0.12))
CHIP_GAP_Y = int(Inches(0.10))
CHIP_PT = MIN_PT
CALLOUT_LABEL_H = int(Inches(0.36))


def _chip_width(text: str) -> int:
    return int(Inches(0.0072 * CHIP_PT * len(text) + 0.40))


def _chip_rows(inner_w: int, chips: list[str]) -> list[list[tuple[str, int]]]:
    rows: list[list[tuple[str, int]]] = []
    cur: list[tuple[str, int]] = []
    cur_w = 0
    for c in chips:
        w = min(_chip_width(c), inner_w)
        add_w = w + (CHIP_GAP_X if cur else 0)
        if cur and cur_w + add_w > inner_w:
            rows.append(cur)
            cur, cur_w = [], 0
            add_w = w
        cur.append((c, w))
        cur_w += add_w
    if cur:
        rows.append(cur)
    return rows


def estimate_callout_chip_height(width, label: str, chips: list[str]) -> int:
    inner_w = max(int(Inches(1.0)), int(width) - 2 * CALLOUT_PAD)
    rows = _chip_rows(inner_w, chips)
    label_h = CALLOUT_LABEL_H
    chip_block_h = len(rows) * CHIP_H + max(0, len(rows) - 1) * CHIP_GAP_Y
    return 2 * CALLOUT_PAD + label_h + int(Inches(0.06)) + chip_block_h


def add_callout_chip_card(slide, x, y, width, label: str, chips: list[str], *,
                           accent=None, badge_start: int = 0) -> int:
    """Card with a bold RED label line, then a wrapping row of small chips."""
    accent = accent or RED
    h = estimate_callout_chip_height(width, label, chips)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, h)
    set_fill(card, CARD_BG, line_color=CARD_LINE, line_w=0.75)
    try:
        card.adjustments[0] = 0.06
    except Exception:
        pass
    add_text(
        slide, int(x) + CALLOUT_PAD, int(y) + int(Inches(0.05)),
        int(width) - 2 * CALLOUT_PAD, CALLOUT_LABEL_H,
        label.upper(), size=CALLOUT_LABEL_PT, bold=True, color=accent,
    )
    inner_w = int(width) - 2 * CALLOUT_PAD
    rows = _chip_rows(inner_w, chips)
    ry = int(y) + CALLOUT_PAD + CALLOUT_LABEL_H + int(Inches(0.06))
    for row in rows:
        rx = int(x) + CALLOUT_PAD
        for i, (text, w) in enumerate(row):
            color = BADGE_COLORS[(badge_start + i) % len(BADGE_COLORS)]
            chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, ry, w, CHIP_H)
            set_fill(chip, _tint(color))
            try:
                chip.adjustments[0] = 0.5
            except Exception:
                pass
            add_text(
                slide, rx, ry, w, CHIP_H, text, size=CHIP_PT, bold=True, color=color,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            )
            rx += w + CHIP_GAP_X
        ry += CHIP_H + CHIP_GAP_Y
    return h


# ---------------------------------------------------------------------------
# Bullet marker / enumerator / lead-in styling -- ported verbatim
# ---------------------------------------------------------------------------
import re  # noqa: E402  (kept near point of use, mirroring the reference file)

ENUMERATOR = re.compile(r"^\s*(\d{1,2}[.)])\s+")


def split_enumerator(text: str) -> tuple[str, str]:
    """("1.", "rest") when the bullet text already starts with its own number."""
    match = ENUMERATOR.match(text or "")
    if match:
        return match.group(1), text[match.end():]
    return "", text


LEAD_IN = re.compile(r"^([^:]{2,60}):\s+(?=\S)")


def split_lead_in(text: str) -> tuple[str, str]:
    """("Build with Spring Boot", "rest") for bullets written as "Label: rest".

    Only a short label at the very start counts -- not a colon that turns up
    mid-sentence, and not a URL scheme (those have no space after the colon).
    """
    match = LEAD_IN.match(text or "")
    if not match:
        return "", text
    label = match.group(1).strip()
    if ". " in label or label.endswith("."):
        return "", text
    return label, text[match.end():]


def is_standard_or_emoji_marker(marker: str) -> bool:
    """True for plain bullets and emoji-only markers (render as a standard bullet)."""
    m = (marker or "").strip()
    if m in ("▪", "-", "•", ""):
        return True
    cps = [ord(ch) for ch in m]
    joiners = {0x200D, 0xFE0E, 0xFE0F, 0x20E3}
    if not cps or cps[0] in joiners:
        return False

    def emoji_cp(cp: int) -> bool:
        return (
            cp in joiners
            or 0x1F3FB <= cp <= 0x1F3FF
            or 0x1F000 <= cp <= 0x1FAFF
            or 0x2600 <= cp <= 0x27BF
            or 0x2300 <= cp <= 0x23FF
            or 0x2B50 <= cp <= 0x2B55
            or 0x1F1E6 <= cp <= 0x1F1FF
        )

    return all(emoji_cp(cp) for cp in cps)


# ---------------------------------------------------------------------------
# Table rendering -- navy header / zebra CARD_BG rows / bold first column
# ---------------------------------------------------------------------------
def _cell_chars_per_line(col_width: int, scale: float = 1.0) -> int:
    usable = max(int(Inches(0.45)), int(col_width) - int(Inches(0.20)))
    return max(6, int(usable / 914400 / (0.078 * scale)))


def packed_table_widths(headers, rows, max_width, scale: float = 1.0) -> list[int]:
    n = len(headers)
    max_lens = [len(str(headers[c])) for c in range(n)]
    for row in rows:
        for c, val in enumerate(row):
            if c < n:
                max_lens[c] = max(max_lens[c], len(str(val)))
    raw = [
        max(int(Inches(1.15 * scale)), min(int(Inches(4.4)), int(Inches((0.11 * L + 0.40) * scale))))
        for L in max_lens
    ]
    total = sum(raw)
    max_w = int(max_width)
    long_cells = any(L > 22 for L in max_lens)
    if long_cells:
        s = max_w / max(total, 1)
        raw = [max(int(Inches(1.05)), int(w * s)) for w in raw]
        raw[-1] += max_w - sum(raw)
    elif total > max_w:
        s = max_w / total
        raw = [max(int(Inches(0.90)), int(w * s)) for w in raw]
    elif total < max_w:
        raw[-1] += max_w - total
    return raw


def _table_row_heights(headers, rows, col_w, scale: float = 1.0) -> list[int]:
    unit = int(Inches(0.26) * scale)
    pad = int(Inches(0.10) * scale)

    header_lines = 1
    for c, val in enumerate(headers):
        if c < len(col_w):
            cpi = _cell_chars_per_line(col_w[c], scale)
            header_lines = max(header_lines, max(1, -(-len(str(val)) // cpi)))
    heights = [max(int(Inches(0.30) * scale), unit * header_lines + pad)]

    for row in rows:
        widest = 1
        for c, val in enumerate(row):
            if c >= len(col_w):
                continue
            cpi = _cell_chars_per_line(col_w[c], scale)
            widest = max(widest, max(1, -(-len(str(val)) // cpi)))
        heights.append(unit * widest + pad)
    return heights


def estimate_table_height(headers, rows, width, scale: float = 1.0) -> int:
    col_w = packed_table_widths(headers, rows, width, scale)
    return sum(_table_row_heights(headers, rows, col_w, scale))


TABLE_PT = 12.0
# Table geometry is expressed at 12pt and scaled; MIN_TABLE_SCALE puts cell
# text at MIN_PT.
MIN_TABLE_SCALE = MIN_PT / TABLE_PT


def add_table(slide, left, top, width, headers, rows, *, scale: float = 1.0, table_pt: float | None = None):
    table_pt = TABLE_PT if table_pt is None else table_pt
    col_w = packed_table_widths(headers, rows, width, scale)
    table_w = sum(col_w)
    row_heights = _table_row_heights(headers, rows, col_w, scale)
    table_h = sum(row_heights)
    n_rows = len(rows) + 1
    n_cols = len(headers)
    graphic_frame = slide.shapes.add_table(n_rows, n_cols, left, top, table_w, table_h)
    table = graphic_frame.table
    for c, w in enumerate(col_w):
        table.columns[c].width = w
    for r, h in enumerate(row_heights):
        table.rows[r].height = h

    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = str(h)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TABLE_HEADER_BG
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            for r_ in p.runs:
                r_.font.size = Pt(table_pt * scale)
                r_.font.bold = True
                r_.font.color.rgb = WHITE
                r_.font.name = BODY_FONT

    for ridx, row in enumerate(rows, start=1):
        bg = WHITE if ridx % 2 else CARD_BG
        for c in range(n_cols):
            val = row[c] if c < len(row) else ""
            cell = table.cell(ridx, c)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            for p in cell.text_frame.paragraphs:
                for r_ in p.runs:
                    r_.font.size = Pt(table_pt * scale)
                    r_.font.bold = c == 0
                    r_.font.color.rgb = INK
                    r_.font.name = BODY_FONT
    return table_h


# ---------------------------------------------------------------------------
# Code block rendering -- Consolas card using CARD_BG/CARD_LINE
# ---------------------------------------------------------------------------
CODE_LINE_SPACING = 0.90  # PowerPoint line-spacing multiple for code cards


def estimate_code_height(code_text: str, width: int, font_pt: float) -> int:
    lines = (code_text or "").split("\n") or [""]
    usable = max(1, int(width) - int(Inches(0.28)))
    chars_per_line = max(12, int(usable / 914400 / (0.0083 * font_pt)))
    wrapped = 0
    for line in lines:
        wrapped += max(1, -(-max(len(line), 1) // chars_per_line))
    line_h = int(Inches(font_pt / 72 * 1.17 * CODE_LINE_SPACING))
    return wrapped * line_h + int(Inches(0.24))


def add_code_block(slide, left, top, width, height, code_text: str, *, font_pt: float = MIN_PT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_fill(card, CARD_BG, line_color=CARD_LINE, line_w=0.75)
    try:
        card.adjustments[0] = 0.04
    except Exception:
        pass
    box = add_textbox(slide, int(left) + int(Inches(0.14)), int(top) + int(Inches(0.10)),
                       int(width) - int(Inches(0.28)), int(height) - int(Inches(0.18)))
    tf = box.text_frame
    tf.word_wrap = True
    lines = (code_text or "").split("\n") or [""]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(0)
        p.space_before = Pt(0)
        p.line_spacing = CODE_LINE_SPACING
        add_run(p, line if line else " ", size=font_pt, color=INK, font=CODE_FONT)
    return box


# ---------------------------------------------------------------------------
# Image fitting -- uniform scale, never stretched, centered, with an optional
# whitespace-margin autocrop and thin CARD_LINE frame.
# ---------------------------------------------------------------------------
def _load_trimmed(path: Path):
    with Image.open(path) as src:
        img = src.convert("RGB")
        diff = ImageChops.difference(img, Image.new("RGB", img.size, (255, 255, 255)))
        bbox = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
        if bbox:
            pad = 6
            left, top, right, bottom = bbox
            img = img.crop((
                max(0, left - pad), max(0, top - pad),
                min(img.width, right + pad), min(img.height, bottom + pad),
            ))
        stream = io.BytesIO()
        img.save(stream, format="PNG", optimize=True, compress_level=9)
        stream.seek(0)
        return stream, img.width, img.height


def add_picture_fitted(slide, path: Path, box_x, box_y, box_w, box_h, *, border=True):
    """Place an image aspect-fit and centered within the given box.

    Technique ported from md287_deck_kit.add_picture_fitted: scale uniformly
    to the limiting dimension, never distort, center in the remaining space.
    This course's diagram slides use a side-by-side bullets/diagram panel
    rather than the reference's full-bleed diagram-only layout, so the box is
    the split-panel's image column instead of the reference's fixed
    DIAGRAM_LEFT/RIGHT/TOP/BOTTOM full-slide box -- same principle, different
    box.
    """
    try:
        stream, iw, ih = _load_trimmed(path)
    except Exception:
        with Image.open(path) as im:
            iw, ih = im.size
        stream = str(path)

    scale = min(int(box_w) / iw, int(box_h) / ih)
    w = max(1, int(iw * scale))
    h = max(1, int(ih * scale))
    x = int(box_x) + (int(box_w) - w) // 2
    y = int(box_y) + (int(box_h) - h) // 2

    if border:
        frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x - Emu(9525), y - Emu(9525),
                                        w + Emu(19050), h + Emu(19050))
        set_fill(frame, WHITE, line_color=CARD_LINE, line_w=0.75)
    pic = slide.shapes.add_picture(stream, x, y, width=w, height=h)
    return pic


# ---------------------------------------------------------------------------
# Cover-slide topic-chip row -- ported from md287_deck_kit's module-title
# chip row: a row of up to 5 colored rounded-rectangle chips under the
# subtitle, one short topic label each, cycling through BADGE_COLORS. Sized
# so 5 chips at CHIP_ROW_W with CHIP_ROW_GAP between them exactly fill
# CONTENT_W (12.30in), matching the reference's own proportions.
# ---------------------------------------------------------------------------
CHIP_ROW_W = int(Inches(2.34))
CHIP_ROW_GAP = int(Inches(0.15))
CHIP_ROW_H = int(Inches(1.05))
CHIP_ROW_PT_STEPS = (MIN_PT,)


def _chip_row_font_size(label: str, width: int) -> float:
    inner_w = max(int(Inches(0.6)), int(width) - int(Inches(0.10)))
    for pt in CHIP_ROW_PT_STEPS:
        chars_per_line = max(8, int(inner_w / 914400 / (CALLOUT_CHAR_W_PER_PT * pt)))
        line_h = Inches(pt / 72 * 1.32) / 914400
        max_lines = max(1, int(int(CHIP_ROW_H) / 914400 / line_h) - 1)
        lines = max(1, -(-len(label) // chars_per_line))
        if lines <= max_lines:
            return pt
    return CHIP_ROW_PT_STEPS[-1]


def add_topic_chip_row(slide, chips: list[str], y) -> int:
    """Row of up to 5 topic chips (rounded rect, house color, bold white
    centered label) -- the cover-slide "what this module covers at a
    glance" strip. Returns the row height actually used."""
    chips = [c for c in (chips or []) if c][:5]
    if not chips:
        return 0
    y = int(y)
    for i, label in enumerate(chips):
        color = BADGE_COLORS[i % len(BADGE_COLORS)]
        x = int(CONTENT_X) + i * (CHIP_ROW_W + CHIP_ROW_GAP)
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, CHIP_ROW_W, CHIP_ROW_H)
        set_fill(chip, color)
        try:
            chip.adjustments[0] = 0.12
        except Exception:
            pass
        pt = _chip_row_font_size(label, CHIP_ROW_W)
        add_text(
            slide, x + int(Inches(0.06)), y, CHIP_ROW_W - int(Inches(0.12)), CHIP_ROW_H,
            label, size=pt, bold=True, color=WHITE,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )
    return CHIP_ROW_H


# ---------------------------------------------------------------------------
# Chapter / cover slide -- white background, ported verbatim from
# md287_deck_kit._chapter_slide (module-divider / course-title layout).
# ---------------------------------------------------------------------------
def chapter_slide(prs, layout, *, title, subtitle=None,
                   quote=None, icons=None, chips=None, notes: str | None = None):
    slide = new_slide(prs, layout)
    add_rail_and_footer(slide, page_num=None)

    if quote:
        add_text(
            slide, Inches(8.14), Inches(0.12), Inches(3.90), Inches(0.40), quote,
            size=MIN_PT, italic=True, color=MUTED, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
        )
    add_text(
        slide, CONTENT_X, Inches(2.15), Inches(12.30), Inches(1.90), title,
        size=40, bold=True, color=RED, font=TITLE_FONT,
    )
    if subtitle:
        add_text(
            slide, CONTENT_X, Inches(4.10), Inches(12.30), Inches(0.90), subtitle,
            size=MIN_PT, color=NAVY,
        )
    # Chips (module topic strip) and icons (small decorative glyphs) share
    # the band between the subtitle (bottom ~5.10in) and the footer
    # (top 6.75in) -- when both are present, icons shrink and sit just above
    # the chip row instead of at their old fixed 0.70in size, so the two
    # never overlap.
    band_y = Inches(5.15)
    if icons:
        icon_d = Inches(0.45) if chips else Inches(0.70)
        for i, ic in enumerate(icons[:4]):
            if isinstance(ic, dict):
                glyph = ic.get("icon", "")
                bg = ic.get("color", TITLE_BADGE_COLORS[i % len(TITLE_BADGE_COLORS)])
            else:
                glyph, bg = ic, TITLE_BADGE_COLORS[i % len(TITLE_BADGE_COLORS)]
            cx = int(CONTENT_X) + i * int(icon_d + Inches(0.15))
            oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, band_y, icon_d, icon_d)
            set_fill(oval, bg)
            if glyph:
                add_text(
                    slide, cx, band_y, icon_d, icon_d, glyph,
                    size=22 if not chips else MIN_PT, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE, font=None,
                )
        if chips:
            band_y = band_y + icon_d + Inches(0.12)
    if chips:
        add_topic_chip_row(slide, chips, band_y)
    if notes:
        set_notes(slide, notes)
    return slide


# ---------------------------------------------------------------------------
# Save with retry
# ---------------------------------------------------------------------------
def save_presentation(prs, out_path: Path, attempts: int = 6) -> None:
    """Save, retrying briefly.

    On Windows a sync client or indexer can hold a freshly written .pptx for a
    moment, which surfaces as OSError(EINVAL) from the zip writer.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, attempts + 1):
        try:
            prs.save(str(out_path))
            return
        except OSError:
            if attempt == attempts:
                raise
            time.sleep(0.8 * attempt)
