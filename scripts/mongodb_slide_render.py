#!/usr/bin/env python3
"""Manifest-record -> pptx-slide renderer for the Mastering MongoDB decks.

Consumes one slide record from scripts/marp_manifests/*.json (schema:
global_index, marp_class, heading, body_markdown, notes, diagram_png) and
draws the corresponding native PowerPoint slide using the chrome/primitives
in mongodb_deck_kit.py, restyled to match the Innovation In Software house
theme (ported from the sibling MD287 project's md287_deck_kit.py):

- ``lead`` records (module/course openers) -> the white-background
  ``K.chapter_slide`` module-divider layout.
- Plain bullet/objectives slides -> auto-shrinking red title block + bullets
  styled with the ported marker/enumerator/lead-in logic + a cream KEY
  TAKEAWAY bar when the source has a "Key message:" callout.
- Split+diagram slides -> title block + left bullet panel + right diagram
  (uniform-scaled, centered, never stretched) + same takeaway/rail/footer.
- Table slides -> title block + navy-header/zebra-row table.
- Code slides -> title block + Consolas CARD_BG/CARD_LINE card box(es).

All slides get the red/black right-edge rail, 14pt gray footer, and rotated
red page number via ``K.add_rail_and_footer``.

Markdown parsing (bullets, tables, code fences, split-div extraction, dedup
of repeated blocks) is unchanged from the original renderer -- only the
drawing calls were restyled.
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
    """Pull the (at most one) keymsg block out; it renders as a slide-level
    KEY TAKEAWAY bar pinned to the bottom, not inline with the other blocks."""
    out = []
    keymsg_text = None
    for b in blocks:
        if b["type"] == "keymsg" and keymsg_text is None:
            keymsg_text = b["text"]
            continue
        out.append(b)
    return out, keymsg_text


# ---------------------------------------------------------------------------
# Sizing heuristics (character-count based -- no font-metrics dependency)
# ---------------------------------------------------------------------------
CHAR_W = 0.0073  # inches per point per character, ~Nirmala UI at BODY_PT_BASE


def _chars_per_line(width, pt) -> int:
    return max(10, int(int(width) / 914400 / (CHAR_W * pt)))


BODY_PT_BASE = 13.0
# Absolute pt sizes this deck's bullet text may render at, largest first. A
# sparse slide (few bullets, lots of room) gets bumped up toward 24pt instead
# of sitting at a fixed 13pt with dead space below; a dense slide still falls
# back down this same ladder for overflow protection, same as before.
BODY_PT_LADDER = (20, 18, 16, 14, 12, 11, 10, 9, 8)
SCALE_STEPS = tuple(pt / BODY_PT_BASE for pt in BODY_PT_LADDER)
BULLET_SPACE_AFTER_PT = 5.0  # was 3.0 -- more breathing room between bullets
FIT_MARGIN = 0.94  # leave a little slack instead of maxing out to the pixel

CODE_PT_STEPS = (17, 15, 13, 12, 11, 10, 9, 8, 7, 6)


def _item_lines(item, width, pt) -> int:
    level, kind, marker, text = item
    indent_w = int(Inches(0.28)) * level
    usable = max(int(Inches(1.0)), int(width) - indent_w - int(Inches(0.32)))
    cpl = _chars_per_line(usable, pt)
    return max(1, -(-(len(text) + 3) // cpl))


def estimate_bullets_height(items, width, scale: float) -> int:
    pt = BODY_PT_BASE * scale
    line_h = int(Inches(pt / 72 * 1.32))
    h = int(Inches(0.05))
    for item in items:
        h += _item_lines(item, width, pt) * line_h + int(Pt(BULLET_SPACE_AFTER_PT * scale))
    return h


def _table_scale(scale: float) -> float:
    """Sparse-table growth is capped lower than bullet growth (18pt max)."""
    return min(scale, K.TABLE_MAX_SCALE)


def estimate_table_height(headers, rows, width, scale: float) -> int:
    return K.estimate_table_height(headers, rows, width, scale=_table_scale(scale))


GAP = int(Inches(0.10))


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


def estimate_stack_height(blocks, width, scale: float) -> int:
    total = 0
    for b in blocks:
        callout = detect_callout_block(b)
        if callout:
            label, value = callout
            chips = _extract_chip_items(value)
            if chips:
                total += K.estimate_callout_chip_height(width, label, chips)
            else:
                total += K.estimate_callout_text_height(width, label, len(strip_markdown_title(value)))
        elif b["type"] == "bullets":
            total += estimate_bullets_height(b["items"], width, scale)
        elif b["type"] == "table":
            total += estimate_table_height(b["headers"], b["rows"], width, scale)
        else:
            continue
        total += GAP
    return total


def fit_stack_scale(blocks, width, available: int) -> float:
    stackable = [b for b in blocks if b["type"] in ("bullets", "table")]
    if not stackable:
        return 1.0
    budget = max(1, int(available * FIT_MARGIN))
    for scale in SCALE_STEPS:
        if estimate_stack_height(stackable, width, scale) <= budget:
            return scale
    return SCALE_STEPS[-1]


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


def draw_bullets(slide, x, y, width, items, scale: float) -> int:
    pt = BODY_PT_BASE * scale
    height = estimate_bullets_height(items, width, scale)
    box = K.add_textbox(slide, x, y, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for level, kind, marker, text in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(BULLET_SPACE_AFTER_PT * scale)
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


def draw_table(slide, x, y, width, headers, rows, scale: float) -> int:
    return K.add_table(slide, x, y, width, headers, rows, scale=_table_scale(scale))


def draw_stack(slide, x, y, width, blocks, scale: float, *, badge_seed: int = 0) -> int:
    cursor = y
    callout_i = 0
    for b in blocks:
        callout = detect_callout_block(b)
        if callout:
            label, value = callout
            chips = _extract_chip_items(value)
            if chips:
                h = K.add_callout_chip_card(
                    slide, x, cursor, width, label, chips,
                    badge_start=badge_seed + callout_i,
                )
            else:
                segments = parse_inline(value)
                h = K.add_callout_text_card(slide, x, cursor, width, label, segments)
            callout_i += 1
        elif b["type"] == "bullets":
            h = draw_bullets(slide, x, cursor, width, b["items"], scale)
        elif b["type"] == "table":
            h = draw_table(slide, x, cursor, width, b["headers"], b["rows"], scale)
        else:
            continue
        cursor += h + GAP
    return cursor - y


def fit_code_font(code_blocks, width, available_h) -> int:
    n = max(1, len(code_blocks))
    per_block_h = available_h / n if n > 1 else available_h
    for pt in CODE_PT_STEPS:
        ok = True
        for cb in code_blocks:
            if K.estimate_code_height(cb["text"], width, pt) > per_block_h:
                ok = False
                break
        if ok:
            return pt
    return CODE_PT_STEPS[-1]


CODE_CARD_ABS_MAX_BOTTOM = int(Inches(7.02))  # ~0.08in clear of the 7.098in footer text


def draw_code_blocks(slide, x, y, width, height, code_blocks, *, font_pt=None) -> int:
    """Draw one or more code cards.

    ``height`` is the *budget* used to pick a font size (via fit_code_font),
    but a card is sized to what its own text actually needs at that font,
    never truncated shorter -- that was the original bug: a card capped to
    the panel's nominal leftover space while its text, sized independently,
    needed a bit more, so the last line or two rendered below the card
    entirely. A card is free to grow past that nominal budget (most
    over-budget cases are only a few tenths of an inch, e.g. a dense bullet
    stack above it left less room than hoped), but never past
    CODE_CARD_ABS_MAX_BOTTOM -- an absolute slide-position ceiling clear of
    the footer -- which bounds the one remaining failure mode: a single code
    block so long that not even the smallest CODE_PT_STEPS size is close to
    fitting (which belongs split across multiple slides at the
    content-authoring stage, not shrunk to illegibility or left to push the
    card past the footer/off the slide).
    """
    n = len(code_blocks)
    if n == 0:
        return 0
    abs_max_h = max(int(Inches(0.5)), CODE_CARD_ABS_MAX_BOTTOM - y)
    if n == 2:
        gap = int(Inches(0.16))
        col_w = (width - gap) // 2
        font_pt = font_pt if font_pt is not None else fit_code_font(code_blocks, col_w, height)
        h0 = K.estimate_code_height(code_blocks[0]["text"], col_w, font_pt)
        h1 = K.estimate_code_height(code_blocks[1]["text"], col_w, font_pt)
        h = min(max(h0, h1, int(Inches(0.6))), abs_max_h)
        K.add_code_block(slide, x, y, col_w, h, code_blocks[0]["text"], font_pt=font_pt)
        K.add_code_block(slide, x + col_w + gap, y, col_w, h, code_blocks[1]["text"], font_pt=font_pt)
        return h
    # 1, or >2 stacked
    font_pt = font_pt if font_pt is not None else fit_code_font(code_blocks, width, height)
    cursor = y
    for cb in code_blocks:
        needed = K.estimate_code_height(cb["text"], width, font_pt)
        remaining_abs = max(int(Inches(0.5)), CODE_CARD_ABS_MAX_BOTTOM - cursor)
        h = max(int(Inches(0.5)), min(needed, remaining_abs))
        K.add_code_block(slide, x, cursor, width, h, cb["text"], font_pt=font_pt)
        cursor += h + GAP
    return cursor - y


# ---------------------------------------------------------------------------
# Panel heading -- an icon badge (a real emoji glyph, not a plain dot) + bold
# RED all-caps label above a bullet panel, ported from the reference theme's
# add_panel_bullets icon+heading pattern (which the split/table/code layouts
# here weren't using yet).
#
# The icon is picked by a keyword heuristic over the slide's own heading
# text -- the same semantic mapping the MD287 reference deck's authors
# applied by hand (objectives -> target, checklists/best-practice -> check
# mark, warnings/anti-patterns -> warning sign, hands-on content -> tools,
# and so on), just automated here since these decks have far too many
# slides to hand-pick one icon each. It doesn't need to be exhaustive, only
# meaningfully varied instead of one static dot everywhere -- order matters
# (more specific patterns are checked first) since some headings match more
# than one keyword.
# ---------------------------------------------------------------------------
_PANEL_ICON_RULES: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"learning objective", re.I), "🎯"),
    (re.compile(r"\b(checklist|best practice|readiness|criteria|production[- ]ready)\b", re.I), "✅"),
    (re.compile(r"\b(mistake|anti-pattern|misconception|warning|caution|risk|failure|"
                r"problem|troubleshoot|diagnos)", re.I), "⚠️"),
    (re.compile(r"^(demo|lab|exercise)\b|\bhands-on\b", re.I), "🛠️"),
    (re.compile(r"knowledge check|questions? and answers?|q&a|discussion prompt|exit ticket", re.I), "❓"),
    (re.compile(r"\b(roadmap|overview|module summary|module outcome|course wrap-up|"
                r"course summary|module completion|transition to module)\b", re.I), "🧭"),
    (re.compile(r"explain\(\)", re.I), "📊"),
    (re.compile(r"\b(metric\w*|monitor\w*|performance|statistic\w*|dashboard\w*|"
                r"aggregat\w*|report\w*|benchmark\w*)\b", re.I), "📊"),
    (re.compile(r"\b(tip|insight|example|use case|scenario)\b", re.I), "💡"),
    (re.compile(r"\b(key term|definition|glossary|terminology|what is)\b", re.I), "🔑"),
)
_PANEL_ICON_DEFAULT = "📌"


def panel_heading_icon(title: str) -> str:
    t = title or ""
    for pattern, icon in _PANEL_ICON_RULES:
        if pattern.search(t):
            return icon
    return _PANEL_ICON_DEFAULT


def panel_heading_label(title: str) -> str:
    t = (title or "").lower()
    if "learning objective" in t:
        return "YOU WILL BE ABLE TO"
    return "KEY POINTS"


def _drop_redundant_intro(blocks: list[dict]) -> list[dict]:
    """Drop a leading single-line "...:" lead-in once a heading already says it.

    e.g. "By the end of this module you will be able to:" directly above a
    bullet list is now redundant with the "YOU WILL BE ABLE TO" panel
    heading, so skip re-printing it verbatim.
    """
    if not blocks:
        return blocks
    b0 = blocks[0]
    if b0["type"] == "bullets" and len(b0["items"]) == 1:
        _level, kind, _marker, text = b0["items"][0]
        stripped = text.strip()
        if kind == "para" and stripped.endswith(":") and len(stripped) <= 110 \
                and not stripped.startswith("**"):
            return blocks[1:]
    return blocks


# ---------------------------------------------------------------------------
# Panel-level render (bullets/tables auto-fit, plus code blocks). The
# key-takeaway bar is handled at the record level (pop_keymsg / K.add_key_takeaway)
# so it always spans the full slide width and is bottom-anchored like the
# reference, regardless of which panel(s) the slide has.
#
# The whole content group (heading + bullets/table/callouts + code) is sized
# first, then vertically distributed within the available box instead of
# being pinned to the top -- this is the main fix for slides that used to
# leave the bottom 40-50% of the panel empty.
# ---------------------------------------------------------------------------
def render_panel(slide, x, y, width, height, blocks, *, title: str = "",
                  badge_color=None, badge_seed: int = 0):
    """Render a full block list into one panel. Returns which kinds were used."""
    blocks = list(blocks)
    code_blocks = [b for b in blocks if b["type"] == "code"]
    other_blocks = [b for b in blocks if b["type"] in ("bullets", "table")]

    used = {"table": any(b["type"] == "table" for b in other_blocks), "code": bool(code_blocks)}

    has_bullets = any(b["type"] == "bullets" for b in other_blocks)
    heading_label = panel_heading_label(title) if has_bullets else None
    if heading_label == "YOU WILL BE ABLE TO":
        # Only the learning-objectives panel repeats its own heading verbatim
        # as a leading "By the end of this module you will be able to:" line
        # -- drop that one redundant lead-in. A generic "KEY POINTS" panel's
        # first paragraph is real content (e.g. "For example, ..."), not a
        # restatement of the heading, so it must never be silently dropped.
        other_blocks = _drop_redundant_intro(other_blocks)
    heading_h = (K.PANEL_HEADING_H + K.PANEL_HEADING_GAP) if heading_label else 0

    code_reserve = 0
    if code_blocks:
        code_reserve = min(int(height * 0.45), max(int(Inches(1.4)), int(height * 0.35)))

    fit_available = max(int(Inches(0.3)), height - heading_h - code_reserve)
    scale = fit_stack_scale(other_blocks, width, fit_available) if other_blocks else 1.0
    stack_est = estimate_stack_height(other_blocks, width, scale) if other_blocks else 0

    code_est = 0
    font_pt = None
    if code_blocks:
        remaining_for_code = max(int(Inches(0.6)), height - heading_h - stack_est)
        font_pt = fit_code_font(code_blocks, width, remaining_for_code)
        if len(code_blocks) == 2:
            gap = int(Inches(0.16))
            col_w = (width - gap) // 2
            code_est = max(K.estimate_code_height(cb["text"], col_w, font_pt) for cb in code_blocks)
        else:
            code_est = sum(K.estimate_code_height(cb["text"], width, font_pt) + GAP for cb in code_blocks)

    total_est = heading_h + stack_est + code_est
    offset = max(0, (height - total_est) // 2)
    offset = min(offset, int(height * 0.4))
    cursor = y + offset

    if heading_label:
        K.add_panel_heading(slide, x, cursor, width, heading_label, badge_color=badge_color,
                             icon=panel_heading_icon(title))
        cursor += heading_h

    if other_blocks:
        used_h = draw_stack(slide, x, cursor, width, other_blocks, scale, badge_seed=badge_seed)
        cursor += used_h

    if code_blocks:
        remaining = max(int(Inches(0.6)), y + height - cursor)
        # Re-fit the code font against the *actual* remaining space at draw
        # time instead of reusing the earlier estimate: the bullet stack's
        # real rendered height can differ slightly from estimate_stack_height's
        # prediction (word-wrap rounding, etc.), and reusing a font chosen
        # against the stale estimate can leave a code card sized too tall for
        # what's actually left below it -- visually overflowing past its own
        # card boundary. Recomputing here is the same cost as the estimate
        # already paid and removes that whole class of mismatch.
        used_h = draw_code_blocks(slide, x, cursor, width, remaining, code_blocks)
        cursor += used_h + GAP

    return used


# ---------------------------------------------------------------------------
# Top-level: one manifest record -> one slide
# ---------------------------------------------------------------------------
CONTENT_TOP_MARGIN = int(Inches(0.10))

# Bullet panel narrower / gap tighter than before (was 4.85in / 0.25in) so the
# diagram panel gets meaningfully more width -- and since it's uniform-scaled
# and width-limited on most of these diagrams, more height too.
SPLIT_TEXT_W = int(Inches(4.20))
SPLIT_GAP = int(Inches(0.20))
SPLIT_IMAGE_X = int(K.CONTENT_X) + SPLIT_TEXT_W + SPLIT_GAP
SPLIT_IMAGE_W = int(K.CONTENT_W) - SPLIT_TEXT_W - SPLIT_GAP


def render_record(prs, layout, record: dict, page_num: int | None, kicker: str | None,
                   repo_root: Path, chips: list[str] | None = None):
    """Render one manifest record. Returns (slide_or_None, kind) where kind is
    one of 'skipped', 'title', 'diagram', 'table', 'code', 'plain'.

    ``chips`` (only used for a ``lead`` record) is the cover slide's row of
    4-5 short topic labels -- see K.add_topic_chip_row."""
    heading_raw = (record.get("heading") or "").strip()
    body_raw = record.get("body_markdown") or ""
    marp_class = (record.get("marp_class") or "").strip()

    if not heading_raw and not body_raw.strip():
        return None, "skipped"

    title = strip_markdown_title(heading_raw) or "Untitled"

    if marp_class == "lead":
        subtitle = flatten_markdown(body_raw)
        tag = (kicker or "COURSE INTRODUCTION").upper()
        slide = K.chapter_slide(
            prs, layout, tag=tag, title=title, subtitle=subtitle, module_label=tag,
            chips=chips, notes=record.get("notes"),
        )
        return slide, "title"

    slide = K.new_slide(prs, layout)
    part_label = kicker.upper() if kicker else None
    top = K.add_title_block(slide, title=title, part_label=part_label)
    top = max(top, CONTENT_TOP_MARGIN + int(Inches(0.55)))

    col_text, was_split = extract_col_text(body_raw)
    diagram_rel = record.get("diagram_png")
    diagram_path = (Path(repo_root) / diagram_rel) if diagram_rel else None
    has_diagram = bool(diagram_path and diagram_path.exists())

    blocks = parse_blocks(col_text if (was_split or has_diagram) else body_raw)
    if not was_split and not has_diagram:
        blocks = parse_blocks(body_raw)

    blocks, keymsg_text = pop_keymsg(blocks)

    # Content stops at the house TAKEAWAY_Y line (matching the reference's
    # content_slide), growing that reserve upward when a takeaway bar is
    # present so the bar never overlaps the panels above it.
    bar_growth = (
        K.takeaway_height(keymsg_text) - int(K.TAKEAWAY_H) if keymsg_text else 0
    )
    available_h = max(int(Inches(0.6)), int(K.TAKEAWAY_Y) - bar_growth - top)

    badge_seed = page_num or 0
    badge_color = K.BADGE_COLORS[badge_seed % len(K.BADGE_COLORS)]

    if has_diagram:
        # Any slide with a matched diagram (split-class or plain content-class
        # slides that also got a diagram match) gets the two-panel treatment:
        # text panel left, image panel right.
        used = render_panel(slide, K.CONTENT_X, top, SPLIT_TEXT_W, available_h, blocks,
                             title=title, badge_color=badge_color, badge_seed=badge_seed)
        K.add_picture_fitted(slide, diagram_path, SPLIT_IMAGE_X, top, SPLIT_IMAGE_W, available_h)
        kind = "diagram"
    else:
        used = render_panel(slide, K.CONTENT_X, top, K.CONTENT_W, available_h, blocks,
                             title=title, badge_color=badge_color, badge_seed=badge_seed)
        if used["table"]:
            kind = "table"
        elif used["code"]:
            kind = "code"
        else:
            kind = "plain"

    if keymsg_text:
        K.add_key_takeaway(slide, keymsg_text)

    K.add_rail_and_footer(slide, page_num)
    K.set_notes(slide, record.get("notes"))
    return slide, kind
