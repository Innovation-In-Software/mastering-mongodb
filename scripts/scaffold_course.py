#!/usr/bin/env python3
"""Bootstrap a new DrKaur course under D:\\Current_work from this template."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path(r"D:\Current_work")
TEMPLATE_ROOT = Path(__file__).resolve().parent.parent

SKIP_COPY = {
    ".git",
    "__pycache__",
    ".cursor",
    "slides/course-complete-marp-with-notes.html",
    "slides/course-complete-speaker-notes.md",
}


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "new-course"


def _parse_toc_modules(toc_path: Path) -> list[dict]:
    modules: list[dict] = []
    for line in toc_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+Module\s+(\d+)\.\s+(.+)$", line.strip())
        if m:
            modules.append({"id": int(m.group(1)), "title": m.group(2).strip(), "day": 1, "duration_minutes": 60})
    return modules


def _write_course_config(
    dest: Path,
    *,
    name: str,
    subtitle: str,
    org: str,
    days: int,
    modules: list[dict],
) -> None:
    header = f"{name} — Complete Course"
    lines = [
        "course:",
        f'  name: "{name}"',
        f'  subtitle: "{subtitle}"',
        f'  org: "{org}"',
        f'  header: "{header}"',
        f"  days: {days}",
        "",
        "paths:",
        "  deck_md: slides/course-complete-marp-with-notes.md",
        "  deck_html: slides/course-complete-marp-with-notes.html",
        "  speaker_notes: slides/course-complete-speaker-notes.md",
        "  lab_guides: slide-exercises",
        "  assets: slides/assets",
        "",
        "modules:",
    ]
    for mod in modules:
        lines.extend(
            [
                f"  - id: {mod['id']}",
                f'    title: "{mod["title"]}"',
                f"    day: {mod.get('day', 1)}",
                f"    duration_minutes: {mod.get('duration_minutes', 60)}",
            ]
        )
    (dest / "course.config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_toc(dest: Path, *, name: str, days: int, modules: list[dict]) -> None:
    total_min = sum(m.get("duration_minutes", 60) for m in modules)
    hours = total_min / 60
    day_label = f"{days} day{'s' if days != 1 else ''}"

    lines = [
        f"# {name} — Table of Contents",
        "",
        f"Generated from scaffold on {date.today().isoformat()}.",
        "",
        "---",
        "",
        "## At a Glance",
        "",
        "| | |",
        "|---|---|",
        f"| **Duration** | {day_label} (~{hours:.1f} hours) |",
        f"| **Modules** | {len(modules)} |",
        "| **Slide deck (present)** | [`slides/course-complete-marp-with-notes.html`](slides/course-complete-marp-with-notes.html) |",
        "| **Slide deck (source)** | [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |",
        "| **Cheatsheet** | [`COURSE-CHEATSHEET.md`](COURSE-CHEATSHEET.md) |",
        "",
        "---",
        "",
        "## Module Index",
        "",
        "| # | Day | Module | Duration | Slide deck |",
        "|---|-----|--------|----------|------------|",
    ]
    for mod in modules:
        dur = mod.get("duration_minutes", 60)
        lines.append(
            f"| **{mod['id']}** | Day {mod.get('day', 1)} | {mod['title']} | ~{dur} min | "
            f"[`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |"
        )
    lines.extend(["", "---", ""])
    for mod in modules:
        lines.extend(
            [
                f"## Module {mod['id']}. {mod['title']}",
                "",
                "| Lesson | Title | Duration | Exercise |",
                "|--------|-------|----------|----------|",
                f"| {mod['id']}.1 | TBD | TBD | — |",
                "",
            ]
        )
    (dest / "FINAL_TABLE_OF_CONTENTS.md").write_text("\n".join(lines), encoding="utf-8")


def _write_cheatsheet(dest: Path, modules: list[dict]) -> None:
    lines = [
        "# Course Cheatsheet",
        "",
        "Acronyms, definitions, and quick references by module.",
        "",
        "---",
        "",
    ]
    for mod in modules:
        lines.extend(
            [
                f"## Module {mod['id']} — {mod['title']}",
                "",
                "| Term | Definition |",
                "|------|------------|",
                "| _TBD_ | Add terms as you author this module |",
                "",
            ]
        )
    (dest / "COURSE-CHEATSHEET.md").write_text("\n".join(lines), encoding="utf-8")


def _write_deck(
    dest: Path,
    *,
    name: str,
    subtitle: str,
    org: str,
    days: int,
    modules: list[dict],
) -> None:
    header = f"{name} — Complete Course"
    day_word = f"{days}-day" if days != 1 else "1-day"
    module_range = f"Modules 1–{len(modules)}" if len(modules) > 1 else "Module 1"

    lines = [
        "---",
        "marp: true",
        "theme: flat-gaia",
        "paginate: true",
        f"header: '{header}'",
        "---",
        "",
        "",
        "<!-- _class: lead -->",
        "",
        f"# {name}",
        "",
        f"## {subtitle}",
        "",
        f"{org} · {day_word} instructor-led course · {module_range}",
        "",
        "<!--",
        f"Welcome to {name}. Replace this opener with your instructor script.",
        "",
        f"{org} · {day_word} instructor-led course · {module_range}.",
        "-->",
        "",
        "---",
        "",
        "",
        "## Course Agenda",
        "",
        "| Module | Title | Day | Duration |",
        "|--------|-------|-----|----------|",
    ]
    for mod in modules:
        dur = mod.get("duration_minutes", 60)
        lines.append(f"| **{mod['id']}** | {mod['title']} | Day {mod.get('day', 1)} | ~{dur} min |")

    total_min = sum(m.get("duration_minutes", 60) for m in modules)
    lines.extend(
        [
            "",
            f"**Total:** ~{total_min / 60:.1f} hours across {days} day{'s' if days != 1 else ''}",
            "",
            "<!--",
            "Course agenda — keep in sync with FINAL_TABLE_OF_CONTENTS.md.",
            "-->",
            "",
            "---",
            "",
        ]
    )

    for mod in modules:
        lines.extend(
            [
                f"<!-- _header: 'Module {mod['id']} — {mod['title']}' -->",
                "",
                "<!-- _class: lead -->",
                "",
                f"# {mod['title']}",
                "",
                "Module overview — add lessons and exercises below",
                "",
                "<!--",
                f"Module {mod['id']} opener. Add lesson and exercise slides after this divider.",
                "-->",
                "",
                "---",
                "",
            ]
        )

    deck_path = dest / "slides" / "course-complete-marp-with-notes.md"
    deck_path.parent.mkdir(parents=True, exist_ok=True)
    deck_path.write_text("\n".join(lines), encoding="utf-8")


def _write_readme(dest: Path, *, name: str, slug: str) -> None:
    text = f"""# {name}

Instructor-led course built from the DrKaur course template.

## Quick start

1. Review [`FINAL_TABLE_OF_CONTENTS.md`](FINAL_TABLE_OF_CONTENTS.md)
2. Edit slides in [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)
3. Add lab guides under [`slide-exercises/`](slide-exercises/)
4. Export HTML:

```powershell
npx @marp-team/marp-cli slides/course-complete-marp-with-notes.md `
  --html --allow-local-files `
  --theme-set scripts/themes/flat-gaia.css `
  -o slides/course-complete-marp-with-notes.html
```

5. Present from [`slides/course-complete-marp-with-notes.html`](slides/course-complete-marp-with-notes.html)

See [`COURSE-AUTHORING-GUIDE.md`](COURSE-AUTHORING-GUIDE.md) for the full workflow.

## Location

`D:\\Current_work\\{slug}\\`
"""
    (dest / "README.md").write_text(text, encoding="utf-8")


def _ensure_module_dirs(dest: Path, modules: list[dict]) -> None:
    for mod in modules:
        mid = mod["id"]
        (dest / "slide-exercises" / f"module-{mid:02d}").mkdir(parents=True, exist_ok=True)
        (dest / "slides" / "assets" / f"module-{mid:02d}").mkdir(parents=True, exist_ok=True)


def _copy_template(dest: Path) -> None:
    if dest.exists():
        raise FileExistsError(f"Destination already exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    def _ignore(directory: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        rel = Path(directory).relative_to(TEMPLATE_ROOT).as_posix()
        for name in names:
            rel_path = f"{rel}/{name}" if rel != "." else name
            if name in SKIP_COPY or rel_path in SKIP_COPY:
                ignored.add(name)
        return ignored

    shutil.copytree(TEMPLATE_ROOT, dest, ignore=_ignore)


def _default_modules(count: int, days: int) -> list[dict]:
    modules: list[dict] = []
    for i in range(1, count + 1):
        day = 1 if i <= (count + 1) // 2 else min(days, 2)
        if days == 1:
            day = 1
        modules.append(
            {
                "id": i,
                "title": f"Module {i}",
                "day": day,
                "duration_minutes": 60,
            }
        )
    return modules


def scaffold_course(
    *,
    name: str,
    slug: str,
    org: str,
    days: int,
    modules: list[dict],
    output_dir: Path,
    from_toc: Path | None = None,
) -> Path:
    if from_toc and from_toc.is_file():
        parsed = _parse_toc_modules(from_toc)
        if parsed:
            modules = parsed

    dest = output_dir / slug
    _copy_template(dest)

    subtitle = f"{days}-day instructor-led course" if days != 1 else "Instructor-led course"
    _write_course_config(dest, name=name, subtitle=subtitle, org=org, days=days, modules=modules)
    _write_toc(dest, name=name, days=days, modules=modules)
    _write_cheatsheet(dest, modules=modules)
    _write_deck(dest, name=name, subtitle=subtitle, org=org, days=days, modules=modules)
    _write_readme(dest, name=name, slug=slug)
    _ensure_module_dirs(dest, modules)

    skill_src = TEMPLATE_ROOT / ".cursor" / "skills" / "drkaur-course-design"
    skill_dst = dest / ".cursor" / "skills" / "drkaur-course-design"
    if skill_src.is_dir():
        shutil.copytree(skill_src, skill_dst)

    return dest


def _prompt(text: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or default


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="Course display name")
    parser.add_argument("--slug", help="Folder slug under output dir")
    parser.add_argument("--org", default="DrKaur", help="Organization / author name")
    parser.add_argument("--days", type=int, default=1, help="Number of course days")
    parser.add_argument("--modules", type=int, default=1, help="Number of modules")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--from-toc", type=Path, help="Pre-fill module titles from an outline markdown file")
    args = parser.parse_args()

    name = args.name or _prompt("Course name", "My New Course")
    slug = args.slug or _slugify(name)
    org = args.org
    days = max(1, args.days)
    module_count = max(1, args.modules)
    modules = _default_modules(module_count, days)

    try:
        dest = scaffold_course(
            name=name,
            slug=slug,
            org=org,
            days=days,
            modules=modules,
            output_dir=args.output_dir,
            from_toc=args.from_toc,
        )
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created course at {dest}")
    print(f"Next: cd {dest}")
    print("  1. Edit FINAL_TABLE_OF_CONTENTS.md")
    print("  2. Author slides and lab guides (see COURSE-AUTHORING-GUIDE.md)")
    print("  3. Export HTML with Marp CLI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
