"""Optional speakable instructor scripts keyed by slide topic."""

from __future__ import annotations

import re
from dataclasses import dataclass

ENRICHMENT_RULES: list[tuple[str, str | None, list[str]]] = []
MODULE_FRAMING: dict[int, list[str]] = {}


@dataclass
class EnrichmentMatch:
    paragraphs: list[str]


def match_enrichment(heading: str, kind: str, module: int | None) -> EnrichmentMatch:
    h = heading.lower()
    paragraphs: list[str] = []

    for pattern, kind_filter, tips in ENRICHMENT_RULES:
        if kind_filter and kind_filter != kind:
            continue
        if re.search(pattern, h, re.I):
            paragraphs.extend(tips)

    if module and module in MODULE_FRAMING and kind == "module_intro":
        paragraphs = MODULE_FRAMING[module] + paragraphs

    seen: set[str] = set()
    unique: list[str] = []
    for p in paragraphs:
        if p not in seen:
            seen.add(p)
            unique.append(p)

    return EnrichmentMatch(paragraphs=unique[:4])


EXERCISE_STEP_SPEECH: dict[tuple[int, int], dict[str, list[str]]] = {}


def exercise_step_speech(module: int, ex_num: int, heading: str, *, first_step: bool = False) -> list[str]:
    speech_map = EXERCISE_STEP_SPEECH.get((module, ex_num), {})
    h = heading.lower()
    if first_step:
        setup = speech_map.get("setup", [])
        if setup:
            return setup
    for key, lines in speech_map.items():
        if key == "default":
            continue
        if key in h:
            return lines
    return speech_map.get("default", [])
