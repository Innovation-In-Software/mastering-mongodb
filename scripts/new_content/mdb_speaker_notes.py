#!/usr/bin/env python3
"""Instructor speaker notes for the MD287 day decks.

Notes are authored as JSON in scripts/speaker_notes/dayN/*.json, keyed by a
stable unit key, and composed into each slide at build time -- so rebuilding
the decks never loses them. The authoring schema is documented in
scripts/speaker_notes/README.md.

Unit keys (stable across rebuilds):
    cover:dayN              day cover slide
    branding                TEKsystems branding slide (shared by all days)
    module:MN               module divider slide
    topic:MN:<number>       a module topic -- rendered as text, as part of a
                            merged slide, or as its own module diagram
    exercise:ex-<id>        checkpoint exercise slide
    lab-divider:dayN        lab section divider
    lab:<number>            lab slide (e.g. lab1-3)
    daydiagram:<path>       curriculum slide diagram, path relative to curriculum/
    closing:dayN            day closing slide
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

NL = chr(10)
NOTES_DIR = Path(__file__).resolve().parent / "speaker_notes"
BRANDING_KEY = "branding"
_ABBREV = {
    "e.g.", "i.e.", "vs.", "etc.", "mr.", "mrs.", "ms.", "dr.",
    "u.s.", "u.k.", "fig.", "no.", "inc.", "ltd.", "co.",
}

_units: dict[str, dict] | None = None
MISSING: list[str] = []
INVENTORY: list[dict] = []


# ---------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------
def cover_key(day: int) -> str:
    return f"cover:day{day}"


def module_key(module: int) -> str:
    return f"module:M{module}"


def topic_key(module: int, number) -> str:
    return f"topic:M{module}:{number}"


def exercise_key(number: str) -> str:
    return f"exercise:{number}"


def lab_divider_key(day: int) -> str:
    return f"lab-divider:day{day}"


def lab_key(number: str) -> str:
    return f"lab:{number}"


def closing_key(day: int) -> str:
    return f"closing:day{day}"


def day_diagram_key(root: Path, path: Path) -> str:
    curriculum = (Path(root) / "curriculum").resolve()
    try:
        rel = Path(path).resolve().relative_to(curriculum).as_posix()
    except ValueError:
        rel = Path(path).name
    return f"daydiagram:{rel}"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def units() -> dict[str, dict]:
    global _units
    if _units is None:
        _units = {}
        for path in sorted(NOTES_DIR.rglob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            _units.update(data.get("units", {}))
    return _units


def reload() -> None:
    global _units
    _units = None


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------
def _clean(text) -> str:
    return " ".join(str(text or "").split())


def _norm(text) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


def _sentences(text: str) -> list[str]:
    """Split into sentences so the notes pane can put a blank line between them."""
    text = _clean(text)
    if not text:
        return []
    parts = re.split(r"(?<=[.?!])\s+", text)
    merged: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if merged:
            last_word = merged[-1].split()[-1]
            if last_word.lower() in _ABBREV or re.fullmatch(r"[A-Za-z]\.", last_word):
                merged[-1] = merged[-1] + " " + part
                continue
        merged.append(part)
    return merged


def _spaced(text: str, indent: str = "") -> list[str]:
    lines: list[str] = []
    for sentence in _sentences(text):
        lines.append(indent + sentence)
        lines.append("")
    return lines


def _section(title: str, lines: list[str]) -> list[str]:
    if not any(line.strip() for line in lines):
        return []
    return [title, "-" * len(title), "", *lines, ""]


def _point_blocks(unit: dict, headings=None) -> list[str]:
    points = [p for p in unit.get("talking_points") or [] if _clean(p.get("explain"))]
    if headings:
        wanted = {_norm(h) for h in headings if h}
        chosen = [p for p in points if _norm(p.get("point")) in wanted]
        if chosen:
            points = chosen
    out: list[str] = []
    for p in points:
        out.append("- " + _clean(p.get("point")))
        out.append("")
        out.extend(_spaced(_clean(p.get("explain")), indent="  "))
    return out


def _example_blocks(unit: dict) -> list[str]:
    out: list[str] = []
    for example in unit.get("real_world_examples") or []:
        if not _clean(example):
            continue
        sentences = _sentences(example)
        if not sentences:
            continue
        out.append("- " + sentences[0])
        out.append("")
        for sentence in sentences[1:]:
            out.append("  " + sentence)
            out.append("")
    return out


def compose(unit: dict, *, headings=None, part: int = 1, parts: int = 1,
            as_diagram: bool = False, header: str | None = None) -> str:
    """Key points, examples, and a use case, spaced for the notes pane."""
    out: list[str] = []
    if header:
        out += [header, "-" * min(len(header), 42), ""]
    out += _section("KEY TALKING POINTS", _point_blocks(unit, None if as_diagram else headings))
    out += _section("REAL-WORLD EXAMPLES", _example_blocks(unit))
    out += _section("USE-CASE SCENARIO", _spaced(unit.get("use_case_scenario")))
    return NL.join(out).strip()


def notes_for(key: str, fallback: str | None = None, **kwargs) -> str | None:
    unit = units().get(key)
    if unit is None:
        MISSING.append(key)
        return fallback
    return compose(unit, **kwargs)


def legacy_topic_block(title: str, subtitle: str, takeaway: str) -> str:
    return NL.join([title, subtitle, "KEY TAKEAWAY: " + takeaway])


def merged_notes(keys: list[str], titles: list[str], legacy: list[str]) -> str:
    """One block per topic sharing the slide, each headed so it is easy to find."""
    blocks = []
    total = len(keys)
    for index, (key, title, old) in enumerate(zip(keys, titles, legacy), start=1):
        header = f"TOPIC {index} OF {total}: {title}"
        text = notes_for(key, header=header)
        blocks.append(text if text else old)
    return (NL + NL + NL).join(blocks)


# ---------------------------------------------------------------------------
# Slide inventory (what each slide shows, for authoring and checking notes)
# ---------------------------------------------------------------------------
def record(**entry) -> None:
    if os.environ.get("MD287_SLIDE_INVENTORY"):
        INVENTORY.append(entry)


def finish_day(day: int) -> list[str]:
    """Write the inventory if requested; return unit keys that had no notes."""
    target = os.environ.get("MD287_SLIDE_INVENTORY")
    if target:
        path = Path(target.replace("{day}", str(day)))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"day": day, "slides": INVENTORY}, indent=1, ensure_ascii=False),
            encoding="utf-8",
        )
    missing = sorted(set(MISSING))
    INVENTORY.clear()
    MISSING.clear()
    return missing
