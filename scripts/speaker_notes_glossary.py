"""Expand acronyms and define technical terms for read-aloud speaker notes."""

from __future__ import annotations

import re
from dataclasses import dataclass

from marp_tables import extract_fenced_code_blocks


@dataclass(frozen=True)
class GlossaryEntry:
    key: str
    speech: str
    full_form: str | None = None
    aliases: tuple[str, ...] = ()


def _entries() -> list[GlossaryEntry]:
    return []


def _slide_corpus(slide: str, heading: str) -> str:
    body = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL)
    body = extract_fenced_code_blocks(body)
    return f"{heading}\n{body}".lower()


def glossary_notes_for_slide(slide: str, heading: str, *, max_notes: int = 8) -> list[str]:
    corpus = _slide_corpus(slide, heading)
    matched: set[str] = set()
    notes: list[str] = []

    for entry in _entries():
        if entry.key in matched:
            continue
        patterns = [re.compile(re.escape(entry.key), re.I)]
        if entry.full_form:
            patterns.append(re.compile(re.escape(entry.full_form), re.I))
        for alias in entry.aliases:
            patterns.append(re.compile(re.escape(alias), re.I))
        if any(p.search(corpus) for p in patterns):
            matched.add(entry.key)
            notes.append(entry.speech)
        if len(notes) >= max_notes:
            break

    return notes
