#!/usr/bin/env python3
"""Fail if Kahoot banks telegraph the correct answer by length."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kahoot_common import (  # noqa: E402
    length_tell_stats,
    question_length_spread,
    validate_question,
)
from mongodb_kahoot_questions import BANK, as_questions  # noqa: E402

REPO = SCRIPTS.parent
MAX_UNIQUE_LONGEST_CORRECT_PCT = 0.0
MAX_ANSWER_SPREAD = 0


def load_json_bank() -> dict[str, list[dict]] | None:
    path = REPO / "kahoot" / "module_questions.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-json",
        action="store_true",
        help="Validate kahoot/module_questions.json instead of the Python bank",
    )
    args = parser.parse_args()

    errors: list[str] = []
    all_qs: list[dict] = []

    if args.from_json:
        bank = load_json_bank()
        if bank is None:
            print("kahoot/module_questions.json not found", file=sys.stderr)
            return 1
        modules = sorted(bank, key=lambda k: int(k))
        getter = lambda m: bank[m]
    else:
        modules = sorted(BANK)
        getter = lambda m: as_questions(int(m))

    print("== Mastering MongoDB Kahoot ==")
    for module in modules:
        questions = getter(module)
        all_qs.extend(questions)
        for qi, q in enumerate(questions, 1):
            for problem in validate_question(q):
                errors.append(f"M{module} Q{qi}: {problem}")
                print(f"  FAIL M{module} Q{qi}: {problem}")
        stats = length_tell_stats(questions)
        pct = stats["unique_longest_correct_pct"]
        max_spread = max((question_length_spread(q) for q in questions), default=0)
        flag = ""
        if pct > MAX_UNIQUE_LONGEST_CORRECT_PCT:
            flag = "  <-- length tell"
            errors.append(
                f"M{module}: uniquely-longest-correct "
                f"{pct:.0f}% > {MAX_UNIQUE_LONGEST_CORRECT_PCT:.0f}%"
            )
        if max_spread > MAX_ANSWER_SPREAD:
            errors.append(
                f"M{module}: answer length spread {max_spread} > {MAX_ANSWER_SPREAD}"
            )
            flag = (flag + "  <-- unequal answers").strip()
        print(
            f"  M{module}: {stats['n']}q  unique-longest-correct="
            f"{stats['unique_longest_correct']}/{stats['n']} ({pct:.0f}%)  "
            f"max-spread={max_spread}{flag}"
        )

    overall = length_tell_stats(all_qs)
    print(
        f"  overall uniquely-longest-correct "
        f"{overall['unique_longest_correct']}/{overall['n']} "
        f"({overall['unique_longest_correct_pct']:.1f}%)"
    )

    if errors:
        print(f"\n{len(errors)} check(s) failed.", file=sys.stderr)
        return 1
    print("\nAll length-tell checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
