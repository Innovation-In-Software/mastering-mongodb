#!/usr/bin/env python3
"""Parse markdown pipe tables from Marp slide sources."""

from __future__ import annotations

import re
from pathlib import Path


def split_marp_slides(markdown: str) -> list[str]:
    text = markdown.lstrip("\ufeff")
    if text.startswith("---"):
        end = text.find("\n---\n", 3)
        if end != -1:
            text = text[end + 5 :]
    return text.split("\n---\n")


def _strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def extract_markdown_tables(slide_md: str) -> list[list[list[str]]]:
    """Return all pipe tables in a slide as row/column string grids."""
    tables: list[list[list[str]]] = []
    lines = _strip_code_fences(slide_md).splitlines()
    index = 0

    while index < len(lines):
        if not lines[index].strip().startswith("|"):
            index += 1
            continue

        block: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("|"):
            block.append(lines[index].strip())
            index += 1

        rows: list[list[str]] = []
        for line in block:
            if re.match(r"^\|[-:\s|]+\|$", line):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells:
                rows.append(cells)

        if rows:
            tables.append(rows)

    return tables


def slide_tables_from_markdown(md_path: Path) -> dict[int, list[list[list[str]]]]:
    """Map 1-based slide numbers to the tables found in that slide."""
    markdown = md_path.read_text(encoding="utf-8")
    slides = split_marp_slides(markdown)
    mapping: dict[int, list[list[list[str]]]] = {}

    for index, slide_md in enumerate(slides, start=1):
        tables = extract_markdown_tables(slide_md)
        if tables:
            mapping[index] = tables

    return mapping


def extract_fenced_code_blocks(slide_md: str) -> list[str]:
    """Return fenced ``` code block contents from a slide."""
    blocks: list[str] = []
    lines = slide_md.splitlines()
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped.startswith("```"):
            index += 1
            continue

        block_lines: list[str] = []
        index += 1
        while index < len(lines) and not lines[index].strip().startswith("```"):
            block_lines.append(lines[index])
            index += 1

        if block_lines:
            blocks.append("\n".join(block_lines))
        if index < len(lines):
            index += 1

    return blocks
