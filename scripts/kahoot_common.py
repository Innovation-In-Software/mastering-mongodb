"""Shared Kahoot Excel helpers."""

from __future__ import annotations

import hashlib
import random
from pathlib import Path

from openpyxl import Workbook

# Official Kahoot spreadsheet import limits (create.kahoot.it).
QUESTION_MAX_CHARS = 95
ANSWER_MAX_CHARS = 60
# Visible length gap that still lets players “pick the longest.”
# 0 = all four options the same length (no length-tell).
MAX_ANSWER_LEN_SPREAD = 0


def balance_correct_positions(
    questions: list[dict],
    *,
    seed: int | str | None = None,
) -> list[dict]:
    """Shuffle answer order per question so the correct slot is not fixed.

    Authored banks often place the right answer in the same slot. Each question
    gets an independent Fisher–Yates shuffle of its four options; the Correct
    index is updated to match. Shuffle is seeded from the question text (and
    optional module seed) so regenerations stay stable without a permanent
    1→2→3→4 pattern across the quiz.
    """
    balanced: list[dict] = []
    for q in questions:
        answers = list(q["answers"])
        if len(answers) != 4:
            raise ValueError(f"Expected 4 answers for: {q['question']}")
        old_correct = int(q["correct"])
        if old_correct not in (1, 2, 3, 4):
            raise ValueError(f"Correct must be 1-4 for: {q['question']}")

        material = f"{seed or ''}|{q['question']}"
        digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
        rng = random.Random(int(digest[:16], 16))

        order = [0, 1, 2, 3]
        rng.shuffle(order)
        new_answers = [answers[i] for i in order]
        new_correct = order.index(old_correct - 1) + 1

        balanced.append(
            {
                "question": q["question"],
                "answers": new_answers,
                "correct": new_correct,
            }
        )
    return balanced


def write_kahoot_xlsx(path: Path, questions: list[dict], time_seconds: int = 30) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Kahoot"
    ws.append(["Question", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Time", "Correct"])
    for q in questions:
        answers = q["answers"]
        if len(answers) != 4:
            raise ValueError(f"Expected 4 answers for: {q['question']}")
        correct = int(q["correct"])
        if correct not in (1, 2, 3, 4):
            raise ValueError(f"Correct must be 1-4 for: {q['question']}")
        ws.append(
            [
                q["question"],
                answers[0],
                answers[1],
                answers[2],
                answers[3],
                time_seconds,
                correct,
            ]
        )
    wb.save(path)


def answer_lengths(question: dict) -> list[int]:
    return [len(a) for a in question["answers"]]


def is_uniquely_longest_correct(question: dict) -> bool:
    answers = question["answers"]
    correct = int(question["correct"]) - 1
    lengths = [len(a) for a in answers]
    longest = max(lengths)
    if lengths.count(longest) != 1:
        return False
    return lengths[correct] == longest


def question_length_spread(question: dict) -> int:
    lengths = answer_lengths(question)
    return max(lengths) - min(lengths)


def validate_question(question: dict) -> list[str]:
    """Return human-readable problems for one item (empty = ok)."""
    problems: list[str] = []
    text = str(question.get("question") or "")
    answers = question.get("answers")
    if not text.strip():
        problems.append("empty question")
    if len(text) > QUESTION_MAX_CHARS:
        problems.append(f"question is {len(text)} chars (max {QUESTION_MAX_CHARS})")
    if not isinstance(answers, list) or len(answers) != 4:
        problems.append("expected exactly 4 answers")
        return problems
    try:
        correct = int(question["correct"])
    except (KeyError, TypeError, ValueError):
        problems.append("correct must be 1-4")
        return problems
    if correct not in (1, 2, 3, 4):
        problems.append(f"correct={correct} is not 1-4")
    for i, ans in enumerate(answers, 1):
        if not isinstance(ans, str) or not ans.strip():
            problems.append(f"answer {i} is empty")
            continue
        if len(ans) > ANSWER_MAX_CHARS:
            problems.append(f"answer {i} is {len(ans)} chars (max {ANSWER_MAX_CHARS}): {ans!r}")
    spread = question_length_spread(question)
    if spread > MAX_ANSWER_LEN_SPREAD:
        problems.append(
            f"answer length spread {spread} > {MAX_ANSWER_LEN_SPREAD} "
            f"(lens={answer_lengths(question)})"
        )
    return problems


def length_tell_stats(questions: list[dict]) -> dict[str, int | float]:
    n = len(questions)
    unique_longest_correct = sum(1 for q in questions if is_uniquely_longest_correct(q))
    return {
        "n": n,
        "unique_longest_correct": unique_longest_correct,
        "unique_longest_correct_pct": (100.0 * unique_longest_correct / n) if n else 0.0,
    }
