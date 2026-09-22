#!/usr/bin/env python3
"""Parse the Mastering MongoDB Marp deck into per-module JSON manifests.

Reads slides/course-complete-marp-with-notes.md, splits it into a flat,
ordered list of slide records, segments that list into the course intro,
the 8 course modules, and (if present) a course-closing tail, and cross
references each module's content slides against the diagram titles in
scripts/chatgpt_diagrams/titles.json to attach a `diagram_png` path where
a confident match is found.

Module boundaries are detected via the Marp `_header` directive that Marp
uses to render the running per-slide header. Exactly one slide per module
carries a directive of the form:

    <!-- _header: 'Module N — <Module Title>' -->

immediately followed (on the same slide, before any other directive/heading)
by `<!-- _class: lead -->` and an `# <Module Title>` heading. This pattern
was verified against the live file (see docstring at bottom / _summary.json)
rather than assumed.

Standard library only: re, json, pathlib, argparse, dataclasses.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DECK_PATH = REPO_ROOT / "slides" / "course-complete-marp-with-notes.md"
TITLES_PATH = REPO_ROOT / "scripts" / "chatgpt_diagrams" / "titles.json"
DIAGRAMS_DIR = REPO_ROOT / "scripts" / "chatgpt_diagrams" / "diagrams"
OUT_DIR = REPO_ROOT / "scripts" / "marp_manifests"

# The exact directive pattern used to detect a module's title/divider slide.
HEADER_DIRECTIVE_RE = re.compile(r"^_header:\s*(.*)$", re.IGNORECASE)
CLASS_DIRECTIVE_RE = re.compile(r"^_class:\s*(.*)$", re.IGNORECASE)
MODULE_HEADER_VALUE_RE = re.compile(
    r"^['\"]?Module\s+(\d+)\s*[—–:\-]?\s*(.*?)['\"]?$"
)
HEADING_LINE_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)\s*$", re.MULTILINE)
COMMENT_RE = re.compile(r"<!--([\s\S]*?)-->")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)
SLIDE_SEP_RE = re.compile(r"(?m)^---[ \t]*$")


@dataclass
class Slide:
    global_index: int
    marp_class: str
    heading: str
    body_markdown: str
    notes: str
    # Internal only (not exported verbatim in the public schema dict, but
    # kept on the object for module-boundary detection and diagnostics).
    header_directive: str = ""
    diagram_png: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "global_index": self.global_index,
            "marp_class": self.marp_class,
            "heading": self.heading,
            "body_markdown": self.body_markdown,
            "notes": self.notes,
        }
        if self.diagram_png is not None:
            d["diagram_png"] = self.diagram_png
        return d


def parse_slides(text: str) -> list[Slide]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("Expected a Marp YAML frontmatter block at the top of the file")
    body = text[m.end():]

    chunks = SLIDE_SEP_RE.split(body)
    slides: list[Slide] = []

    for i, raw_chunk in enumerate(chunks, start=1):
        chunk = raw_chunk
        marp_class = ""
        header_directive = ""

        # Consume leading directive comments (_class / _header), in
        # whatever order/number they appear, before any real content.
        pos = 0
        stripped = chunk.lstrip("\r\n \t")
        consumed_leading = len(chunk) - len(stripped)
        cursor = consumed_leading
        while True:
            m2 = re.match(r"\s*<!--(.*?)-->", chunk[cursor:], re.DOTALL)
            if not m2:
                break
            inner = m2.group(1).strip()
            class_m = CLASS_DIRECTIVE_RE.match(inner)
            header_m = HEADER_DIRECTIVE_RE.match(inner)
            if class_m:
                marp_class = class_m.group(1).strip()
            elif header_m:
                header_directive = header_m.group(1).strip().strip("'\"")
            else:
                # Not a directive comment -> stop; this is real content
                # (or, in a degenerate single-comment slide, the notes).
                break
            cursor += m2.end()

        rest = chunk[cursor:]

        # Trailing notes comment: the LAST comment in `rest`, only if
        # nothing but whitespace follows it.
        notes = ""
        visible = rest
        comments = list(COMMENT_RE.finditer(rest))
        if comments:
            last = comments[-1]
            if rest[last.end():].strip() == "":
                notes = last.group(1).strip()
                visible = rest[: last.start()]

        visible = visible.strip("\r\n")

        heading = ""
        body_markdown = visible.strip()
        hm = HEADING_LINE_RE.search(visible)
        if hm:
            heading = hm.group(2).strip()
            body_markdown = visible[hm.end():].strip("\r\n").strip()

        slides.append(
            Slide(
                global_index=i,
                marp_class=marp_class,
                heading=heading,
                body_markdown=body_markdown,
                notes=notes,
                header_directive=header_directive,
            )
        )

    return slides


def find_module_boundaries(slides: list[Slide]) -> dict[int, int]:
    """Return {module_number: 0-based index into `slides`} for each
    slide carrying a `_header: 'Module N — ...'` directive."""
    boundaries: dict[int, int] = {}
    for idx, s in enumerate(slides):
        if not s.header_directive:
            continue
        mm = MODULE_HEADER_VALUE_RE.match(s.header_directive)
        if mm:
            num = int(mm.group(1))
            boundaries[num] = idx
    return boundaries


def normalize_title(s: str) -> str:
    s = s.strip()
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-")
    s = s.replace("`", "")
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def sanitize_filename_title(title: str) -> str:
    """Mirror scripts/chatgpt_diagrams/runner.py:filename_for()."""
    out = title
    for ch in '/\\:?*"|<>':
        out = out.replace(ch, "-")
    out = out.replace("`", "")
    return out


def match_diagrams_for_module(
    module_no: int, module_slides: list[Slide], titles: list[str]
) -> tuple[list[dict], list[dict]]:
    """Greedy, order-preserving match of `titles` against the headings of
    `module_slides` starting at local slide 3 (slide 1 = divider, slide 2 =
    agenda/objectives). Returns (matches, unmatched) diagnostic lists and
    mutates matched Slide objects' `diagram_png`."""
    candidates = [
        (local_idx, s) for local_idx, s in enumerate(module_slides, start=1) if local_idx >= 3
    ]
    norm_candidates = [(local_idx, s, normalize_title(s.heading)) for local_idx, s in candidates]

    matches: list[dict] = []
    unmatched: list[dict] = []
    pos = 0
    mod_key = f"{module_no:02d}"

    for title_idx, title in enumerate(titles):
        norm_title = normalize_title(title)
        found_j = None
        for j in range(pos, len(norm_candidates)):
            if norm_candidates[j][2] == norm_title:
                found_j = j
                break
        png_name = f"{title_idx + 3:03d} - {sanitize_filename_title(title)}.png"
        png_rel = f"scripts/chatgpt_diagrams/diagrams/module{mod_key}/{png_name}"
        png_abs_exists = (DIAGRAMS_DIR / f"module{mod_key}" / png_name).is_file()

        if found_j is not None:
            local_idx, slide, _ = norm_candidates[found_j]
            if png_abs_exists:
                slide.diagram_png = png_rel
            matches.append(
                {
                    "title_index": title_idx,
                    "title": title,
                    "slide_index_in_module": local_idx,
                    "heading": slide.heading,
                    "global_index": slide.global_index,
                    "diagram_png": png_rel if png_abs_exists else None,
                    "png_exists": png_abs_exists,
                }
            )
            pos = found_j + 1
        else:
            nearby = [
                {"slide_index_in_module": c[0], "heading": c[1].heading}
                for c in candidates[max(0, pos - 1) : pos + 3]
            ]
            unmatched.append(
                {
                    "title_index": title_idx,
                    "title": title,
                    "expected_png": png_rel,
                    "png_exists": png_abs_exists,
                    "nearby_headings": nearby,
                }
            )

    return matches, unmatched


def main() -> None:
    text = DECK_PATH.read_text(encoding="utf-8")
    slides = parse_slides(text)

    titles = json.loads(TITLES_PATH.read_text(encoding="utf-8"))

    boundaries = find_module_boundaries(slides)
    missing = [n for n in range(1, 9) if n not in boundaries]
    if missing:
        raise SystemExit(
            f"Could not find module boundary marker(s) for module(s): {missing}. "
            "Expected a slide with <!-- _header: 'Module N — ...' -->."
        )

    ordered_bounds = sorted(boundaries.items())  # [(1, idx1), (2, idx2), ...]

    course_intro = slides[: ordered_bounds[0][1]]
    module_slice: dict[int, list[Slide]] = {}
    for i, (num, start_idx) in enumerate(ordered_bounds):
        end_idx = ordered_bounds[i + 1][1] if i + 1 < len(ordered_bounds) else len(slides)
        module_slice[num] = slides[start_idx:end_idx]
    course_closing: list[Slide] = []  # nothing follows module 8's own end marker

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = {
        "deck_path": str(DECK_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "total_slides_parsed": len(slides),
        "module_boundary_pattern": (
            r"<!-- _header: 'Module N — <Module Title>' --> immediately "
            r"followed by <!-- _class: lead --> and an '# <Module Title>' heading "
            r"on the same slide"
        ),
        "course_intro_slide_count": len(course_intro),
        "course_closing_slide_count": len(course_closing),
        "modules": {},
    }

    # course_intro.json
    (OUT_DIR / "course_intro.json").write_text(
        json.dumps([s.to_dict() for s in course_intro], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    # course_closing.json (empty list currently; kept for schema completeness)
    (OUT_DIR / "course_closing.json").write_text(
        json.dumps([s.to_dict() for s in course_closing], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    for num in range(1, 9):
        mod_slides = module_slice[num]
        mod_key = f"{num:02d}"
        mod_titles = titles.get(mod_key, [])

        matches, unmatched = match_diagrams_for_module(num, mod_slides, mod_titles)

        (OUT_DIR / f"module{mod_key}.json").write_text(
            json.dumps([s.to_dict() for s in mod_slides], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        summary["modules"][mod_key] = {
            "divider_heading": mod_slides[0].heading if mod_slides else None,
            "slide_count": len(mod_slides),
            "global_index_range": [mod_slides[0].global_index, mod_slides[-1].global_index]
            if mod_slides
            else None,
            "diagram_title_count": len(mod_titles),
            "matched_count": len(matches),
            "unmatched_count": len(unmatched),
            "matched_png_missing_on_disk": sum(1 for m in matches if not m["png_exists"]),
            "unmatched_titles": unmatched,
        }

    (OUT_DIR / "_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # ---- console report ----
    print(f"Parsed {len(slides)} slides from {DECK_PATH.relative_to(REPO_ROOT)}")
    print(f"course_intro: {len(course_intro)} slides")
    for num in range(1, 9):
        mk = f"{num:02d}"
        info = summary["modules"][mk]
        print(
            f"module{mk}: {info['slide_count']} slides | "
            f"diagrams matched {info['matched_count']}/{info['diagram_title_count']} "
            f"(unmatched {info['unmatched_count']}, "
            f"png missing on disk for {info['matched_png_missing_on_disk']} matches)"
        )
    print(f"course_closing: {len(course_closing)} slides")
    print(f"\nManifests written to {OUT_DIR.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
