#!/usr/bin/env python3
"""Sync beginner step summaries from slide-exercises into course Marp exercise slides (modules 5-10)."""

from __future__ import annotations

import re
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md, lab_guides_dir
from marp_tables import split_marp_slides

DECK = deck_md()
SE = lab_guides_dir()

_EXERCISE_SLIDE = re.compile(r"^##\s+Exercise\s+(\d+)\.(\d+)\s+—\s+Steps", re.MULTILINE)
_STEP = re.compile(
    r"###\s+Step\s+(\d+)\s+—\s+(.+?)\n\n"
    r"\*\*Do this[^*]*\*\*:?\s*(.*?)\n\n"
    r"\*\*Expected result:\*\*\s*(.+?)(?=\n\n---|\n\n###|\Z)",
    re.DOTALL | re.IGNORECASE,
)

_CLEANUPS = [
    (
        r"\*\*Platform:\*\* Windows 10/11 · \*\*PowerShell\*\* ``Ctrl\+` `` \(Git Bash/WSL for `\.sh` scripts\)\s*\n*",
        "**Windows:** Use **PowerShell** in Cursor (``Ctrl+` `` → **PowerShell**)\n\n",
    ),
    (
        r"\*\*Demonstration \(Windows\):\*\* \*\*PowerShell\*\* terminal \(``Ctrl\+` ``\) · Agent panel ``Ctrl\+I`` · shortcuts use \*\*Ctrl\*\*\s*\n*",
        "",
    ),
    (
        r"\*\*Terminal:\*\* \*\*PowerShell\*\* — unless step notes Git Bash or WSL\s*\n*",
        "",
    ),
    (
        r"\*\*Terminal:\*\* \*\*PowerShell\*\* — ``Ctrl\+` `` in Cursor\s*\n*",
        "",
    ),
    (
        r"\*\*Where:\*\* \*\*Agent panel\*\* — ``Ctrl\+I``\s*\n*",
        "**Where:** Cursor **Agent** panel (`Ctrl+I`)\n\n",
    ),
    (
        r"\*\*Where:\*\* \*\*Web browser\*\* — Edge or Chrome\s*\n*",
        "**Where:** Web browser (Edge or Chrome)\n\n",
    ),
]


def _visible(slide: str) -> str:
    return re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()


def _parse_steps(guide_path: Path) -> list[dict[str, str]]:
    text = guide_path.read_text(encoding="utf-8")
    start = text.find("## Steps from the training slides")
    if start == -1:
        return []
    end = text.find("\n---\n\n## ", start + 10)
    section = text[start:end] if end != -1 else text[start:]
    steps = []
    for m in _STEP.finditer(section):
        do = re.sub(r"\s+", " ", m.group(3).strip())[:220]
        exp = re.sub(r"\s+", " ", m.group(4).strip())[:160]
        steps.append({"n": m.group(1), "title": m.group(2).strip(), "do": do, "exp": exp})
    return steps


def _summary_block(steps: list[dict[str, str]], max_steps: int = 3) -> str:
    if not steps:
        return ""
    lines = ["**Follow along (Windows) — key steps:**", ""]
    for s in steps[:max_steps]:
        lines.append(f"**Step {s['n']} — {s['title']}**")
        do = s["do"].replace("```", "").strip()
        lines.append(f"- **Do:** {do}")
        lines.append(f"- **Expected:** {s['exp']}")
        lines.append("")
    lines.append(
        "_Full lab guide with every command: see **Lab guide** on the lesson divider slide._\n"
    )
    return "\n".join(lines)


def _inject_summary(slide: str, summary: str) -> str:
    parts = slide.split("\n<!--\n", 1)
    body = parts[0]
    comments = ("\n<!--\n" + parts[1]) if len(parts) > 1 else ""
    if "**Follow along (Windows)" in body:
        body = re.sub(
            r"\*\*Follow along \(Windows\).*?(?=\n\n\*\*Step |\n\n\*\*Windows:|\n\n## |\Z)",
            summary.rstrip() + "\n\n",
            body,
            count=1,
            flags=re.DOTALL,
        )
    else:
        m = _EXERCISE_SLIDE.search(body)
        if m:
            rest = body[m.end() :].lstrip("\n")
            if rest.startswith("**Windows:**"):
                body = body[: m.end()] + "\n\n" + summary + "\n" + rest
            else:
                body = body[: m.end()] + "\n\n" + summary + "\n\n" + rest
    return body + comments


def sync_deck(modules: range) -> int:
    text = DECK.read_text(encoding="utf-8")
    fm_end = text.find("\n---\n", 3) + 5
    frontmatter = text[:fm_end]
    slides = split_marp_slides(text[fm_end:])
    current_module: int | None = None
    seen_exercises: set[tuple[int, int]] = set()
    changed = 0

    guides: dict[tuple[int, int], list[dict]] = {}
    for mod in modules:
        folder = SE / f"module-{mod:02d}"
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("exercise-*.md")):
            m = re.search(r"exercise-(\d+)\.(\d+)", path.name)
            if m:
                guides[(int(m.group(1)), int(m.group(2)))] = _parse_steps(path)

    new_slides: list[str] = []
    for slide in slides:
        hdr = re.search(r"<!--\s*_header:\s*['\"]Module\s+(\d+)", slide)
        if hdr:
            current_module = int(hdr.group(1))

        body = slide
        for pat, repl in _CLEANUPS:
            body = re.sub(pat, repl, body)

        if current_module in modules and _EXERCISE_SLIDE.search(_visible(body)):
            body = re.sub(
                r"```bash\n(agent[^\n]*)\n```",
                r"```powershell\n\1\n```",
                body,
                count=1,
            )
            body = body.replace(
                "Write a bash function that checks if a port is in use",
                "Write a PowerShell function that checks if a TCP port is in use",
            )
            body = body.replace(
                'agent --model gpt-5-mini "What does this command do: ls -la | grep .txt"',
                'agent --model gpt-5-mini "What does this command do: Get-ChildItem | Where-Object Name -like \'*.txt\'"',
            )

        em = _EXERCISE_SLIDE.search(_visible(body))
        if em and current_module in modules:
            mod, ex = int(em.group(1)), int(em.group(2))
            key = (mod, ex)
            if key not in seen_exercises and key in guides:
                seen_exercises.add(key)
                summary = _summary_block(guides[key])
                if summary:
                    body = _inject_summary(body, summary)
                    changed += 1

        new_slides.append(body)

    out = frontmatter + "\n\n" + "\n\n---\n\n".join(s.rstrip() for s in new_slides) + "\n"
    DECK.write_text(out, encoding="utf-8")
    print(f"Updated {changed} first exercise slides in {DECK.name}")
    return changed


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from course_config import modules as config_modules

    mod_ids = [int(m["id"]) for m in config_modules()]
    sync_deck(range(min(mod_ids), max(mod_ids) + 1) if mod_ids else range(1, 2))
