"""Shared SVG helpers for Marp slide diagrams."""

from __future__ import annotations

import html
import re

RED = "#cc0000"
TEXT = "#1a1a1a"
MUTED = "#666666"
BG = "#ffffff"
PANEL = "#f7f7f7"
HEADER_BG = "#ffebeb"
BORDER = "#d0d0d0"
FONT = "Arial, Helvetica, sans-serif"
MONO = "Consolas, 'Courier New', monospace"

FS_TITLE = 26
FS_HEADING = 24
FS_BODY = 22
FS_SMALL = 20
FS_MONO = 23

HEADER_H = 54
HEADER_GAP = 16
ROW_H = 46
PANEL_PAD = 16


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "diagram"


def _text_baseline_in_box(box_y: float, box_h: float, font_size: float) -> float:
    return box_y + box_h / 2 + font_size * 0.35


def monospace_panel_svg(
    lines: list[str],
    width: int = 920,
    *,
    max_panel_height: int = 500,
    font_size: float | None = None,
) -> str:
    """Render monospace ASCII block on a fixed character grid inside a panel."""
    pad_x = 24
    pad_y = 24
    fs = font_size or FS_MONO
    char_w = fs * 0.62
    line_h = fs * 1.45
    max_len = max((len(line) for line in lines), default=0)
    content_w = max_len * char_w
    width = max(width, int(pad_x * 2 + content_w))
    height = int(pad_y * 2 + len(lines) * line_h)

    if height > max_panel_height:
        scale = max_panel_height / height
        fs *= scale
        char_w = fs * 0.62
        line_h = fs * 1.45
        height = int(pad_y * 2 + len(lines) * line_h)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" rx="10" ry="10" fill="{PANEL}" '
        f'stroke="{BORDER}" stroke-width="2"/>',
    ]
    y = pad_y + fs * 0.85
    for line in lines:
        parts.append(
            f'<text x="{pad_x}" y="{y}" text-anchor="start" '
            f'font-family="{MONO}" font-size="{fs:.2f}" fill="{TEXT}">'
            f"{html.escape(line)}</text>"
        )
        y += line_h
    parts.append("</svg>")
    return "\n".join(parts)


def lines_from_monospace_svg(svg_text: str) -> list[str]:
    """Recover source lines from a previously generated monospace panel SVG."""
    import html as html_mod

    rows: dict[float, list[tuple[float, str]]] = {}
    for match in re.finditer(
        r'<text x="([0-9.]+)" y="([0-9.]+)"([^>]*)>([^<]*)</text>', svg_text
    ):
        x, y = float(match.group(1)), float(match.group(2))
        attrs, text = match.group(3), html_mod.unescape(match.group(4))
        if 'text-anchor="start"' in attrs or len(text) > 1:
            rows.setdefault(y, []).append((x, text))
            continue
        rows.setdefault(y, []).append((x, text))

    lines: list[str] = []
    char_w = FS_MONO * 0.62
    pad_x = 24
    for y in sorted(rows):
        chars = sorted(rows[y], key=lambda item: item[0])
        if len(chars) == 1:
            lines.append(chars[0][1])
            continue
        if all(len(ch) > 1 for _, ch in chars):
            lines.extend(ch for _, ch in chars)
            continue
        max_col = 0
        grid: dict[int, str] = {}
        for x, ch in chars:
            col = round((x - pad_x) / char_w)
            grid[col] = ch
            max_col = max(max_col, col)
        line = "".join(grid.get(i, " ") for i in range(max_col + 1)).rstrip()
        lines.append(line)
    return lines
