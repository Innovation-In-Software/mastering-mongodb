#!/usr/bin/env python3
"""Manifest-record -> pptx-slide renderer for the Mastering MongoDB decks.

Consumes one slide record from scripts/marp_manifests/*.json (schema:
global_index, marp_class, heading, body_markdown, notes, diagram_png) and
draws the corresponding native PowerPoint slide using the chrome/primitives
in mongodb_deck_kit.py, restyled to match the Innovation In Software house
theme (ported from the sibling MD287 project's md287_deck_kit.py):

- ``lead`` records (module/course openers) -> the white-background
  ``K.chapter_slide`` cover layout (no tag or byline).
- Everything between two covers -> one packed flow (render_flow): topics
  run on from slide to slide at a fixed 18pt body size (tables and code
  14pt), a topic starting
  mid-slide gets a bold red subheading, a slide opening mid-topic is titled
  "<topic> (cont.)", diagrams float at the right of their topic's text,
  short lists run in two columns, and key takeaways are inline cards.

Consecutive "X" / "X (cont.)" source records (and an exercise/lab intro and
its step records) are merged into one topic first (merge_continuations).
Nothing is dropped: every block is drawn, and only identical repeated
blocks within a merged topic are shown once. Each slide's speaker notes hold
the notes of every topic that starts on it. Titles are 20-24pt, and "Innovation In Software" appears nowhere but that
footer.

All slides get the red/black right-edge rail, copyright footer, and rotated
red page number via ``K.add_rail_and_footer``. render_record (one record ->
its own slides) is still used for cover slides.
"""
from __future__ import annotations

import re
from pathlib import Path

from pptx.util import Inches, Pt

import mongodb_deck_kit as K

# ---------------------------------------------------------------------------
# Inline markdown helpers
# ---------------------------------------------------------------------------
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_TICK_RE = re.compile(r"`([^`]*)`")


def strip_markdown_title(text: str | None) -> str:
    """Plain text for titles: drop backticks/bold/link syntax, keep the words."""
    text = text or ""
    text = _LINK_RE.sub(r"\1", text)
    text = _BOLD_RE.sub(r"\1", text)
    text = text.replace("`", "")
    return text.strip()


def flatten_markdown(text: str | None) -> str:
    """Plain multi-line text for lead-slide subtitles: strip markdown syntax."""
    out = []
    for line in (text or "").split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^#{1,6}\s*", "", line)
        line = _LINK_RE.sub(r"\1", line)
        line = _BOLD_RE.sub(r"\1", line)
        line = _TICK_RE.sub(r"\1", line)
        line = line.strip("_")
        out.append(line)
    return "\n".join(out)


_INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|_[^_]+_)")


def parse_inline(text: str) -> list[tuple[str, dict]]:
    """Split a line into (text, style) runs for **bold**, `code`, _italic_."""
    text = _LINK_RE.sub(r"\1", text or "")
    segments: list[tuple[str, dict]] = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            segments.append((text[pos:m.start()], {}))
        token = m.group(0)
        if token.startswith("**"):
            segments.append((token[2:-2].replace("`", ""), {"bold": True}))
        elif token.startswith("`"):
            segments.append((token[1:-1], {"code": True}))
        else:
            # Italic spans aren't re-tokenized for nested markers, so at least
            # strip any bold/tick syntax that would otherwise leak through as
            # literal asterisks/backticks.
            inner = _BOLD_RE.sub(r"\1", token[1:-1])
            inner = inner.replace("`", "")
            segments.append((inner, {"italic": True}))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], {}))
    return segments or [("", {})]


# ---------------------------------------------------------------------------
# Markdown block parser
# ---------------------------------------------------------------------------
_SEP_ROW_RE = re.compile(r"^:?-+:?$")
_BULLET_RE = re.compile(r"^(\s*)-\s+(.*)$")
_NUM_RE = re.compile(r"^(\s*)(\d{1,2}[.)])\s+(.*)$")


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_separator_row(line: str) -> bool:
    s = line.strip()
    if "|" not in s and "-" not in s:
        return False
    parts = [p.strip() for p in s.strip("|").split("|")]
    parts = [p for p in parts if p != ""]
    return bool(parts) and all(_SEP_ROW_RE.match(p) for p in parts)


def extract_col_text(body: str) -> tuple[str, bool]:
    """(text, was_split) -- pull the col-text panel out of a split-layout div."""
    m = re.search(r'<div\s+class="col-text">(.*?)</div>\s*<div\s+class="col-visual">',
                  body or "", re.S)
    if m:
        return m.group(1), True
    return body or "", False


def parse_blocks(text: str) -> list[dict]:
    """Parse markdown body text into an ordered list of block dicts.

    Block shapes: {'type': 'bullets', 'items': [(level, kind, marker, text), ...]}
                  {'type': 'table', 'headers': [...], 'rows': [[...], ...]}
                  {'type': 'code', 'lang': str, 'text': str}
                  {'type': 'keymsg', 'text': str}
    """
    lines = (text or "").replace("\r\n", "\n").split("\n")
    n = len(lines)
    blocks: list[dict] = []
    i = 0
    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if stripped == "":
            i += 1
            continue

        # HTML div wrapper leftovers (e.g. unmatched </div>, <div class="cols">)
        if re.match(r"^</?div\b", stripped) or re.match(r"^<img\b", stripped):
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(code_lines).rstrip("\n")})
            continue

        # Blockquote -- rendered as a "KEY TAKEAWAY" callout bar, same
        # treatment as an explicit "**Key message:**" paragraph below.
        if stripped.startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            quote_text = " ".join(l.strip() for l in quote_lines if l.strip())
            blocks.append({"type": "keymsg", "text": strip_markdown_title(quote_text)})
            continue

        # Markdown table: header row followed by a separator row
        if stripped.startswith("|") and i + 1 < n and _is_separator_row(lines[i + 1]):
            headers = [strip_markdown_title(c) for c in _split_row(lines[i])]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([strip_markdown_title(c) for c in _split_row(lines[i])])
                i += 1
            blocks.append({"type": "table", "headers": headers, "rows": rows})
            continue

        # Bullet / numbered list run
        if _BULLET_RE.match(raw) or _NUM_RE.match(raw):
            items: list[tuple[int, str, str, str]] = []
            while i < n:
                line = lines[i]
                s = line.strip()
                if s == "":
                    break
                mb = _BULLET_RE.match(line)
                mn = _NUM_RE.match(line)
                if mb:
                    level = min(2, len(mb.group(1)) // 2)
                    items.append((level, "bullet", "•", mb.group(2)))
                    i += 1
                elif mn:
                    level = min(2, len(mn.group(1)) // 2)
                    items.append((level, "number", mn.group(2), mn.group(3)))
                    i += 1
                elif re.match(r"^</?div\b|^<img\b", s):
                    i += 1
                elif s.startswith(">"):
                    break
                elif s.startswith("```") or (s.startswith("|") and i + 1 < n and _is_separator_row(lines[i + 1])):
                    break
                else:
                    # continuation / lead-in line attached to the list (e.g. a bold
                    # "**Step 1 ...**" sub-heading between bullets)
                    items.append((0, "para", "", s))
                    i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        # Generic paragraph run -- collect until a blank line or a new block type
        para_lines = []
        while i < n:
            s = lines[i].strip()
            if s == "" or s.startswith("```") or s.startswith(">") \
                    or _BULLET_RE.match(lines[i]) or _NUM_RE.match(lines[i]):
                break
            if re.match(r"^</?div\b|^<img\b", s):
                i += 1
                continue
            if s.startswith("|") and i + 1 < n and _is_separator_row(lines[i + 1]):
                break
            para_lines.append(s)
            i += 1
        para_text = " ".join(para_lines).strip()
        if not para_text:
            continue
        if re.match(r"^\*\*key message:\*\*", para_text, re.I):
            rest = re.sub(r"^\*\*key message:\*\*\s*", "", para_text, flags=re.I)
            blocks.append({"type": "keymsg", "text": strip_markdown_title(rest)})
        else:
            # A stray markdown heading ("### Advantages of ...") shows as a bold line.
            heading = re.match(r"^#{1,6}\s+(.*)$", para_text)
            if heading:
                para_text = f"**{strip_markdown_title(heading.group(1))}**"
            blocks.append({"type": "bullets", "items": [(0, "para", "", para_text)]})

    return _dedupe_repeated_blocks(blocks)


def _block_signature(b: dict):
    if b["type"] == "bullets":
        return ("bullets", tuple(b["items"]))
    if b["type"] == "table":
        return ("table", tuple(b["headers"]), tuple(tuple(r) for r in b["rows"]))
    if b["type"] == "code":
        return ("code", b["text"])
    if b["type"] == "keymsg":
        return ("keymsg", b["text"])
    if b["type"] in ("diagram", "float"):
        return (b["type"], str(b["path"]))
    return ("unknown",)


def _dedupe_repeated_blocks(blocks: list[dict]) -> list[dict]:
    """Drop exact-duplicate blocks that already appeared earlier in the slide.

    A source-manifest generation quirk repeats whole "Step N ..." bullet
    groups several times over in a small number of lab/exercise records
    (~80 of 1052 slides). Rather than silently truncating or crashing on the
    resulting overflow, keep the first occurrence of each distinct block and
    drop later exact repeats, which collapses those records back down to
    their intended single copy while leaving normal (non-repeating) slides
    completely untouched.
    """
    seen = set()
    out = []
    for b in blocks:
        sig = _block_signature(b)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(b)
    return out


def pop_keymsg(blocks: list[dict]) -> tuple[list[dict], str | None]:
    """Pull the keymsg blocks out; together they render as one slide-level
    KEY TAKEAWAY bar pinned to the bottom, not inline with the other blocks."""
    out = []
    msgs: list[str] = []
    for b in blocks:
        if b["type"] == "keymsg":
            if b["text"] and b["text"] not in msgs:
                msgs.append(b["text"])
            continue
        out.append(b)
    return out, (" ".join(msgs) or None)


# ---------------------------------------------------------------------------
# Brand scrub -- "Innovation In Software" appears on slides only in the
# copyright footer, never in slide body text.
# ---------------------------------------------------------------------------
_BRAND_RES = (
    re.compile(r"Innovation In Software(?: Corporation)?\s*[·•|]\s*", re.I),
    re.compile(r"\s*[·•|]\s*Innovation In Software(?: Corporation)?", re.I),
    re.compile(r"\s*\bInnovation In Software(?: Corporation)?\b\s*", re.I),
)


def scrub_brand(text: str | None) -> str | None:
    if not text:
        return text
    for rx in _BRAND_RES:
        text = rx.sub(" " if rx is _BRAND_RES[2] else "", text)
    return text


# ---------------------------------------------------------------------------
# Continuation merge -- the source splits many topics into "X", "X (cont.)",
# "X (cont.)" records holding a few lines each. Consecutive records on the
# same topic are merged into one flow and re-paginated to fill each slide.
# ---------------------------------------------------------------------------
_CONT_RE = re.compile(r"\s*\((?:cont(?:inued)?\.?)\)\s*$", re.I)


def base_heading(heading: str | None) -> str:
    return _CONT_RE.sub("", (heading or "").strip())


# "Lab 7.8 — Analyze Query Routing", "Lab 7.8 — Steps 1–2", ... are one activity.
_ACTIVITY_RE = re.compile(r"^((?:exercise|lab|demo|challenge)\s+\d+(?:\.\d+)*)\b", re.I)


def _activity_id(heading: str) -> str | None:
    m = _ACTIVITY_RE.match(strip_markdown_title(heading or ""))
    return m.group(1).lower() if m else None


def merge_continuations(records: list[dict]) -> list[dict]:
    """Merge consecutive records on the same topic: the same heading apart
    from "(cont.)", or the same exercise / lab / demo number."""
    out: list[dict] = []
    for r in records:
        is_lead = (r.get("marp_class") or "").strip() == "lead"
        base = base_heading(r.get("heading"))
        prev = out[-1] if out else None
        same_activity = prev is not None and _activity_id(base) is not None \
            and _activity_id(base) == _activity_id(prev.get("heading"))
        if (prev is not None and not is_lead and base
                and (prev.get("marp_class") or "").strip() != "lead"
                and (base_heading(prev.get("heading")) == base or same_activity)):
            prev["_parts"].append(r)
            continue
        out.append({**r, "heading": base or r.get("heading"), "_parts": [r]})
    return out


# ---------------------------------------------------------------------------
# Sizing heuristics (character-count based -- no font-metrics dependency)
#
# Body text never goes below K.MIN_PT (20pt). Each slide group picks the
# largest size from PT_LADDER that doesn't need more slides than 20pt would,
# so sparse content grows to fill the slide instead of leaving it empty.
# Content that doesn't fit one slide continues on "(cont.)" slides.
# ---------------------------------------------------------------------------
CHAR_W = 0.0066  # inches per point per character, ~Nirmala UI (calibrated against a render)

PT_LADDER = (28, 26, 24, 22, 20)
MAX_TABLE_PT = 24
MAX_CODE_PT = 24
BULLET_SPACE_AFTER = 0.20  # of the font size
LINE_SPACING = 0.90  # PowerPoint line-spacing multiple for body text (Nirmala UI has generous leading)
FIT_MARGIN = 0.97  # leave a little slack instead of maxing out to the pixel
GAP = int(Inches(0.08))
CONT_SUFFIX = " (cont.)"
IMAGE_MIN_H = int(Inches(2.6))  # a diagram never shrinks below this to share a slide


CODE_PT = 14.0   # code blocks
TABLE_PT = 14.0  # table cells


def _code_pt(pt) -> float:
    return CODE_PT


def _table_scale(pt) -> float:
    return TABLE_PT / K.TABLE_PT


def _chars_per_line(width, pt) -> int:
    return max(10, int(int(width) / 914400 / (CHAR_W * pt)))


def _item_lines(item, width, pt) -> int:
    level, kind, marker, text = item
    indent_w = int(Inches(0.28)) * level
    usable = max(int(Inches(1.0)), int(width) - indent_w - int(Inches(0.32)))
    return _wrapped_lines(text, _chars_per_line(usable, pt) - 3)


def _wrapped_lines(text: str, cpl: int) -> int:
    """Lines `text` wraps to, simulating word wrap. Widths are in body-font
    characters: inline `code` (Consolas) and **bold** runs are wider than
    regular Nirmala UI text, and a word never splits across lines unless it
    is longer than a whole line."""
    words: list[float] = []
    for seg, style in parse_inline(text):
        weight = 1.32 if style.get("code") else 1.08 if style.get("bold") else 1.0
        for w in seg.split():
            words.append(len(w) * weight)
    cpl = max(8, cpl)
    lines, cur = 1, 0.0
    for w in words:
        need = w if cur == 0 else cur + 1 + w
        if need <= cpl:
            cur = need
            continue
        if cur > 0:
            lines += 1
        while w > cpl:  # an over-long token breaks mid-word
            lines += 1
            w -= cpl
        cur = w
    return lines


def estimate_bullets_height(items, width, pt) -> int:
    line_h = int(Inches(pt / 72 * 1.2 * LINE_SPACING))
    h = int(Inches(0.03))
    for item in items:
        h += _item_lines(item, width, pt) * line_h + int(Pt(pt * BULLET_SPACE_AFTER))
    return h - int(Pt(pt * BULLET_SPACE_AFTER))  # no spacing after the last item


# ---------------------------------------------------------------------------
# Standalone "**Label:** value" callout lines (Example/Examples/Use cases/
# Structure/Misconception/... -- any short lead-in line that parse_blocks
# isolated into its own single-paragraph block) get a light CARD_BG card
# instead of floating as a lone plain-text line. A short comma/·-separated
# value renders as its own row of chips.
# ---------------------------------------------------------------------------
_CALLOUT_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 /\-]{1,40}):\*\*\s*(.*)$", re.S)


def detect_callout_block(block: dict) -> tuple[str, str] | None:
    if block.get("type") != "bullets" or len(block.get("items", [])) != 1:
        return None
    _level, kind, _marker, text = block["items"][0]
    if kind != "para":
        return None
    m = _CALLOUT_RE.match(text.strip())
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


def _extract_chip_items(value: str) -> list[str] | None:
    plain = strip_markdown_title(value).rstrip(" .").strip()
    if "·" in plain:
        parts = [p.strip() for p in plain.split("·") if p.strip()]
    elif "," in plain:
        parts = [p.strip() for p in plain.split(",") if p.strip()]
    else:
        return None
    if not (2 <= len(parts) <= 8):
        return None
    if any(len(p) > 30 or p.count(" ") > 4 for p in parts):
        return None
    return parts


def block_height(b: dict, width, pt) -> int:
    """Estimated drawn height of one block at body size pt (no GAP)."""
    if b["type"] == "image":
        return b.get("h", b["min_h"])
    callout = detect_callout_block(b)
    if callout:
        label, value = callout
        chips = _extract_chip_items(value)
        if chips:
            return K.estimate_callout_chip_height(width, label, chips)
        return K.estimate_callout_text_height(width, label, len(strip_markdown_title(value)), pt)
    if b["type"] == "bullets":
        return estimate_bullets_height(b["items"], width, pt)
    if b["type"] == "table":
        return K.estimate_table_height(b["headers"], b["rows"], width, scale=_table_scale(pt))
    if b["type"] == "code":
        return K.estimate_code_height(b["text"], width, _code_pt(pt))
    return 0


def stack_height(blocks, width, pt) -> int:
    if not blocks:
        return 0
    return sum(block_height(b, width, pt) + GAP for b in blocks) - GAP


def _aspect(path: Path) -> float:
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size[0] / max(1, im.size[1])
    except Exception:
        return 1.0


def image_block(path: Path, width, max_h: int) -> dict:
    """A diagram in the flow: wants its natural height at full width (capped
    at a full slide), may shrink to IMAGE_MIN_H to share a slide with text."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            iw, ih = im.size
        natural = int(int(width) * ih / max(1, iw))
    except Exception:
        natural = max_h
    desired = min(max_h, natural)
    return {"type": "image", "path": path, "desired": desired,
            "min_h": min(desired, max(IMAGE_MIN_H, int(desired * 0.45)))}


# ---------------------------------------------------------------------------
# Pagination -- pack blocks, in source order, into pages of a given height.
# A block that doesn't fit in what's left of a page is split at a natural
# boundary: bullets between items, tables between rows (header repeated),
# code between lines (preferring a blank line). Callout cards never split.
# ---------------------------------------------------------------------------
def _largest_prefix(n: int, fits) -> int:
    k = 0
    while k < n and fits(k + 1):
        k += 1
    return k


def split_block(b: dict, width, room: int, page_empty: bool, pt, *, min_side: int = 2):
    """(head, tail): head fits in `room`, tail continues on the next page.

    head is None when nothing useful fits (move the whole block on); tail is
    None when the whole block fits. On an empty page at least one item / row /
    line is always taken so pagination can't stall.
    """
    if detect_callout_block(b) or b["type"] not in ("bullets", "table", "code"):
        return (b, None) if page_empty else (None, b)

    if b["type"] == "bullets":
        items = b["items"]
        n = len(items)
        k = _largest_prefix(n, lambda k: estimate_bullets_height(items[:k], width, pt) <= room)
        # Don't strand a lead-in line ("**Step 2**", "Examples:") or a parent
        # bullet at the bottom of a page, away from what it introduces.
        while 1 < k < n and (items[k - 1][1] == "para" or items[k][0] > items[k - 1][0]):
            k -= 1
        if k >= n:
            return b, None
        # A split list keeps at least min_side items on each side.
        if n - k < min_side:
            k = n - min_side
        if k < min_side and not page_empty:
            return None, b
        k = max(1, k)
        return {"type": "bullets", "items": items[:k]}, {"type": "bullets", "items": items[k:]}

    if b["type"] == "table":
        headers, rows = b["headers"], b["rows"]
        n = len(rows)
        k = _largest_prefix(
            n, lambda k: K.estimate_table_height(headers, rows[:k], width, scale=_table_scale(pt)) <= room)
        if k == 0:
            if not page_empty:
                return None, b
            k = 1
        if k >= n:
            return b, None
        return ({"type": "table", "headers": headers, "rows": rows[:k]},
                {"type": "table", "headers": headers, "rows": rows[k:]})

    # code
    lines = b["text"].split("\n")
    n = len(lines)
    k = _largest_prefix(
        n, lambda k: K.estimate_code_height("\n".join(lines[:k]), width, _code_pt(pt)) <= room)
    if k < n:
        # Prefer to break at a blank line a few lines back, and never leave a
        # single orphan line for the next slide.
        for j in range(k - 1, max(1, k - 5), -1):
            if not lines[j].strip():
                k = j
                break
        if n - k == 1 and k > 2:
            k -= 1
    if k < 3 and not page_empty:
        return None, b
    k = max(1, k)
    if k >= n:
        return b, None
    head = "\n".join(lines[:k]).rstrip("\n")
    tail = "\n".join(lines[k:]).lstrip("\n")
    return {**b, "text": head}, {**b, "text": tail}


KEEP_WHOLE_BULLETS = 4  # lists this short move to the next slide rather than split


def _is_lead_in(b: dict, nxt: dict | None = None) -> bool:
    """A lone paragraph that introduces the block after it: one ending in ":",
    or a short caption line directly above a code sample."""
    if b["type"] != "bullets" or len(b["items"]) != 1 or b["items"][0][1] != "para":
        return False
    text = strip_markdown_title(b["items"][0][3]).rstrip()
    if text.endswith(":"):
        return True
    return nxt is not None and nxt["type"] == "code" and len(text) <= 80


def _first_unit_height(b: dict, width, pt) -> int:
    """Smallest piece of b that could open a page (for keep-with-next)."""
    if b["type"] == "image":
        return b["min_h"]
    if detect_callout_block(b):
        return block_height(b, width, pt)
    if b["type"] == "bullets":
        return estimate_bullets_height(b["items"][:1], width, pt)
    if b["type"] == "table":
        return K.estimate_table_height(b["headers"], b["rows"][:1], width, scale=_table_scale(pt))
    if b["type"] == "code":
        return K.estimate_code_height("\n".join(b["text"].split("\n")[:3]), width, _code_pt(pt))
    return 0


def _keep_whole(b: dict) -> bool:
    if b["type"] in ("code", "table"):
        return True
    return b["type"] == "bullets" and len(b["items"]) <= KEEP_WHOLE_BULLETS


def _keep_with_height(nxt: dict, width, cap_rest: int, pt) -> int:
    """How much of the next block must share a slide with a lead-in: all of
    it when it will move as one piece anyway, otherwise its first unit."""
    full = block_height(nxt, width, pt) + GAP
    if _keep_whole(nxt) and full <= cap_rest * FIT_MARGIN:
        return full
    return _first_unit_height(nxt, width, pt)


def _paginate_once(blocks, width, cap_first: int, cap_rest: int, pt,
                   keep_whole: bool = True) -> list[list[dict]]:
    pages: list[list[dict]] = [[]]
    used, cap = 0, cap_first
    queue = [({k: v for k, v in b.items() if k != "h"} if b["type"] == "image" else b) for b in blocks]

    def new_page():
        nonlocal used, cap
        pages.append([])
        used, cap = 0, cap_rest

    while queue:
        b = queue.pop(0)
        limit = int(cap * FIT_MARGIN)
        room = limit - used - (GAP if pages[-1] else 0)

        if b["type"] == "image":
            # A diagram takes what's left of the slide if that's enough for
            # it, otherwise it starts the next slide.
            if room >= b["min_h"] or not pages[-1]:
                h = max(min(b["desired"], room), min(b["min_h"], room))
                pages[-1].append({**b, "h": h})
                used += h + (GAP if len(pages[-1]) > 1 else 0)
            else:
                queue.insert(0, b)
                new_page()
            continue

        h = block_height(b, width, pt)
        # Keep a lead-in line on the same slide as the start of what it introduces.
        if pages[-1] and queue and _is_lead_in(b, queue[0]) and \
                h + GAP + _keep_with_height(queue[0], width, cap_rest, pt) > room:
            queue.insert(0, b)
            new_page()
            continue
        if h <= room:
            pages[-1].append(b)
            used += h + (GAP if len(pages[-1]) > 1 else 0)
            continue
        # A code block, table, or short list that fits on a slide of its own
        # moves over whole instead of being cut in two.
        if keep_whole and pages[-1] and _keep_whole(b) and h <= cap_rest * FIT_MARGIN:
            queue.insert(0, b)
            new_page()
            continue
        head, tail = split_block(b, width, room, not pages[-1], pt)
        if head is not None:
            pages[-1].append(head)
            used += block_height(head, width, pt) + (GAP if len(pages[-1]) > 1 else 0)
        if tail is None:
            continue
        queue.insert(0, tail)
        new_page()
    if len(pages) > 1 and not pages[-1]:
        pages.pop()
    return pages


def paginate(blocks, width, cap_first: int, cap_rest: int, pt) -> list[list[dict]]:
    """Pack blocks onto as few slides as possible, then even them out: once
    N slides are needed, retry with a lower per-slide target so the content
    spreads across those N slides instead of leaving a near-empty last one."""
    pages = _paginate_once(blocks, width, cap_first, cap_rest, pt)
    if len(pages) > 1:
        # Keeping code/tables/short lists whole is a nicety, not worth a
        # whole extra slide -- drop it when that saves one.
        loose = _paginate_once(blocks, width, cap_first, cap_rest, pt, keep_whole=False)
        if len(loose) < len(pages):
            pages = loose
    n = len(pages)
    if n <= 1 or any(b["type"] == "image" for b in blocks):
        return pages
    total = stack_height(blocks, width, pt)
    for slack in (1.10, 1.20, 1.35):
        target = int(total / n * slack / FIT_MARGIN)
        trial = _paginate_once(blocks, width, min(cap_first, target), min(cap_rest, target), pt)
        if len(trial) == n:
            return trial
    return pages


# ---------------------------------------------------------------------------
# Bullet drawing -- marker/enumerator/lead-in styling ported from
# md287_deck_kit.add_panel_bullets (standard bullet -> INK "•", a bullet's own
# embedded "1." enumerator -> bold RED number, an explicit numbered-list
# marker -> bold RED number, a short "Label: rest" lead-in -> bold INK label).
# ---------------------------------------------------------------------------
def _add_bullet_text(paragraph, text: str, pt: float) -> None:
    label, rest = K.split_lead_in(text)
    if label:
        K.add_run(paragraph, f"{label}: ", size=pt, bold=True, color=K.INK)
        for seg_text, style in parse_inline(rest):
            K.add_rich_run(paragraph, [(seg_text, style)], size=pt, color=K.INK)
    else:
        for seg_text, style in parse_inline(text):
            K.add_rich_run(paragraph, [(seg_text, style)], size=pt, color=K.INK)


def draw_bullets(slide, x, y, width, items, pt) -> int:
    height = estimate_bullets_height(items, width, pt)
    box = K.add_textbox(slide, x, y, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for level, kind, marker, text in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(pt * BULLET_SPACE_AFTER)
        p.line_spacing = LINE_SPACING
        p.space_before = Pt(0)
        indent = "    " * level
        if indent:
            K.add_run(p, indent, size=pt, color=K.INK)

        if kind == "para":
            # A continuation/lead-in line attached to the list (often a bold
            # "**Step N ...**" sub-heading) -- no bullet glyph, per the
            # reference technique which only styles genuine list markers.
            _add_bullet_text(p, text, pt)
            continue

        if kind == "number":
            # Explicit numbered-list marker (e.g. "1)") -- bold red enumerator.
            K.add_run(p, f"{marker} ", size=pt, bold=True, color=K.RED)
            _add_bullet_text(p, text, pt)
            continue

        # kind == "bullet"
        if K.is_standard_or_emoji_marker(marker):
            number, rest = K.split_enumerator(text)
            if number:
                # The bullet text carries its own "1." -- use it instead of a dot.
                K.add_run(p, f"{number} ", size=pt, bold=True, color=K.RED)
                _add_bullet_text(p, rest, pt)
            else:
                glyph = "•" if level == 0 else "–"
                K.add_run(p, f"{glyph}  ", size=pt, color=K.INK)
                _add_bullet_text(p, text, pt)
        else:
            K.add_run(p, f"{marker} ", size=pt, bold=True, color=K.RED)
            _add_bullet_text(p, text, pt)
    return height


def draw_stack(slide, x, y, width, blocks, pt, *, badge_seed: int = 0) -> int:
    """Draw blocks top to bottom in source order. Returns the height used."""
    cursor = y
    callout_i = 0
    for b in blocks:
        callout = detect_callout_block(b)
        if b["type"] == "image":
            h = b["h"]
            K.add_picture_fitted(slide, b["path"], x, cursor, width, h)
        elif callout:
            label, value = callout
            chips = _extract_chip_items(value)
            if chips:
                h = K.add_callout_chip_card(
                    slide, x, cursor, width, label, chips,
                    badge_start=badge_seed + callout_i,
                )
            else:
                h = K.add_callout_text_card(slide, x, cursor, width, label, parse_inline(value), pt=pt)
            callout_i += 1
        elif b["type"] == "bullets":
            h = draw_bullets(slide, x, cursor, width, b["items"], pt)
        elif b["type"] == "table":
            h = K.add_table(slide, x, cursor, width, b["headers"], b["rows"], scale=_table_scale(pt))
        elif b["type"] == "code":
            cpt = _code_pt(pt)
            h = K.estimate_code_height(b["text"], width, cpt)
            K.add_code_block(slide, x, cursor, width, h, b["text"], font_pt=cpt)
        else:
            continue
        cursor += h + GAP
    return cursor - y


# ---------------------------------------------------------------------------
# Top-level: one manifest record (or a merged run of "(cont.)" records) ->
# one or more slides. Content is top-aligned under the title and packed down
# to the copyright line; there are no kicker labels or generic panel headings.
# ---------------------------------------------------------------------------
CONTENT_TOP_MARGIN = int(Inches(0.10))

# Diagram beside text (only when that text fits there at 20pt or larger).
SPLIT_TEXT_W = int(Inches(4.80))
SPLIT_GAP = int(Inches(0.20))
SPLIT_IMAGE_X = int(K.CONTENT_X) + SPLIT_TEXT_W + SPLIT_GAP
SPLIT_IMAGE_W = int(K.CONTENT_W) - SPLIT_TEXT_W - SPLIT_GAP

TAKEAWAY_GAP = int(Inches(0.12))


def _content_top(title: str) -> int:
    return max(K.content_top_for(None, title), CONTENT_TOP_MARGIN + int(Inches(0.55)))


def _start_slide(prs, layout, title):
    slide = K.new_slide(prs, layout)
    top = K.add_title_block(slide, title=title)
    return slide, max(top, CONTENT_TOP_MARGIN + int(Inches(0.55)))


def _record_parts(record: dict, repo_root: Path):
    """(blocks-with-diagrams-in-flow, diagram paths, notes) for a record or a
    merged run of continuation records."""
    blocks: list[dict] = []
    diagrams: list[Path] = []
    notes: list[str] = []
    for part in record.get("_parts") or [record]:
        body_raw = scrub_brand(part.get("body_markdown") or "")
        col_text, was_split = extract_col_text(body_raw)
        diagram_rel = part.get("diagram_png")
        diagram_path = (Path(repo_root) / diagram_rel) if diagram_rel else None
        has_diagram = bool(diagram_path and diagram_path.exists())
        blocks.extend(parse_blocks(col_text if (was_split or has_diagram) else body_raw))
        if has_diagram:
            blocks.append({"type": "diagram", "path": diagram_path})
            diagrams.append(diagram_path)
        n = scrub_brand(part.get("notes"))
        if n and n.strip() and n.strip() not in notes:
            notes.append(n.strip())
    return _dedupe_repeated_blocks(blocks), diagrams, "\n\n".join(notes) or None


def _fill_page(page: list[dict], width, room: int, pt):
    """Use the space pagination left over on one slide: diagrams grow back
    toward full size, and text on a text-only slide takes the largest size
    from PT_LADDER that still fits. Returns (page, pt)."""
    images = [b for b in page if b["type"] == "image"]
    if images:
        text_h = stack_height([b for b in page if b["type"] != "image"], width, pt)
        spare = room - text_h - GAP * (len(page) - 1) - sum(b["h"] for b in images)
        out = []
        for b in page:
            if b["type"] == "image" and spare > 0:
                grow = min(spare, b["desired"] - b["h"])
                if grow > 0:
                    b = {**b, "h": b["h"] + grow}
                    spare -= grow
            out.append(b)
        return out, pt
    for p in PT_LADDER:
        if p < pt:
            break
        if stack_height(page, width, p) <= room:
            return page, p
    return page, pt


def render_record(prs, layout, record: dict, page_num: int | None, kicker: str | None,
                   repo_root: Path, chips: list[str] | None = None):
    """Render one manifest record (or a merge_continuations group). Returns
    (slides, kind) where slides is the list of slides drawn (empty when
    skipped; continuation slides follow the first, numbered page_num,
    page_num + 1, ...) and kind is one of 'skipped', 'title', 'diagram',
    'table', 'code', 'plain'.

    ``kicker`` is accepted for the builder's call signature but no longer
    drawn -- slides carry no "Day N · Module N" / "Course Introduction" label.
    ``chips`` (only used for a ``lead`` record) is the cover slide's row of
    4-5 short topic labels -- see K.add_topic_chip_row."""
    heading_raw = scrub_brand((record.get("heading") or "").strip())
    marp_class = (record.get("marp_class") or "").strip()
    parts = record.get("_parts") or [record]

    if not heading_raw and not any((p.get("body_markdown") or "").strip() for p in parts):
        return [], "skipped"

    title = strip_markdown_title(heading_raw) or "Untitled"

    if marp_class == "lead":
        subtitle = flatten_markdown(scrub_brand(record.get("body_markdown") or ""))
        slide = K.chapter_slide(prs, layout, title=title, subtitle=subtitle, chips=chips,
                                notes=scrub_brand(record.get("notes")))
        return [slide], "title"

    flow, diagrams, notes = _record_parts(record, repo_root)
    flow, keymsg_text = pop_keymsg(flow)
    text_blocks = [b for b in flow if b["type"] != "diagram"]

    reserve = (K.takeaway_height(keymsg_text) + TAKEAWAY_GAP) if keymsg_text else 0
    bottom = int(K.CONTENT_BOTTOM)
    first_top = _content_top(title)
    # Source headings sometimes already say "(cont.)" -- don't double it.
    cont_title = title if title.lower().rstrip().endswith(CONT_SUFFIX.strip()) else title + CONT_SUFFIX
    cont_top = _content_top(cont_title)
    width = int(K.CONTENT_W)

    slides = []
    badge_seed = page_num or 0

    def finish(slide, *, takeaway: bool):
        if takeaway and keymsg_text:
            K.add_key_takeaway(slide, keymsg_text)
        K.add_rail_and_footer(slide, None if page_num is None else page_num + len(slides))
        K.set_notes(slide, notes if not slides else f"(Continued: {title}.)")
        slides.append(slide)

    # 1) One diagram beside its text -- when that text is plain bullets /
    #    callouts and fits there on one slide at 20pt or more.
    if len(diagrams) == 1 and text_blocks and all(b["type"] == "bullets" for b in text_blocks) \
            and _aspect(diagrams[0]) <= 2.0:  # a wide, short diagram reads better below its text
        room = int((bottom - reserve - first_top) * FIT_MARGIN)
        pt = next((p for p in PT_LADDER if stack_height(text_blocks, SPLIT_TEXT_W, p) <= room), None)
        if pt is not None:
            slide, top = _start_slide(prs, layout, title)
            draw_stack(slide, K.CONTENT_X, top, SPLIT_TEXT_W, text_blocks, pt, badge_seed=badge_seed)
            K.add_picture_fitted(slide, diagrams[0], SPLIT_IMAGE_X, top, SPLIT_IMAGE_W,
                                 bottom - reserve - top)
            finish(slide, takeaway=True)
            return slides, "diagram"

    # 2) Everything in one top-aligned flow at full width, diagrams in place,
    #    split across slides as needed at the largest size that doesn't add
    #    slides.
    cap_first = bottom - first_top
    cap_rest = bottom - cont_top
    blocks = [image_block(b["path"], width, cap_rest) if b["type"] == "diagram" else b for b in flow]

    def layout_at(pt):
        pages = paginate(blocks, width, cap_first, cap_rest, pt)
        if keymsg_text:
            li = len(pages) - 1
            cap_li = cap_first if li == 0 else cap_rest
            if stack_height(pages[li], width, pt) > (cap_li - reserve) * FIT_MARGIN:
                redo = paginate(pages[li], width, cap_li - reserve, cap_rest - reserve, pt)
                pages = pages[:li] + redo
        return pages

    min_pages = len(layout_at(K.MIN_PT))
    pt, pages = K.MIN_PT, None
    for p in PT_LADDER:
        trial = layout_at(p)
        if len(trial) <= min_pages:
            pt, pages = p, trial
            break

    for i, page in enumerate(pages):
        is_last = i == len(pages) - 1
        room = int(((cap_first if i == 0 else cap_rest) - (reserve if is_last else 0)) * FIT_MARGIN)
        page, page_pt = _fill_page(page, width, room, pt)
        slide, top = _start_slide(prs, layout, title if i == 0 else cont_title)
        draw_stack(slide, K.CONTENT_X, top, width, page, page_pt, badge_seed=badge_seed + i)
        finish(slide, takeaway=is_last)

    if diagrams:
        return slides, "diagram"
    kinds = {b["type"] for b in text_blocks}
    kind = "table" if "table" in kinds else "code" if "code" in kinds else "plain"
    return slides, kind


# ---------------------------------------------------------------------------
# Packed flow -- a run of topics (everything between two cover slides)
# rendered as one continuous flow at a fixed 18pt body size (tables and
# code blocks 14pt):
#
# - a topic that starts at the top of a slide gives the slide its title; one
#   that starts mid-slide gets a bold red subheading instead, so topics share
#   slides rather than each leaving the bottom of its own slide empty;
# - a slide that opens mid-topic is titled "<topic> (cont.)";
# - a diagram floats at the right of its own topic's text, which wraps in
#   the column beside it;
# - lists of short items run in two columns;
# - a topic's key takeaway is a full-width card at the end of the topic.
#
# Nothing is dropped: every block of every source record is drawn (only
# exact duplicate blocks within a topic are collapsed, as before), and each
# slide's speaker notes hold the notes of every topic that starts on it.
# ---------------------------------------------------------------------------
FLOW_PT = K.MIN_PT
FLOW_FIT = 1.0
FLOAT_W = int(Inches(5.80))
FLOAT_GAP = int(Inches(0.20))
NARROW_W = int(K.CONTENT_W) - FLOAT_W - FLOAT_GAP
TWO_COL_GAP = int(Inches(0.30))
TWO_COL_MAX_CHARS = 50
SUBHEAD_GAP_BEFORE = int(Inches(0.06))
SUBHEAD_H = int(Inches(FLOW_PT / 72 * 1.25)) + int(Inches(0.04))
KEEP_WHOLE_ROOM = 0.15  # keep a code block / table whole only when less than this much of a slide is left


def _flow_items(group: dict, repo_root: Path) -> list[dict]:
    """topic marker, then per source part: its diagram (as a float) and its
    blocks; the topic's takeaway last."""
    title = strip_markdown_title(scrub_brand((group.get("heading") or "").strip())) or "Untitled"
    items: list[dict] = []
    body: list[dict] = []
    notes: list[str] = []
    for part in group.get("_parts") or [group]:
        body_raw = scrub_brand(part.get("body_markdown") or "")
        col_text, was_split = extract_col_text(body_raw)
        diagram_rel = part.get("diagram_png")
        diagram_path = (Path(repo_root) / diagram_rel) if diagram_rel else None
        has_diagram = bool(diagram_path and diagram_path.exists())
        if has_diagram:
            body.append({"type": "float", "path": diagram_path})
        body.extend(parse_blocks(col_text if (was_split or has_diagram) else body_raw))
        n = scrub_brand(part.get("notes"))
        if n and n.strip() and n.strip() not in notes:
            notes.append(n.strip())
    body = _dedupe_repeated_blocks(body)
    body = _rejoin_code_chunks(body)
    body, keymsg = pop_keymsg(body)
    items.append({"type": "topic", "title": title, "notes": "\n\n".join(notes) or None})
    items.extend(body)
    if keymsg:
        items.append({"type": "takeaway", "text": keymsg})
    return items


CODE_CHUNK_MIN_LINES = 25  # merge_rich_content cuts code samples over 32 lines into consecutive chunks


def _rejoin_code_chunks(blocks: list[dict]) -> list[dict]:
    """Put a long code sample that the source build cut into consecutive
    chunks back together, so it can be laid out (in two columns if need be)
    on one slide."""
    out: list[dict] = []
    for b in blocks:
        prev = out[-1] if out else None
        if (b["type"] == "code" and prev is not None and prev["type"] == "code"
                and prev["text"].count("\n") + 1 >= CODE_CHUNK_MIN_LINES):
            joined = {**prev, "text": prev["text"].rstrip("\n") + "\n" + b["text"]}
            if _fits_one_slide(joined):
                out[-1] = joined
                continue
        out.append(b)
    return out


def _fits_one_slide(b: dict) -> bool:
    """Would this code block fit on one (cont.) slide, in one column or two?"""
    W = int(K.CONTENT_W)
    cap = int(K.CONTENT_BOTTOM) - _content_top("X" + CONT_SUFFIX)
    if _flow_height(b, W) <= cap:
        return True
    halves = _code_halves(b)
    half_w = (W - TWO_COL_GAP) // 2
    return bool(halves) and all(_code_fits_width(h, half_w) for h in halves) \
        and max(_flow_height(h, half_w) for h in halves) <= cap


def _two_col_ok(b: dict) -> bool:
    if b["type"] != "bullets" or detect_callout_block(b):
        return False
    items = b["items"]
    return len(items) >= 4 and all(
        lvl == 0 and kind in ("bullet", "number") and len(strip_markdown_title(t)) <= TWO_COL_MAX_CHARS
        for lvl, kind, _m, t in items)


def _two_col_split(items):
    half = -(-len(items) // 2)
    return items[:half], items[half:]


def _code_fits_width(b: dict, width) -> bool:
    # Consolas advance width is 0.55em (0.00764 in/pt); a little slack on top.
    cpl = int((int(width) - int(Inches(0.28))) / 914400 / (0.0078 * CODE_PT))
    return all(len(line) <= cpl for line in b["text"].split("\n"))


def _narrow_ok(b: dict) -> bool:
    """Can this block sit in the text column beside a floating diagram?"""
    if b["type"] in ("table", "takeaway", "float"):
        return False
    if b["type"] == "code":
        # Long samples go below the diagram, at full width, where they can
        # run in two columns rather than being split across slides.
        return _code_fits_width(b, NARROW_W) and b["text"].count("\n") + 1 <= NARROW_CODE_MAX_LINES
    return True


NARROW_CODE_MAX_LINES = 12


def _flow_height(b: dict, width, *, two_col: bool = False) -> int:
    if b["type"] == "topic":
        # A long subheading in the narrow column beside a diagram wraps.
        lines = _wrapped_lines(f"**{b['title']}**", _chars_per_line(width, FLOW_PT))
        return SUBHEAD_H + (lines - 1) * int(Inches(FLOW_PT / 72 * 1.25))
    if b["type"] == "takeaway":
        return K.takeaway_height(b["text"])
    if two_col:
        left, right = _two_col_split(b["items"])
        col_w = (int(width) - TWO_COL_GAP) // 2
        return max(estimate_bullets_height(left, col_w, FLOW_PT),
                   estimate_bullets_height(right, col_w, FLOW_PT))
    return block_height(b, width, FLOW_PT)


def _float_size(path: Path) -> tuple[int, int]:
    return FLOAT_W, int(FLOAT_W / max(0.2, _aspect(path)))


FLOAT_MIN_W = int(Inches(4.20))


def _float_fit(path: Path, room: int):
    """Largest float (FLOAT_W down to FLOAT_MIN_W wide) whose height fits in
    room; (None, None) when even the smallest doesn't."""
    aspect = max(0.2, _aspect(path))
    fw = min(FLOAT_W, int(room * aspect))
    if fw < FLOAT_MIN_W:
        return None, None
    return fw, int(fw / aspect)


def _split_sentences(b: dict, width, room: int):
    """Split a list whose *first* item alone is too tall, between sentences
    of that item; the rest of the item continues (unmarked) on the next slide."""
    if b["type"] != "bullets" or detect_callout_block(b):
        return None, b
    lvl, kind, marker, text = b["items"][0]
    sents = re.split(r"(?<=[.!?:;])\s+(?=[A-Z`*(\[])", text)
    if len(sents) < 2:
        return None, b
    k = _largest_prefix(len(sents) - 1, lambda k: estimate_bullets_height(
        [(lvl, kind, marker, " ".join(sents[:k]))], width, FLOW_PT) <= room)
    if k == 0:
        return None, b
    head = {"type": "bullets", "items": [(lvl, kind, marker, " ".join(sents[:k]))]}
    tail = {"type": "bullets", "items": [(lvl, "para", "", " ".join(sents[k:]))] + b["items"][1:]}
    return head, tail


def _flow_first_unit(b: dict, width) -> int:
    if b["type"] == "float":
        return int(FLOAT_MIN_W / max(0.2, _aspect(b["path"])))
    if b["type"] in ("topic", "takeaway"):
        return _flow_height(b, width)
    return _first_unit_height(b, width, FLOW_PT)


def _code_card_w(b: dict, col_w) -> int:
    """Code card width: its longest line (at the same per-character width
    K.estimate_code_height wraps at, so nothing wraps) plus padding, never
    wider than the column."""
    longest = max((len(line) for line in b["text"].split("\n")), default=1)
    need = int(Inches(longest * 0.0083 * CODE_PT + 0.28 + 0.12))
    return max(int(Inches(1.6)), min(int(col_w), need))


COMPACT_MIN_LINES = 8


def _compactable(b: dict) -> bool:
    """A code sample long enough, with short enough lines, to run in two columns."""
    if b["type"] != "code" or b["text"].count("\n") + 1 < COMPACT_MIN_LINES:
        return False
    halves = _code_halves(b)
    if not halves:
        return False
    half_w = (int(K.CONTENT_W) - TWO_COL_GAP) // 2
    cpl = int((half_w - int(Inches(0.28))) / 914400 / (0.0078 * CODE_PT))
    lens = [len(line) for h in halves for line in h["text"].split("\n")]
    # A line or two may wrap, as long as none runs far past the column.
    return sum(n > cpl for n in lens) <= 2 and max(lens) <= cpl * 1.3


def _lead_in_fits_with(lead: dict, nxt: dict, cap: int) -> bool:
    """Would a lead-in line and the block it introduces share one slide?"""
    W = int(K.CONTENT_W)
    if nxt["type"] in ("topic", "float", "takeaway"):
        return False
    h = _flow_height(nxt, W, two_col=_two_col_ok(nxt))
    if nxt["type"] == "code" and h > cap - SUBHEAD_H and _compactable(nxt):
        half_w = (W - TWO_COL_GAP) // 2
        h = max(_flow_height(hb, half_w) for hb in _code_halves(nxt))
    if h > cap:  # a block taller than a slide is split anyway; its start will do
        h = _flow_first_unit(nxt, W)
    return _flow_height(lead, W) + GAP + h <= cap


def _topic_fits_one_slide(topic: dict, queue: list[dict]) -> bool:
    """Would this topic (its items up to the next topic marker) fit on one
    slide of its own?"""
    items = [topic]
    for it in queue:
        if it["type"] == "topic":
            break
        items.append(it)
    return len(paginate_flow(items)) <= 1


def _code_halves(b: dict):
    """Split a code block's lines in two, at a blank line near the middle
    when there is one."""
    lines = b["text"].split("\n")
    if len(lines) < 6:
        return None
    mid = len(lines) // 2
    for off in range(0, 6):
        for j in (mid - off, mid + off):
            if 2 <= j < len(lines) - 2 and not lines[j].strip():
                return ({**b, "text": "\n".join(lines[:j]).rstrip("\n")},
                        {**b, "text": "\n".join(lines[j + 1:]).lstrip("\n")})
    return ({**b, "text": "\n".join(lines[:mid])}, {**b, "text": "\n".join(lines[mid:])})


def paginate_flow(items: list[dict]) -> list[dict]:
    """Lay the flow out onto slides. Returns one dict per slide:
    {"title", "notes": [..], "placed": [(item, x, y, w, h, mode)], "topic"}
    with y relative to the slide's content top."""
    W = int(K.CONTENT_W)
    X = int(K.CONTENT_X)
    pages: list[dict] = []
    queue = list(items)
    current_topic = ""

    page = None
    y = 0
    cap = 0
    float_bottom = None
    # A diagram that didn't fit where it came in the flow waits here and
    # opens the next slide, still beside its own topic's text.
    pending = None

    def open_page():
        nonlocal page, y, cap, float_bottom, pending
        # A topic at the very top of a slide becomes its title.
        if pending is not None:
            title = pending[1] if pending[1].lower().endswith(CONT_SUFFIX.strip())                 else pending[1] + CONT_SUFFIX
            notes, topic = [], pending[1]
        elif queue and queue[0]["type"] == "topic":
            t = queue.pop(0)
            title, notes = t["title"], [t["notes"]] if t["notes"] else []
            topic = t["title"]
        else:
            title = current_topic if current_topic.lower().endswith(CONT_SUFFIX.strip()) \
                else current_topic + CONT_SUFFIX
            notes, topic = [], current_topic
        page = {"title": title, "notes": notes, "placed": [], "topic": topic}
        pages.append(page)
        y = 0
        cap = int((int(K.CONTENT_BOTTOM) - _content_top(title)) * FLOW_FIT)
        float_bottom = None
        if pending is not None:
            fb = pending[0]
            fw, fh = _float_fit(fb["path"], cap)
            if fw is None:
                fw, fh = _float_size(fb["path"])
                fh = min(fh, cap)
            page["placed"].append((fb, X + W - fw, 0, fw, fh, "float"))
            float_bottom = fh
            pending = None
        return topic

    current_topic = open_page()

    # Keep-together: a topic that starts mid-slide is laid out on trial. If
    # any of it would spill onto another slide, everything is rolled back
    # and the topic starts at the top of a fresh slide instead (where it
    # gets the slide title). Only a topic longer than a whole slide ever
    # continues on "(cont.)" slides.
    trial = None

    def checkpoint():
        return {"pages": len(pages), "page": {**page, "notes": list(page["notes"]),
                                                "placed": list(page["placed"])},
                "y": y, "cap": cap, "float_bottom": float_bottom, "pending": pending,
                "current_topic": current_topic, "queue": list(queue)}

    def rollback():
        nonlocal page, y, cap, float_bottom, pending, current_topic, trial
        t = trial
        trial = None
        del pages[t["pages"]:]
        page = t["page"]
        pages[-1] = page
        y, cap, float_bottom = t["y"], t["cap"], t["float_bottom"]
        pending, current_topic = t["pending"], t["current_topic"]
        queue[:] = t["queue"]
        end = next((k for k in range(1, len(queue)) if queue[k]["type"] == "topic"), len(queue))
        if not queue[0].get("_compact") and any(_compactable(it) for it in queue[1:end]):
            # Second try, right here: its long code samples in two columns.
            queue[0] = {**queue[0], "_compact": True}
            for k in range(1, end):
                if _compactable(queue[k]):
                    queue[k] = {**queue[k], "compact": True}
            return
        # Start the topic on a new slide instead (code back to one column).
        queue[0] = {**queue[0], "_fresh": True}
        for k in range(1, end):
            queue[k] = {kk: v for kk, v in queue[k].items() if kk != "compact"}
        current_topic = open_page()

    def new_page():
        nonlocal current_topic, pending
        if trial is not None:
            rollback()
            return
        # Never end a slide on a lead-in line ("Example validator:") --
        # it goes over with the block it introduces.
        # (Only when the two fit on a slide together; a block that needs a
        # whole slide of its own leaves the lead-in where it is.)
        while len(page["placed"]) > 1 and page["placed"][-1][5] == "block" \
                and _is_lead_in(page["placed"][-1][0]) and queue \
                and _lead_in_fits_with(page["placed"][-1][0], queue[0], cap):
            queue.insert(0, page["placed"].pop()[0])
        # Never leave a subheading stranded at the bottom of a slide:
        # move it (and its waiting diagram) to open the next one.
        if page["placed"] and page["placed"][-1][5] == "topic":
            t = page["placed"].pop()[0]
            if t["notes"] and t["notes"] in page["notes"]:
                page["notes"].remove(t["notes"])
            if pending is not None and pending[1] == t["title"]:
                queue.insert(0, pending[0])
                pending = None
            queue.insert(0, t)
        current_topic = open_page()

    while True:
        while queue:
            b = queue.pop(0)
            if float_bottom is not None and y >= float_bottom:
                float_bottom = None
            beside = float_bottom is not None
            col_w = NARROW_W if beside else W
            empty = not page["placed"]

            if beside and not _narrow_ok(b) and b["type"] != "float":
                y = float_bottom
                float_bottom, beside, col_w = None, False, W
            gap = 0 if empty else GAP
            room = cap - y - gap

            if b["type"] == "topic":
                if trial is not None:
                    if pending is not None:  # its diagram didn't make it onto the slide
                        queue.insert(0, b)
                        new_page()
                        continue
                    trial = None  # the previous topic fitted where it started
                if pending is not None:  # the previous topic's diagram goes first
                    queue.insert(0, b)
                    new_page()
                    continue
                if not empty and b.get("_fresh"):
                    queue.insert(0, b)
                    new_page()
                    continue
                extra = 0 if empty else SUBHEAD_GAP_BEFORE
                sh = _flow_height(b, col_w)
                nxt = queue[0] if queue else None
                need = extra + sh + (GAP + _flow_first_unit(nxt, col_w) if nxt else 0)
                if need > room:
                    queue.insert(0, b)
                    new_page()
                    continue
                # A topic longer than a slide continues onto a (cont.) slide
                # wherever it starts, so it may start here, mid-slide, under
                # its subheading; only a topic that fits one slide is tried
                # (and, if it spills, moved to a fresh slide) as a whole.
                if not empty and _topic_fits_one_slide(b, queue):
                    queue.insert(0, b)
                    trial = checkpoint()
                    queue.pop(0)
                page["placed"].append((b, X, y + gap + extra, col_w, sh, "topic"))
                y += gap + extra + sh
                if b["notes"]:
                    page["notes"].append(b["notes"])
                current_topic = b["title"]
                page["topic"] = page["topic"] or b["title"]
                continue

            if b["type"] == "float":
                # A second diagram stacks under the one already floating; the
                # text column beside them carries on where it is.
                fy = max(y + gap, float_bottom + GAP) if float_bottom is not None else y + gap
                fw, fh = _float_fit(b["path"], cap - fy)
                if fw is None:
                    if not empty and pending is None and trial is None:
                        pending = (b, current_topic)
                        continue
                    if not empty:
                        queue.insert(0, b)
                        new_page()
                        continue
                    fw, fh = _float_size(b["path"])
                    fh = min(fh, cap)
                    fy = y + gap
                page["placed"].append((b, X + W - fw, fy, fw, fh, "float"))
                float_bottom = fy + fh
                if fy == y + gap:
                    y += gap
                continue

            if b["type"] == "takeaway":
                h = _flow_height(b, W)
                if h > room and not empty:
                    queue.insert(0, b)
                    new_page()
                    continue
                page["placed"].append((b, X, y + gap, W, h, "takeaway"))
                y += gap + h
                continue

            # Keep a lead-in line with the start of what it introduces.
            # (A diagram in between can wait for the next slide, so look past it.)
            nxt_real = next((it for it in queue if it["type"] != "float"), None)
            if not empty and nxt_real is not None and _is_lead_in(b, nxt_real):
                h = _flow_height(b, col_w)
                nxt = nxt_real
                nxt_w = col_w if (not beside or _narrow_ok(nxt)) else W
                # The block it introduces moves over whole when it fits on a
                # slide, so the lead-in needs room for all of it, not a start.
                nxt_full = _flow_height(nxt, nxt_w, two_col=not beside and _two_col_ok(nxt)) \
                    if nxt["type"] not in ("topic", "float", "takeaway") else None
                if nxt["type"] == "code" and nxt_full is not None and not beside and (
                        nxt.get("compact") or (nxt_full > cap and _fits_one_slide(nxt))
                        or (nxt_full > room - h - GAP and _compactable(nxt))):
                    # it will run in two columns
                    half_w = (W - TWO_COL_GAP) // 2
                    nxt_full = max(_flow_height(hb, half_w) for hb in _code_halves(nxt))
                need_next = nxt_full if nxt_full is not None and nxt_full <= cap \
                    else _flow_first_unit(nxt, nxt_w)
                if h + GAP + need_next > room:
                    queue.insert(0, b)
                    new_page()
                    continue

            # On a topic's second try, its long code runs in two columns.
            # Also whenever that is what lets a long sample fit where it is.
            if b["type"] == "code" and not beside and (b.get("compact") or (
                    _flow_height(b, W) > room and _compactable(b))):
                halves = _code_halves(b)
                half_w = (W - TWO_COL_GAP) // 2
                h2 = max(_flow_height(hb, half_w) for hb in halves)
                if h2 <= room:
                    page["placed"].append(({**b, "halves": halves}, X, y + gap, W, h2, "code2"))
                    y += gap + h2
                    continue

            # A code block taller than a slide, with short lines, runs in two
            # side-by-side columns so it still stays on one slide.
            if b["type"] == "code" and not beside and _flow_height(b, W) > cap:
                halves = _code_halves(b)
                half_w = (W - TWO_COL_GAP) // 2
                if halves and all(_code_fits_width(hb, half_w) for hb in halves):
                    h2 = max(_flow_height(hb, half_w) for hb in halves)
                    if h2 <= cap:
                        if h2 > room and not empty:
                            queue.insert(0, b)
                            new_page()
                            continue
                        page["placed"].append(({**b, "halves": halves}, X, y + gap, W, h2, "code2"))
                        y += gap + h2
                        continue

            two_col = not beside and _two_col_ok(b)
            h = _flow_height(b, col_w, two_col=two_col)
            if h <= room:
                page["placed"].append((b, X, y + gap, col_w, h, "two_col" if two_col else "block"))
                y += gap + h
                continue
            # Inside a long topic, a block that fits on a slide of its own
            # (code, table, list, paragraph) moves over whole rather than
            # being cut in two; only a block taller than a slide is split.
            if not empty and _flow_height(b, W, two_col=_two_col_ok(b)) <= cap:
                queue.insert(0, b)
                new_page()
                continue
            head, tail = split_block(b, col_w, room, empty, FLOW_PT, min_side=1)
            if head is None and room > int(Inches(0.8)):
                head, tail = _split_sentences(b, col_w, room)
            if head is not None:
                hh = _flow_height(head, col_w)
                page["placed"].append((head, X, y + gap, col_w, hh, "block"))
                y += gap + hh
            if tail is not None:
                queue.insert(0, tail)
                new_page()
        if pending is not None:
            if trial is not None:
                rollback()
                continue
            current_topic = open_page()
        break
    return pages


def _reattach_lead_ins(items: list[dict]) -> list[dict]:
    """The source sometimes ends one slide with "Decrease inventory:" and
    starts the next slide with the code it introduces. Move such a trailing
    lead-in line past the next topic's heading, directly above that code."""
    out = list(items)
    k = 1
    while k < len(out):
        if out[k]["type"] == "topic":
            prev = out[k - 1]
            j = k + 1
            while j < len(out) and out[j]["type"] == "float":
                j += 1
            if (prev["type"] == "bullets" and len(prev["items"]) == 1
                    and prev["items"][0][1] == "para"
                    and strip_markdown_title(prev["items"][0][3]).rstrip().endswith(":")
                    and j < len(out) and out[j]["type"] == "code"):
                out.insert(j, out.pop(k - 1))
                continue
        k += 1
    return out


def render_flow(prs, layout, groups: list[dict], page_num: int, repo_root: Path) -> list:
    """Render a run of non-cover topic groups as packed slides; returns them."""
    items: list[dict] = []
    for g in groups:
        items.extend(_flow_items(g, repo_root))
    items = _reattach_lead_ins(items)
    slides = []
    for i, page in enumerate(paginate_flow(items)):
        slide, top = _start_slide(prs, layout, page["title"])
        for b, x, y, w, h, mode in page["placed"]:
            yy = top + y
            if mode == "topic":
                K.add_text(slide, x, yy, w, h, b["title"], size=FLOW_PT, bold=True, color=K.RED)
            elif mode == "float":
                K.add_picture_fitted(slide, b["path"], x, yy, w, h)
            elif mode == "takeaway":
                K.add_key_takeaway(slide, b["text"], top=yy)
            elif mode == "code2":
                col_w = (w - TWO_COL_GAP) // 2
                cx = x
                for hb in b["halves"]:
                    cw = _code_card_w(hb, col_w)
                    K.add_code_block(slide, cx, yy, cw, h, hb["text"], font_pt=CODE_PT)
                    cx += cw + TWO_COL_GAP
            elif b["type"] == "code":
                # The card is as wide as its longest line, not the whole column.
                K.add_code_block(slide, x, yy, _code_card_w(b, w), h, b["text"], font_pt=CODE_PT)
            elif mode == "two_col":
                left, right = _two_col_split(b["items"])
                col_w = (w - TWO_COL_GAP) // 2
                draw_bullets(slide, x, yy, col_w, left, FLOW_PT)
                draw_bullets(slide, x + col_w + TWO_COL_GAP, yy, col_w, right, FLOW_PT)
            else:
                draw_stack(slide, x, yy, w, [b], FLOW_PT, badge_seed=page_num + i)
        K.add_rail_and_footer(slide, page_num + i)
        K.set_notes(slide, "\n\n".join(page["notes"]) or f"(Continued: {page['topic']}.)")
        slides.append(slide)
    return slides
