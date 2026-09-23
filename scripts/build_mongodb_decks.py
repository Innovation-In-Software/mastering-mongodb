#!/usr/bin/env python3
"""CLI driver: manifest JSON -> native .pptx deck for Mastering MongoDB.

Usage:
    python build_mongodb_decks.py --day 1          # one day deck (intro + that day's modules)
    python build_mongodb_decks.py --all            # all three day decks
    python build_mongodb_decks.py --intro          # standalone intro deck
    python build_mongodb_decks.py --module 1       # standalone module deck
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import yaml
from pptx import Presentation

import fix_docprops_slide_count as docprops
import mongodb_deck_kit as K
import mongodb_slide_render as R

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = REPO_ROOT / "scripts" / "marp_manifests"
OUT_DIR = REPO_ROOT / "decks" / "pptx"
CONFIG_PATH = REPO_ROOT / "course.config.yaml"

MODULE_FILE_SLUGS = {
    1: "Introduction_to_NoSQL_Databases",
    2: "Installation_and_Setup",
    3: "Data_Modeling_with_MongoDB",
    4: "The_MongoDB_Query_Language",
    5: "The_Aggregation_Framework",
    6: "Indexing_and_Query_Performance",
    7: "Introduction_to_Replication_and_Sharding",
    8: "MongoDB_Best_Practices_Security_and_Troubleshooting",
}

# Cover-slide topic-chip row (K.add_topic_chip_row) -- 4-5 short labels per
# deck, derived from that module's own top-level "## N. Title" sections in
# its moduleNN_content_source.md (the same section lists the merge pipeline
# parses for rich content), shortened to chip-width-friendly phrases. Key 0
# is the course-introduction deck's own cover slide.
MODULE_TOPIC_CHIPS: dict[int, list[str]] = {
    0: ["NoSQL & MongoDB Basics", "Data Modeling & Queries", "Aggregation & Indexing",
        "Replication & Sharding", "Production Best Practices"],
    1: ["Defining NoSQL", "Document, KV & Graph Stores", "MongoDB Architecture",
        "Core Features", "Practical Benefits"],
    2: ["Choosing a Deployment", "Installing MongoDB", "Connecting with mongosh",
        "First MongoDB Commands", "Troubleshooting Connections"],
    3: ["Databases, Collections & Documents", "BSON & Data Types", "Access-Pattern Design",
        "Embedding vs Referencing", "Common Modeling Mistakes"],
    4: ["Basic Retrieval", "Comparison & Logical Operators", "Querying Arrays",
        "Update Operators", "Safe Data Manipulation"],
    5: ["Pipeline Structure", "$match & $group Stages", "$project & $sort Stages",
        "$lookup & $facet", "Pipeline Performance"],
    6: ["How Indexes Work", "Compound Indexes", "Specialized Index Types",
        "Covered Queries & Selectivity", "Common Indexing Mistakes"],
    7: ["Replication vs Sharding", "Replica Set Fundamentals", "Write & Read Concerns",
        "Sharded Cluster Components", "Choosing a Shard Key"],
    8: ["Data Modeling Guidelines", "Performance & Indexing", "Security Considerations",
        "Backups & Troubleshooting", "Production Readiness"],
}


# Day decks -- file names come from the README "Three-day outline" themes.
# Which modules belong to each day comes from course.config.yaml.
DAY_FILE_SLUGS = {
    1: "Run_MongoDB_and_Model_Documents",
    2: "Query_and_Transform_Data",
    3: "Tune_Scale_and_Ship",
}


def load_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def module_out_name(n: int) -> str:
    return f"MongoDB_Module{n:02d}_{MODULE_FILE_SLUGS[n]}.pptx"


def build_deck(manifest_path: Path, out_path: Path, *, default_kicker_fn, chips: list[str] | None = None) -> dict:
    """Render every record in manifest_path into a new deck at out_path.

    default_kicker_fn(record, is_first_lead) -> kicker string or None.
    chips -- this deck's cover-slide topic-chip row (only used on the lead
    record; see MODULE_TOPIC_CHIPS).
    """
    return build_combined_deck([(manifest_path, default_kicker_fn, chips)], out_path)


def build_combined_deck(segments: list[tuple[Path, object, list[str] | None]], out_path: Path) -> dict:
    """Render several manifests, in order, into one deck at out_path.

    Each segment is (manifest_path, kicker_fn, chips). Every segment keeps its
    own lead/cover slide and chips; page numbers run on through the whole deck.
    """
    prs = K.new_presentation()
    layout = K.blank_layout(prs)

    stats = {"title": 0, "topics": 0, "packed": 0, "skipped": 0}
    page_num = 0

    for manifest_path, default_kicker_fn, chips in segments:
        records = json.loads(manifest_path.read_text(encoding="utf-8"))
        # "X" / "X (cont.)" source records become one flow, re-paginated to fill slides.
        records = R.merge_continuations(records)
        # Topics between cover slides are packed as one continuous 20pt flow
        # (R.render_flow): topics share slides, diagrams float beside text.
        run: list[dict] = []

        def flush():
            nonlocal page_num
            if run:
                slides = R.render_flow(prs, layout, run, page_num + 1, REPO_ROOT)
                page_num += len(slides)
                stats["topics"] += len(run)
                stats["packed"] += len(slides)
                run.clear()

        for record in records:
            if (record.get("marp_class") or "").strip() == "lead":
                flush()
                R.render_record(prs, layout, record, None, None, REPO_ROOT, chips=chips)
                stats["title"] += 1
            elif (record.get("heading") or "").strip() or any(
                    (p.get("body_markdown") or "").strip() for p in record["_parts"]):
                run.append(record)
            else:
                stats["skipped"] += 1
        flush()

    K.save_presentation(prs, out_path)

    # docProps slide-count fix -- prevents PowerPoint's repair dialog.
    docprops.process(out_path, check_only=False)

    # Round-trip validation.
    reopened = Presentation(str(out_path))
    actual = len(reopened.slides)
    stats["written_slides"] = actual
    stats["file_size_kb"] = out_path.stat().st_size // 1024
    return stats


def print_summary(name: str, stats: dict) -> None:
    print(f"\n=== {name} ===")
    print(f"  slides written : {stats['written_slides']}")
    print(f"  file size      : {stats['file_size_kb']} KB")
    print(f"  cover slides   : {stats['title']}")
    print(f"  topics         : {stats['topics']}  packed onto {stats['packed']} content slides")
    print(f"  skipped blanks : {stats['skipped']}")


def build_intro() -> dict:
    out_path = OUT_DIR / "MongoDB_Course_Introduction.pptx"
    stats = build_deck(MANIFEST_DIR / "course_intro.json", out_path, default_kicker_fn=intro_kicker,
                        chips=MODULE_TOPIC_CHIPS[0])
    print_summary(out_path.name, stats)
    return stats


def build_module(n: int) -> dict:
    def kicker_fn(record, is_first_lead):
        return f"Module {n}"

    manifest_path = MANIFEST_DIR / f"module{n:02d}.json"
    out_path = OUT_DIR / module_out_name(n)
    stats = build_deck(manifest_path, out_path, default_kicker_fn=kicker_fn,
                        chips=MODULE_TOPIC_CHIPS.get(n))
    print_summary(out_path.name, stats)
    return stats


def day_out_name(day: int) -> str:
    return f"MongoDB_Day{day}_{DAY_FILE_SLUGS[day]}.pptx"


def intro_kicker(record, is_first_lead):
    return None if is_first_lead else "Course Introduction"


def build_day(day: int) -> dict:
    """Day deck: Day 1 opens with the course introduction, then each module
    assigned to that day in course.config.yaml, in module order."""
    modules = sorted(m["id"] for m in load_config()["modules"] if m["day"] == day)
    if not modules:
        raise SystemExit(f"course.config.yaml assigns no modules to day {day}")

    segments = []
    if day == 1:
        segments.append((MANIFEST_DIR / "course_intro.json", intro_kicker, MODULE_TOPIC_CHIPS[0]))
    for n in modules:
        segments.append((MANIFEST_DIR / f"module{n:02d}.json",
                         lambda record, is_first_lead, n=n: f"Day {day} · Module {n}",
                         MODULE_TOPIC_CHIPS.get(n)))

    out_path = OUT_DIR / day_out_name(day)
    stats = build_combined_deck(segments, out_path)
    print_summary(f"{out_path.name} (modules {', '.join(map(str, modules))})", stats)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", type=int, action="append", choices=range(1, 9),
                        help="Build a single module deck (1-8). May be repeated.")
    parser.add_argument("--intro", action="store_true", help="Build the course-introduction deck.")
    parser.add_argument("--day", type=int, action="append", choices=range(1, 4),
                        help="Build a day deck (1-3). May be repeated.")
    parser.add_argument("--all", action="store_true", help="Build all three day decks.")
    args = parser.parse_args()

    if not (args.module or args.intro or args.day or args.all):
        parser.error("nothing to do -- pass --day N, --all, --intro, or --module N")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if args.all:
        for day in (1, 2, 3):
            build_day(day)
    else:
        for day in sorted(set(args.day or [])):
            build_day(day)
        if args.intro:
            build_intro()
        for n in sorted(set(args.module or [])):
            build_module(n)

    print(f"\nDone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
