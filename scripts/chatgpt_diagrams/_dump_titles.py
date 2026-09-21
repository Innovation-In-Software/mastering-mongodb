"""Dump concept-slide titles per module to titles.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "slides" / "course-complete-marp-with-notes.md"
OUT = Path(__file__).resolve().parent / "titles.json"

SKIP = re.compile(
    r"^(Exercise|Lab|Demo|Knowledge Check|Questions|Exit Ticket|Transition|"
    r"Practical Challenge|Module \d+ Practical|Course Agenda|Mastering MongoDB|"
    r"Module Learning Objectives|Module Knowledge Check|Module Completion Checklist|"
    r"Instructor pacing|Hands-on Labs|Final Course Knowledge Assessment|"
    r"Final Practical Assessment|Participant Action Plan|Course Review|"
    r"Next Steps|Module \d+ Exit Ticket|Module 4 Exit Ticket|Module 6 Exit Ticket|"
    r"Module 7 Exit Ticket|Module 8 Completion Checklist|"
    r"Introduction to NoSQL Databases|MongoDB Installation and Setup|"
    r"Data Modeling with MongoDB|The MongoDB Query Language|"
    r"The Aggregation Framework|Indexing and Query Performance|"
    r"Introduction to Replication and Sharding|"
    r"MongoDB Best Practices, Security, and Troubleshooting)\b",
    re.I,
)
CODE_SLIDE = re.compile(r"— code\s*$")


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    parts = re.split(r"<!-- _header: 'Module (\d+)[^\n]*' -->", text)
    modules: dict[str, list[str]] = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        body = parts[i + 1]
        titles = []
        for raw in re.findall(r"^# (.+)$", body, re.M):
            t = raw.strip()
            if SKIP.search(t) or CODE_SLIDE.search(t):
                continue
            titles.append(t)
        modules[f"{n:02d}"] = titles
        print(f"Module {n}: {len(titles)} diagrams")
    OUT.write_text(json.dumps(modules, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
