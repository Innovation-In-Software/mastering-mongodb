#!/usr/bin/env python3
"""Splice rich subject-matter markdown content into a module's Marp manifest.

Reusable pipeline for replacing the thin/terse concept slides in
``scripts/marp_manifests/moduleNN.json`` with richer material supplied as a
``moduleNN_content_source.md`` file (prose paragraphs, multi-example code
blocks, comparison tables, deeper explanations) while leaving the module's
structural slides (title/lead, learning objectives, knowledge checks,
exercises/labs/demos, module summary, exit ticket, Q&A, transition) exactly
where they are.

Pipeline (generic, reusable for modules 3-8 later):

1. ``parse_source_markdown`` -- turn a ``## N. Title`` / ``### Subheading``
   content-source file into a tree of sections/subsections, each holding an
   ordered list of atomic markdown "chunks" (paragraph, bullet/numbered list,
   fenced code block, pipe table, blockquote). Chunks are the unit the
   per-module slide PLAN slices into slides -- content is never retyped by
   hand, only re-grouped.
2. A per-module ``SLIDE_PLAN`` (hand-authored list of ``SlideSpec``) says,
   for each *new* slide: which chunks from which section/subsection go on
   it, what heading to use, and (optionally) which existing diagram PNG to
   reuse. This is the "light per-module judgement call" the task allows --
   everything else here is generic.
3. ``build_new_slides`` renders each ``SlideSpec`` into a manifest-schema
   slide record: ``{global_index, marp_class, heading, body_markdown, notes,
   diagram_png?}`` -- the same schema ``mongodb_slide_render.py`` already
   consumes, so nothing downstream changes.
4. ``splice_manifest`` finds the preserve-vs-replace ranges in the existing
   ``moduleNN.json`` (also a per-module hardcoded config: front-matter
   indices to keep, the concept-slide indices to drop, and the
   exercise/lab/demo/summary indices to keep and move to the end in their
   original relative order), backs up the original manifest, and writes the
   spliced, renumbered manifest.

Usage:
    python merge_rich_content.py --module 1 --source module01_content_source.md
    python merge_rich_content.py --module 2 --source module02_content_source.md --dry-run
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
MANIFEST_DIR = SCRIPTS_DIR / "marp_manifests"
DIAGRAMS_DIR = SCRIPTS_DIR / "chatgpt_diagrams" / "diagrams"

# ---------------------------------------------------------------------------
# Step 1: parse a moduleNN_content_source.md file into sections/subsections
# of atomic markdown chunks.
# ---------------------------------------------------------------------------

_FOOTNOTE_REF_RE = re.compile(r"\s*\(\[[^\]\n]{1,60}\]\[\d+\]\)")
_FOOTNOTE_DEF_RE = re.compile(r"^\[\d+\]:\s+\S+")
_BARE_STAR_BULLET_RE = re.compile(r"^(\s*)\*(?!\*)\s+")


def _clean_line(line: str) -> str:
    line = _FOOTNOTE_REF_RE.sub("", line)
    line = _BARE_STAR_BULLET_RE.sub(r"\1- ", line)
    return line


def _strip_source_noise(text: str) -> str:
    """Drop trailing reference-style footnote link definitions and inline
    citation markers (e.g. ``([MongoDB Docs][1])``, ``[1]: https://...``)."""
    out_lines = []
    for line in text.split("\n"):
        if _FOOTNOTE_DEF_RE.match(line.strip()):
            continue
        out_lines.append(_clean_line(line))
    return "\n".join(out_lines)


_CODE_MAX_LINES = 32  # a single code card can't stay readable much beyond this
                       # even at the renderer's smallest font step (9pt) -- see
                       # CODE_PT_STEPS in mongodb_slide_render.py.


def _split_oversized_code_chunk(chunk: str) -> list[str]:
    """A single fenced code block over ``_CODE_MAX_LINES`` lines (e.g. a large
    aggregation pipeline literal) would still overflow the slide even at the
    renderer's smallest code font -- split it into several still-valid fenced
    chunks instead of ever letting one code card be the whole overflow.
    Prefers splitting at blank lines inside the fence (keeps each piece a
    clean top-level object/stage); falls back to an even line-count split if
    the block has no blank lines to split on."""
    lines = chunk.split("\n")
    if len(lines) < 3 or not lines[0].strip().startswith("```"):
        return [chunk]
    lang = lines[0].strip()[3:]
    body = lines[1:-1] if lines[-1].strip().startswith("```") else lines[1:]
    if len(body) <= _CODE_MAX_LINES:
        return [chunk]

    n_pieces = -(-len(body) // _CODE_MAX_LINES)
    target = -(-len(body) // n_pieces)

    blank_idxs = [i for i, l in enumerate(body) if l.strip() == ""]
    pieces: list[list[str]] = []
    start = 0
    while start < len(body):
        want = start + target
        hard_limit = start + _CODE_MAX_LINES  # invariant: no piece may ever exceed this
        if want >= len(body):
            pieces.append(body[start:min(len(body), hard_limit)] if len(body) > hard_limit else body[start:])
            if len(body) > hard_limit:
                start = hard_limit
                continue
            break
        # Prefer snapping the cut to a blank line near `want` (keeps each
        # piece a clean top-level object/stage) -- but only ever forward to
        # one that still respects hard_limit; a blank line further out than
        # that would silently produce an oversized piece, so it falls back
        # to the nearest blank line before `want`, or a hard line-count cut.
        forward = [b for b in blank_idxs if want <= b < hard_limit]
        cut = forward[0] if forward else None
        if cut is None:
            before = [b for b in blank_idxs if start < b < want]
            cut = before[-1] if before else want
        pieces.append(body[start:cut])
        start = cut + (1 if cut < len(body) and body[cut].strip() == "" else 0)

    return [f"```{lang}\n" + "\n".join(p).strip("\n") + "\n```" for p in pieces if any(l.strip() for l in p)]


def split_chunks(body: str) -> list[str]:
    """Split a subsection's raw markdown body into atomic top-level chunks:
    paragraph / bullet-or-numbered-list / fenced-code-block / pipe-table /
    blockquote. Blank lines separate chunks; code fences, tables, and
    blockquote runs are kept atomic (never split internally) -- except a
    single code block far too long for even the smallest slide font, which
    gets divided into several still-valid fenced pieces
    (see ``_split_oversized_code_chunk``)."""
    lines = [l for l in body.split("\n")]
    n = len(lines)
    chunks: list[str] = []
    i = 0
    list_start_re = re.compile(r"^(\s*)([-*]|\d{1,2}[.)])\s+")

    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "":
            i += 1
            continue
        if stripped == "---":
            i += 1
            continue
        if stripped.startswith("```"):
            j = i + 1
            while j < n and not lines[j].strip().startswith("```"):
                j += 1
            j = min(j + 1, n)
            chunks.extend(_split_oversized_code_chunk("\n".join(lines[i:j]).rstrip()))
            i = j
            continue
        if stripped.startswith(">"):
            j = i
            while j < n and lines[j].strip().startswith(">"):
                j += 1
            chunks.append("\n".join(lines[i:j]).rstrip())
            i = j
            continue
        if stripped.startswith("|"):
            j = i
            while j < n and lines[j].strip().startswith("|"):
                j += 1
            chunks.append("\n".join(lines[i:j]).rstrip())
            i = j
            continue
        if list_start_re.match(line):
            j = i
            while j < n and lines[j].strip() != "" and not lines[j].strip().startswith("```"):
                j += 1
            chunks.append("\n".join(lines[i:j]).rstrip())
            i = j
            continue
        # generic paragraph run
        j = i
        while (
            j < n
            and lines[j].strip() != ""
            and lines[j].strip() != "---"
            and not lines[j].strip().startswith("```")
            and not lines[j].strip().startswith("|")
            and not lines[j].strip().startswith(">")
            and not list_start_re.match(lines[j])
        ):
            j += 1
        chunks.append("\n".join(lines[i:j]).rstrip())
        i = j

    return [c for c in chunks if c.strip()]


@dataclass
class Subsection:
    title: str  # "" for a section's intro (pre-### material)
    chunks: list[str] = field(default_factory=list)


@dataclass
class Section:
    number: str
    title: str
    subsections: list[Subsection] = field(default_factory=list)  # [0] is always the intro


def _detect_heading_levels(text: str) -> tuple[int, int]:
    """Most content-source files use "## N. Title" for sections / "### Sub"
    for subsections (module01, 02, 04-07). Module 03 instead uses a single
    "# N. Title" for sections / "## Sub" for subsections. Detect which this
    file uses by finding which heading depth actually carries the numbered
    "N." sections, defaulting to the more common ##/### scheme."""
    if re.search(r"(?m)^##\s+\d+\.\s", text):
        return 2, 3
    if re.search(r"(?m)^#\s+\d+\.\s", text):
        return 1, 2
    return 2, 3


def parse_source_markdown(text: str, section_level: int | None = None,
                           subsection_level: int | None = None) -> list[Section]:
    """Parse a moduleNN_content_source.md file into an ordered list of
    Section (each a numbered "N. Title", or an unnumbered trailing section
    such as "Practical Benefits"), each holding an ordered list of Subsection
    (subsections[0] is always the section's own intro material, title="").

    Any prose before the very first section heading (module03's overview
    paragraph before "# 1. ...") is captured as a synthetic leading section
    titled "Introduction" (number="0") so it isn't silently discarded --
    a module's SLIDE_PLAN can reference it via section_num="0" like any
    other section, and it is simply omitted if the file has none.

    ``section_level``/``subsection_level`` (in '#' counts) are auto-detected
    from the file when not given -- see ``_detect_heading_levels``.
    """
    text = _strip_source_noise(text)
    if section_level is None or subsection_level is None:
        auto_sec, auto_sub = _detect_heading_levels(text)
        section_level = section_level if section_level is not None else auto_sec
        subsection_level = subsection_level if subsection_level is not None else auto_sub

    sec_num_re = re.compile(rf"^#{{{section_level}}}\s+(\d+)\.\s*(.+)$")
    sec_plain_re = re.compile(rf"^#{{{section_level}}}\s+(.+)$")
    sub_re = re.compile(rf"^#{{{subsection_level}}}\s+(.+)$")
    any_heading_re = re.compile(r"^#{1,6}\s+")

    lines = text.split("\n")
    sections: list[Section] = []
    cur_section: Section | None = None
    cur_sub: Subsection | None = None
    buf: list[str] = []
    seen_first_heading = False

    def flush():
        nonlocal buf
        if cur_sub is not None:
            cur_sub.chunks = split_chunks("\n".join(buf))
        buf = []

    def ensure_front_section():
        nonlocal cur_section, cur_sub
        if cur_section is None:
            cur_section = Section(number="0", title="Introduction")
            sections.append(cur_section)
            cur_sub = Subsection(title="")
            cur_section.subsections.append(cur_sub)

    for line in lines:
        # The file's very first heading line is always its own "# Module N:
        # Title" -- skip it unconditionally, whatever level it happens to be
        # (this must run before the section/subsection checks below, since
        # for module03 that title line would otherwise collide with the
        # single-'#' section pattern).
        if not seen_first_heading and any_heading_re.match(line):
            seen_first_heading = True
            continue

        m_num = sec_num_re.match(line)
        if m_num:
            flush()
            cur_section = Section(number=m_num.group(1), title=m_num.group(2).strip())
            sections.append(cur_section)
            cur_sub = Subsection(title="")
            cur_section.subsections.append(cur_sub)
            continue

        m_sub = sub_re.match(line)
        if m_sub:
            flush()
            ensure_front_section()
            cur_sub = Subsection(title=m_sub.group(1).strip())
            cur_section.subsections.append(cur_sub)
            continue

        # A trailing unnumbered closing section such as "## Practical Benefits"
        # / "## Practical Lab" (no leading digit) still starts a new section.
        m_plain = sec_plain_re.match(line)
        if m_plain:
            flush()
            cur_section = Section(number="", title=m_plain.group(1).strip())
            sections.append(cur_section)
            cur_sub = Subsection(title="")
            cur_section.subsections.append(cur_sub)
            continue

        ensure_front_section()
        buf.append(line)

    flush()

    # Drop the synthesized "Introduction" section if the file had no actual
    # front-matter before its first heading (the common case).
    if sections and sections[0].number == "0" and sections[0].title == "Introduction":
        if not any(sub.chunks for sub in sections[0].subsections):
            sections = sections[1:]

    return sections


def find_subsection(sections: list[Section], section_num: str, sub_title: str = "") -> Subsection:
    """``section_num`` matches a numbered section's ``number`` (e.g. "1"), or --
    for the unnumbered closing sections such as "## Practical Benefits" -- its
    ``title`` instead."""
    for sec in sections:
        if sec.number == section_num or (not sec.number and sec.title == section_num):
            for sub in sec.subsections:
                if sub.title == sub_title:
                    return sub
    raise KeyError(f"subsection not found: section={section_num!r} title={sub_title!r}")


def get_chunks(sections: list[Section], section_num: str, sub_title: str = "",
                idx: tuple[int, int | None] | None = None) -> list[str]:
    sub = find_subsection(sections, section_num, sub_title)
    chunks = sub.chunks
    if idx is None:
        return list(chunks)
    start, stop = idx
    return list(chunks[start:stop])


# ---------------------------------------------------------------------------
# Diagram matching -- explicit override wins; otherwise fuzzy-match the slide
# heading against the module's diagram filename titles.
# ---------------------------------------------------------------------------

def _norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def list_module_diagrams(module_num: int) -> dict[str, Path]:
    mod_dir = DIAGRAMS_DIR / f"module{module_num:02d}"
    out = {}
    if not mod_dir.is_dir():
        return out
    for p in sorted(mod_dir.glob("*.png")):
        title = re.sub(r"^\d+\s*-\s*", "", p.stem)
        out[title] = p
    return out


def fuzzy_find_diagram(module_num: int, query: str, threshold: float = 0.62) -> str | None:
    """Best-effort fallback matcher for future modules; explicit overrides in
    a module's SLIDE_PLAN should be preferred whenever a human already knows
    the right diagram."""
    catalog = list_module_diagrams(module_num)
    if not catalog:
        return None
    qn = _norm(query)
    best_title, best_score = None, 0.0
    for title in catalog:
        score = difflib.SequenceMatcher(None, qn, _norm(title)).ratio()
        if score > best_score:
            best_title, best_score = title, score
    if best_title and best_score >= threshold:
        rel = catalog[best_title].relative_to(REPO_ROOT)
        return str(rel).replace("\\", "/")
    return None


def best_diagram_match(module_num: int, queries: list[str], threshold: float = 0.60) -> str | None:
    """Try several candidate query strings (e.g. a bare subsection title and
    that title combined with its parent section's title, for source files
    whose subsections are too short/generic to match alone -- "Database"
    under section "1. Databases, Collections and Documents") and return the
    single best-scoring diagram across all of them, if any clears the bar."""
    catalog = list_module_diagrams(module_num)
    if not catalog:
        return None
    best_title, best_score = None, 0.0
    for query in queries:
        qn = _norm(query)
        if not qn:
            continue
        for title in catalog:
            score = difflib.SequenceMatcher(None, qn, _norm(title)).ratio()
            if score > best_score:
                best_title, best_score = title, score
    if best_title and best_score >= threshold:
        rel = catalog[best_title].relative_to(REPO_ROOT)
        return str(rel).replace("\\", "/")
    return None


# ---------------------------------------------------------------------------
# Step 2/3: SlideSpec -> manifest-schema slide record
# ---------------------------------------------------------------------------

@dataclass
class SlideSpec:
    heading: str
    parts: list[tuple[str, str, tuple[int, int | None] | None]]  # (section_num, sub_title, chunk_range)
    notes: str
    diagram: str | None = None  # explicit relative path, or None -> no diagram
    marp_class: str | None = None  # auto-picked ("split" if diagram else "content") if None
    extra_markdown: list[str] = field(default_factory=list)  # literal markdown appended after parts


def build_slide_record(sections: list[Section], spec: SlideSpec, global_index: int,
                        module_num: int) -> dict:
    body_chunks: list[str] = []
    for section_num, sub_title, idx in spec.parts:
        body_chunks.extend(get_chunks(sections, section_num, sub_title, idx))
    body_chunks.extend(spec.extra_markdown)
    body_markdown = "\n\n".join(body_chunks)

    diagram_png = spec.diagram
    marp_class = spec.marp_class or ("split" if diagram_png else "content")

    record = {
        "global_index": global_index,
        "marp_class": marp_class,
        "heading": spec.heading,
        "body_markdown": body_markdown,
        "notes": spec.notes,
    }
    if diagram_png:
        full = REPO_ROOT / diagram_png
        if not full.exists():
            raise FileNotFoundError(f"diagram not found for slide {spec.heading!r}: {diagram_png}")
        record["diagram_png"] = diagram_png
    return record


def build_new_slides(sections: list[Section], plan: list[SlideSpec], start_index: int,
                      module_num: int) -> list[dict]:
    out = []
    for i, spec in enumerate(plan):
        out.append(build_slide_record(sections, spec, start_index + i, module_num))
    return out


# ---------------------------------------------------------------------------
# Generic auto-planner -- for modules whose subsections are too numerous/dense
# to hand-author one SlideSpec at a time (e.g. module04's dozens of small
# `db.collection.method()` operator examples). Packs each subsection's chunks
# into one or more slides by a weight budget (so several short, closely
# related snippets land on one slide instead of one slide each, but a slide
# never gets so dense the render font-ladder would have to shrink to
# unreadable sizes), and fuzzy-matches a diagram for the first slide of each
# subsection. A module can still override specific headings' diagrams or
# suppress a bad fuzzy match via `diagram_overrides` / `skip_diagram_for`.
# ---------------------------------------------------------------------------

def estimate_chunk_weight(chunk: str) -> int:
    """Crude density proxy (same spirit as the renderer's char-count-based
    font ladder): a fenced code block or table gets extra weight per
    character (monospace/cell padding reads "wider") plus a flat per-chunk
    overhead for its card/row chrome and inter-block spacing."""
    body = chunk.strip()
    n = len(chunk)
    if body.startswith("```"):
        return int(n * 1.20) + 90
    if body.startswith("|"):
        return int(n * 1.15) + 70
    return n + 45


def pack_chunks(chunks: list[str], budget: int = 850, max_chunks: int = 6) -> list[tuple[int, int]]:
    """Greedily group consecutive chunks into (start, stop) ranges that stay
    under a weight budget -- consolidates several small, related chunks onto
    one slide, and splits a subsection across multiple slides once it's too
    dense for one. A single oversized chunk still gets its own range rather
    than being silently dropped.

    A budget-triggered cut never leaves a range with only its first chunk --
    a short one-line lead-in ("Course progression can be summarized as
    follows:") immediately followed by one large table/code chunk would
    otherwise get stranded as its own near-empty slide just because adding
    that next (heavy) chunk alone would blow the budget. The max_chunks cap
    still applies from the first chunk, and a single chunk that's already
    oversized on its own still becomes its own range once a 2nd chunk is
    considered."""
    if not chunks:
        return []
    ranges: list[tuple[int, int]] = []
    start = 0
    total = 0
    count = 0
    for i, c in enumerate(chunks):
        w = estimate_chunk_weight(c)
        over_budget = count >= 2 and total + w > budget
        if count > 0 and (over_budget or count >= max_chunks):
            ranges.append((start, i))
            start, total, count = i, 0, 0
        total += w
        count += 1
    ranges.append((start, len(chunks)))
    return ranges


def make_auto_plan(module_num: int, *, budget: int = 850, max_chunks: int = 6,
                    diagram_threshold: float = 0.60, fold_intro_ratio: float = 0.40,
                    diagram_overrides: dict[str, str] | None = None,
                    skip_diagram_for: "set[str] | None" = None,
                    note_max: int = 200):
    """Return a plan_fn(sections) -> list[SlideSpec] for merge_rich_content's
    generic auto-planner (see module-level docstring above)."""
    diagram_overrides = diagram_overrides or {}
    skip_diagram_for = skip_diagram_for or set()
    used_diagrams: set[str] = set()

    def pick_diagram(topic: str, sec_title: str = "") -> str | None:
        if topic in diagram_overrides:
            d = diagram_overrides[topic]
            used_diagrams.add(d)
            return d
        if topic in skip_diagram_for:
            return None
        # Try the bare topic first, and -- for source files whose subsection
        # titles are too short/generic to match alone (a single word like
        # "Database" or "Field") -- also try it combined with the parent
        # section's title, taking whichever scores higher.
        queries = [topic]
        if sec_title and sec_title != topic:
            queries.append(f"{sec_title} {topic}")
        d = best_diagram_match(module_num, queries, threshold=diagram_threshold)
        if d and d not in used_diagrams:
            used_diagrams.add(d)
            return d
        return None

    _skip_prefix_re = re.compile(r"^(```|\||>|-|\*)|^\d+[.)]\s")
    _bare_label_re = re.compile(r"^`([^`]{1,28})`$")

    def cont_heading(base: str, chunks: list[str]) -> str:
        """A continuation slide's heading: if this range's own chunks open
        with one or more bare "`$operator`"-style mini-labels (module04/05's
        convention for a flat run of short operator examples with no ###
        subheading of their own), name the slide after them instead of a
        generic "(cont.)" -- e.g. "General Update Operators -- $mul, $min"."""
        labels = []
        for c in chunks:
            m = _bare_label_re.match(c.strip())
            if m:
                labels.append(m.group(1))
            if len(labels) >= 3:
                break
        if labels:
            return f"{base} — {', '.join(labels)}"
        return f"{base} (cont.)"

    def make_note(sub_title: str, chunks: list[str]) -> str:
        for c in chunks:
            s = c.strip()
            if not s or _skip_prefix_re.match(s):
                continue
            s = re.sub(r"\s+", " ", s)
            if len(s) > note_max:
                s = s[:note_max].rsplit(" ", 1)[0] + "..."
            return s
        return f"Covers {sub_title}."

    def plan_fn(sections: list[Section]) -> list[SlideSpec]:
        specs: list[SlideSpec] = []
        for sec in sections:
            subs = sec.subsections
            intro = subs[0] if subs and subs[0].title == "" else None
            named_subs = [s for s in subs if s.title != ""]
            intro_chunks = intro.chunks if intro else []
            intro_weight = sum(estimate_chunk_weight(c) for c in intro_chunks)
            sec_key = sec.number or sec.title

            fold_intro = bool(intro_chunks) and bool(named_subs) \
                and intro_weight < budget * fold_intro_ratio
            intro_folded = False

            if intro_chunks and not fold_intro:
                heading = sec.title or (intro.title or "Overview")
                for j, (a, b) in enumerate(pack_chunks(intro_chunks, budget, max_chunks)):
                    slide_heading = heading if j == 0 else cont_heading(heading, intro_chunks[a:b])
                    specs.append(SlideSpec(
                        heading=slide_heading,
                        parts=[(sec_key, "", (a, b))],
                        diagram=pick_diagram(heading, sec.title) if j == 0 else None,
                        notes=make_note(heading, intro_chunks[a:b]),
                    ))

            for sub in named_subs:
                ranges = pack_chunks(sub.chunks, budget, max_chunks)
                if not ranges:
                    continue
                for j, (a, b) in enumerate(ranges):
                    parts = []
                    if j == 0 and fold_intro and not intro_folded:
                        parts.append((sec_key, "", (0, None)))
                        intro_folded = True
                    parts.append((sec_key, sub.title, (a, b)))
                    slide_heading = sub.title if j == 0 else cont_heading(sub.title, sub.chunks[a:b])
                    specs.append(SlideSpec(
                        heading=slide_heading,
                        parts=parts,
                        diagram=pick_diagram(sub.title, sec.title) if j == 0 else None,
                        notes=make_note(sub.title, sub.chunks[a:b]),
                    ))

            # A section with an intro that never got folded in (no named
            # subsections at all) is already fully handled above; a section
            # whose intro was meant to fold in but had no named subsections
            # to fold onto can't happen (fold_intro requires named_subs).
        return specs

    return plan_fn


# ---------------------------------------------------------------------------
# Step 4: splice into the existing manifest
# ---------------------------------------------------------------------------

@dataclass
class ModuleConfig:
    front_preserve: list[int]      # global_index values kept at the very front, in order
    end_preserve: list[int]        # global_index values kept at the end, in original relative order
    # everything else in the manifest (any global_index not in front_preserve/end_preserve)
    # is a concept slide and gets dropped/replaced.
    plan_fn: "callable"            # (sections) -> list[SlideSpec]


def splice_manifest(manifest_path: Path, sections: list[Section], config: ModuleConfig,
                     module_num: int) -> tuple[list[dict], dict]:
    original = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_index = {rec["global_index"]: rec for rec in original}

    missing_front = [i for i in config.front_preserve if i not in by_index]
    missing_end = [i for i in config.end_preserve if i not in by_index]
    if missing_front or missing_end:
        raise KeyError(f"preserve indices not found in manifest: front={missing_front} end={missing_end}")

    kept_indices = set(config.front_preserve) | set(config.end_preserve)
    replaced = [rec for rec in original if rec["global_index"] not in kept_indices]

    plan = config.plan_fn(sections)
    new_slides = build_new_slides(sections, plan, start_index=0, module_num=module_num)

    spliced = (
        [by_index[i] for i in config.front_preserve]
        + new_slides
        + [by_index[i] for i in config.end_preserve]
    )
    for n, rec in enumerate(spliced, start=1):
        rec["global_index"] = n

    stats = {
        "original_total": len(original),
        "front_preserved": len(config.front_preserve),
        "end_preserved": len(config.end_preserve),
        "concept_slides_replaced": len(replaced),
        "concept_slides_replaced_headings": [r["heading"] for r in replaced],
        "new_slide_count": len(new_slides),
        "new_slide_headings": [s["heading"] for s in new_slides],
        "new_total": len(spliced),
        "diagrams_reused": [s.get("diagram_png") for s in new_slides if s.get("diagram_png")],
    }
    return spliced, stats


def run(module_num: int, source_path: Path, dry_run: bool = False) -> dict:
    from module_slide_plans import MODULE_CONFIGS  # local import: per-module plans

    if module_num not in MODULE_CONFIGS:
        raise SystemExit(f"no SLIDE_PLAN configured for module {module_num} yet -- add one to "
                          f"module_slide_plans.py")
    config = MODULE_CONFIGS[module_num]

    source_text = source_path.read_text(encoding="utf-8")
    sections = parse_source_markdown(source_text)

    manifest_path = MANIFEST_DIR / f"module{module_num:02d}.json"
    spliced, stats = splice_manifest(manifest_path, sections, config, module_num)

    if not dry_run:
        backup_path = manifest_path.with_suffix(".json.orig-terse")
        if not backup_path.exists():
            shutil.copy2(manifest_path, backup_path)
        manifest_path.write_text(json.dumps(spliced, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", type=int, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source_path = args.source if args.source.is_absolute() else (SCRIPTS_DIR / args.source)
    stats = run(args.module, source_path, dry_run=args.dry_run)

    print(f"=== module {args.module:02d} {'(dry run)' if args.dry_run else ''} ===")
    print(f"  original slides          : {stats['original_total']}")
    print(f"  front preserved          : {stats['front_preserved']}")
    print(f"  end preserved            : {stats['end_preserved']}")
    print(f"  concept slides replaced  : {stats['concept_slides_replaced']}")
    print(f"  -> became new slides     : {stats['new_slide_count']}")
    print(f"  new total slides         : {stats['new_total']}")
    print(f"  diagrams reused          : {len(stats['diagrams_reused'])}")
    for d in stats["diagrams_reused"]:
        print(f"      {d}")


if __name__ == "__main__":
    main()
