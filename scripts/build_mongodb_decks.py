#!/usr/bin/env python3
"""CLI driver: manifest JSON -> native .pptx deck for Mastering MongoDB.

Usage:
    python build_mongodb_decks.py --intro
    python build_mongodb_decks.py --module 1
    python build_mongodb_decks.py --all
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
    records = json.loads(manifest_path.read_text(encoding="utf-8"))
    prs = K.new_presentation()
    layout = K.blank_layout(prs)

    stats = {"title": 0, "diagram": 0, "table": 0, "code": 0, "plain": 0, "skipped": 0}
    page_num = 0
    seen_lead = False

    for record in records:
        marp_class = (record.get("marp_class") or "").strip()
        is_lead = marp_class == "lead"
        kicker = default_kicker_fn(record, is_lead and not seen_lead)
        if is_lead:
            seen_lead = True
            slide, kind = R.render_record(prs, layout, record, None, kicker, REPO_ROOT, chips=chips)
        else:
            page_num += 1
            slide, kind = R.render_record(prs, layout, record, page_num, kicker, REPO_ROOT)
            if slide is None:
                page_num -= 1  # skipped record didn't consume a page number

        stats[kind] = stats.get(kind, 0) + 1

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
    print(f"  title slides   : {stats['title']}")
    print(f"  diagram slides : {stats['diagram']}")
    print(f"  table slides   : {stats['table']}")
    print(f"  code slides    : {stats['code']}")
    print(f"  plain bullets  : {stats['plain']}")
    print(f"  skipped blanks : {stats['skipped']}")


def build_intro() -> dict:
    def kicker_fn(record, is_first_lead):
        return None if is_first_lead else "Course Introduction"

    out_path = OUT_DIR / "MongoDB_Course_Introduction.pptx"
    stats = build_deck(MANIFEST_DIR / "course_intro.json", out_path, default_kicker_fn=kicker_fn,
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", type=int, action="append", choices=range(1, 9),
                        help="Build a single module deck (1-8). May be repeated.")
    parser.add_argument("--intro", action="store_true", help="Build the course-introduction deck.")
    parser.add_argument("--all", action="store_true", help="Build the intro deck and all 8 modules.")
    args = parser.parse_args()

    if not (args.module or args.intro or args.all):
        parser.error("nothing to do -- pass --intro, --module N, or --all")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if args.all:
        build_intro()
        for n in range(1, 9):
            build_module(n)
    else:
        if args.intro:
            build_intro()
        for n in sorted(set(args.module or [])):
            build_module(n)

    print(f"\nDone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
