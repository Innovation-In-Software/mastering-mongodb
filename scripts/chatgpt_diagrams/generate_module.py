#!/usr/bin/env python3
"""Generate one module's HD diagrams via ChatGPT + Playwright (MD287 approach).

    python scripts/chatgpt_diagrams/generate_module.py --module 1 --dry-run
    python scripts/chatgpt_diagrams/generate_module.py --module 1
    python scripts/chatgpt_diagrams/generate_module.py --module 1 --max 1
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from catalog import PROMPT, diagrams_for  # noqa: E402
from runner import run  # noqa: E402


def main() -> int:
    # Peek --module before runner argparse so we can build the diagram list.
    module = 1
    argv = sys.argv[1:]
    if "--module" in argv:
        i = argv.index("--module")
        module = int(argv[i + 1])
        del argv[i : i + 2]
        sys.argv = [sys.argv[0], *argv]
    elif argv and argv[0].isdigit():
        module = int(argv[0])
        sys.argv = [sys.argv[0], *argv[1:]]

    nn = f"{module:02d}"
    return run(
        description=f"Generate Module {module} HD diagrams via ChatGPT.",
        out_dir=HERE / "diagrams" / f"module{nn}",
        log_dir=HERE / "diagrams_logs" / f"module{nn}",
        progress_file=HERE / f"diagrams_module{nn}_progress.json",
        results_file=HERE / f"diagrams_module{nn}_results.csv",
        prompt_template=PROMPT,
        diagrams=diagrams_for(module),
    )


if __name__ == "__main__":
    raise SystemExit(main())
