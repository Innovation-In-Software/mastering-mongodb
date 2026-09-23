#!/usr/bin/env python3
"""Regenerate Kahoot Excel files from scripts/mongodb_kahoot_questions.py.

Writes kahoot/module_questions.json (shuffled snapshot) and Kahoot_Module_N.xlsx.
Does not create Kahoot quizzes or change share URLs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kahoot_common import (  # noqa: E402
    QUESTION_MAX_CHARS,
    ANSWER_MAX_CHARS,
    balance_correct_positions,
    validate_question,
    write_kahoot_xlsx,
)
from mongodb_kahoot_questions import BANK, as_questions  # noqa: E402

REPO = SCRIPTS.parent
KAHOOT = REPO / "kahoot"
EXPECTED = 15
MODULES = range(1, 9)


def regenerate(*, shuffle: bool) -> list[str]:
    written: list[str] = []
    snapshot: dict[str, list[dict]] = {}
    for module in MODULES:
        if module not in BANK:
            raise ValueError(f"Missing module {module} in mongodb_kahoot_questions.BANK")
        questions = as_questions(module)
        if len(questions) != EXPECTED:
            raise ValueError(
                f"module {module}: expected {EXPECTED} questions, found {len(questions)}"
            )
        problems = [p for q in questions for p in validate_question(q)]
        if problems:
            preview = "; ".join(problems[:8])
            raise ValueError(f"module {module}: {preview}")
        if shuffle:
            questions = balance_correct_positions(questions, seed=module)
        out = KAHOOT / f"Kahoot_Module_{module}.xlsx"
        write_kahoot_xlsx(out, questions)
        snapshot[str(module)] = questions
        written.append(str(out.relative_to(REPO)))

    json_path = KAHOOT / "module_questions.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    written.append(str(json_path.relative_to(REPO)))
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Keep authored answer order (default shuffles with a stable seed)",
    )
    args = parser.parse_args()
    written = regenerate(shuffle=not args.no_shuffle)
    print(
        f"wrote {len(written)} files "
        f"(question {QUESTION_MAX_CHARS}c / answer {ANSWER_MAX_CHARS}c)"
    )
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
