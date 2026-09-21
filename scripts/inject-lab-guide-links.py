#!/usr/bin/env python3
"""Add lab guide links to the first slide of each hands-on exercise block."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md, lab_guides_dir, repo_root
from marp_tables import split_marp_slides

REPO = repo_root()
DEFAULT_DECK = deck_md()
_EXERCISE_HEADING = re.compile(r"^##\s+Exercise\s+(\d+)\.(\d+)\s+—", re.MULTILINE)


def _visible(slide: str) -> str:
    return re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()


def _lab_path(module: int, exercise: int) -> str | None:
    folder = lab_guides_dir() / f"module-{module:02d}"
    matches = sorted(folder.glob(f"exercise-{module}.{exercise}-*.md"))
    if not matches:
        return None
    return matches[0].relative_to(REPO).as_posix().replace("\\", "/")


def _inject(slide: str, rel_path: str, label: str) -> str:
    link = f"**Lab guide:** [`{label}`](../{rel_path})\n\n"
    parts = slide.split("\n<!--\n", 1)
    body = parts[0]
    rest = ("\n<!--\n" + parts[1]) if len(parts) > 1 else ""
    lines = body.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            insert_at = i + 1
            while insert_at < len(lines) and not lines[insert_at].strip():
                insert_at += 1
            break
    lines.insert(insert_at, link.rstrip())
    return "\n".join(lines) + rest


def inject_all(markdown: str) -> tuple[str, int]:
    end = markdown.find("\n---\n", 3)
    frontmatter = markdown[: end + 5]
    slides = split_marp_slides(markdown[end + 5 :])
    seen: set[tuple[int, int]] = set()
    count = 0

    for i, slide in enumerate(slides):
        visible = _visible(slide)
        m = _EXERCISE_HEADING.search(visible)
        if not m:
            continue
        mod, ex = int(m.group(1)), int(m.group(2))
        if (mod, ex) in seen:
            continue
        if "**Lab guide:**" in visible:
            seen.add((mod, ex))
            continue
        path = _lab_path(mod, ex)
        if not path:
            continue
        seen.add((mod, ex))
        slides[i] = _inject(slide, path, f"Exercise {mod}.{ex}")
        count += 1

    body = "\n\n---\n\n".join(s.rstrip() for s in slides) + "\n"
    return frontmatter + "\n\n" + body, count


def main() -> int:
    path = DEFAULT_DECK
    text = path.read_text(encoding="utf-8")
    updated, n = inject_all(text)
    path.write_text(updated, encoding="utf-8")
    print(f"Injected {n} lab guide links into {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
