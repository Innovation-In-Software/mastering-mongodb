#!/usr/bin/env python3
"""Write labs/EXERCISES-INDEX.md, labs/LABS-INDEX.md and labs/README.md.

The indexes are generated from the files on disk (titles come from each file's
first "# " heading), so rerun this after adding or renaming a worksheet or lab:

    python scripts/new_content/build_lab_indexes.py

Layout (same convention as the MD287 course):
    labs/day-0D/exercises/exercise-M.N-<slug>.md            participant worksheet
    labs/day-0D/exercises/solution/exercise-M.N-<slug>.md   instructor answer key
    labs/day-0D/labL/LAB-L-GUIDE.md                         day lab guide
    labs/day-0D/labL/solution/LAB-L-SOLUTION.md             expected outputs
    labs/practice-exercises/module-0M-README.md             in-slide practice answers
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LABS = ROOT / "labs"
CONFIG = yaml.safe_load((ROOT / "course.config.yaml").read_text(encoding="utf-8"))
MODULES = {m["id"]: m for m in CONFIG["modules"]}
DECK = {
    1: "MongoDB_Module01_Introduction_to_NoSQL_Databases",
    2: "MongoDB_Module02_Installation_and_Setup",
    3: "MongoDB_Module03_Data_Modeling_with_MongoDB",
    4: "MongoDB_Module04_The_MongoDB_Query_Language",
    5: "MongoDB_Module05_The_Aggregation_Framework",
    6: "MongoDB_Module06_Indexing_and_Query_Performance",
    7: "MongoDB_Module07_Introduction_to_Replication_and_Sharding",
    8: "MongoDB_Module08_Best_Practices_Security_and_Troubleshooting",
}
# Each day lab closes the module it follows.
LAB_AFTER_MODULE = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}


def title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def short(t: str) -> str:
    return re.sub(r"^(Exercise \d+\.\d+|Lab \d+)\s*[—-]\s*", "", t)


def rel(p: Path) -> str:
    return p.relative_to(LABS).as_posix()


def exercises():
    rows = []
    for p in LABS.glob("day-0*/exercises/exercise-*.md"):
        m = re.match(r"exercise-(\d+)\.(\d+)-", p.name)
        rows.append((int(m.group(1)), int(m.group(2)), p))
    return sorted(rows)


def labs():
    rows = []
    for p in LABS.glob("day-0*/lab*/LAB-*-GUIDE.md"):
        n = int(re.search(r"LAB-(\d+)-GUIDE", p.name).group(1))
        rows.append((n, p))
    return sorted(rows)


def solution_for(worksheet: Path) -> Path:
    return worksheet.parent / "solution" / worksheet.name


def lab_solution(guide: Path, n: int) -> Path:
    return guide.parent / "solution" / f"LAB-{n}-SOLUTION.md"


def link(p: Path, text: str) -> str:
    return f"[{text}]({rel(p)})" if p.exists() else f"{text} (missing)"


def exercises_index() -> str:
    out = ["# Exercises — official checkpoints",
           "",
           "These worksheets are the **official numbered checkpoints** in the module decks "
           "(`decks/pptx_new/`). They are numbered by module in the order they appear on the slides "
           "(Exercise *M.N* = module *M*, checkpoint *N*). Each has a participant worksheet and a "
           "separate instructor answer key in the day's `exercises/solution/` folder.",
           "",
           "In-slide **practice exercises** (unnumbered \"PRACTICE EXERCISE\" slides) have reference "
           "answers in [practice-exercises/](practice-exercises/).",
           "",
           "| # | Module | Day | Worksheet | Answer key |",
           "| - | ------ | --- | --------- | ---------- |"]
    for mod, n, p in exercises():
        m = MODULES[mod]
        out.append(f"| {mod}.{n} | {mod} {m['title']} | {m['day']} | {link(p, short(title(p)))} | "
                   f"{link(solution_for(p), 'solution')} |")
    out += ["", "## Practice-exercise answers (in-slide activities)", ""]
    for mod in sorted(MODULES):
        p = LABS / "practice-exercises" / f"module-{mod:02d}-README.md"
        out.append(f"- Module {mod} — {MODULES[mod]['title']}: {link(p, rel(p))}")
    out += ["", "Superseded guides from the earlier course layout are kept in "
                "[`../archive/slide-exercises/`](../archive/slide-exercises/) for reference only.", ""]
    return "\n".join(out)


def labs_index() -> str:
    out = ["# Labs — one hands-on lab per module block",
           "",
           "Seven sequenced labs run on the shared `training_store` dataset "
           "([`datasets/training_store/load.js`](../datasets/training_store/load.js)). Each lab is the "
           "last official slide of the module it follows. Every lab has a participant guide and an "
           "instructor solution with the expected output of each step.",
           "",
           "| Lab | Day | After module | Guide | Solution |",
           "| --- | --- | ------------ | ----- | -------- |"]
    for n, p in labs():
        mod = LAB_AFTER_MODULE[n]
        day = int(p.parts[-3][-2:])
        out.append(f"| {n} | {day} | {mod} {MODULES[mod]['title']} | {link(p, short(title(p)))} | "
                   f"{link(lab_solution(p, n), 'solution')} |")
    out += ["",
            "Reload `training_store` at the start of Day 2 and Day 3 (and whenever a lab's "
            "*Before you start* section asks):",
            "",
            "```powershell",
            'mongosh "mongodb://localhost:27017" .\\datasets\\training_store\\load.js',
            "```",
            "",
            "Superseded day-lab files from the earlier layout are in [`../archive/labs/`](../archive/labs/).",
            ""]
    return "\n".join(out)


def readme() -> str:
    out = ["# Labs and exercises",
           "",
           "Everything learners do hands-on, in the order it happens in the module decks "
           "(`decks/pptx_new/`). Indexes: [EXERCISES-INDEX.md](EXERCISES-INDEX.md) · "
           "[LABS-INDEX.md](LABS-INDEX.md).",
           "",
           "```text",
           "labs/",
           "  day-01/  exercises/ (1.x-3.x)  exercises/solution/  lab1/  lab2/",
           "  day-02/  exercises/ (4.x-5.x)  exercises/solution/  lab3/  lab4/",
           "  day-03/  exercises/ (6.x-8.x)  exercises/solution/  lab5/  lab6/  lab7/",
           "  practice-exercises/            module-01-README.md ... module-08-README.md",
           "```",
           "",
           "## Sequence by day",
           ""]
    ex = exercises()
    lab_rows = dict(labs())
    for day in sorted({m["day"] for m in MODULES.values()}):
        out.append(f"### Day {day}")
        out.append("")
        for mod in sorted(k for k, m in MODULES.items() if m["day"] == day):
            m = MODULES[mod]
            deck = DECK[mod]
            items = [f"{mod}.{n} {short(title(p))}" for mm, n, p in ex if mm == mod]
            line = f"- **Module {mod} — {m['title']}** (`decks/pptx_new/{deck}.pptx`)"
            out.append(line)
            if items:
                out.append("  - Exercises: " + " · ".join(items))
            for n, after in LAB_AFTER_MODULE.items():
                if after == mod and n in lab_rows:
                    out.append(f"  - Then **Lab {n} — {short(title(lab_rows[n]))}**: "
                               f"[{rel(lab_rows[n])}]({rel(lab_rows[n])})")
        out.append("")
    out += ["## Conventions",
            "",
            "- **Participant worksheets** (`exercises/exercise-M.N-*.md`) state the scenario, tasks, "
            "time and deliverable — no answers.",
            "- **Answer keys** (`exercises/solution/`) and **lab solutions** (`labN/solution/`) are "
            "for instructors; keep them out of the participant hand-out.",
            "- Every command, value and expected result matches `datasets/training_store/load.js` "
            "on a fresh load. Expected outputs were worked out from the dataset; run the key "
            "examples once in mongosh before class.",
            "- Never type a real password into a slide, worksheet, URI or chat: let `mongosh` prompt, "
            "or use `<password>` placeholders.",
            ""]
    return "\n".join(out)


def main() -> None:
    (LABS / "EXERCISES-INDEX.md").write_text(exercises_index(), encoding="utf-8")
    (LABS / "LABS-INDEX.md").write_text(labs_index(), encoding="utf-8")
    (LABS / "README.md").write_text(readme(), encoding="utf-8")
    print(f"Wrote labs/EXERCISES-INDEX.md ({len(exercises())} exercises), labs/LABS-INDEX.md "
          f"({len(labs())} labs) and labs/README.md")


if __name__ == "__main__":
    main()
