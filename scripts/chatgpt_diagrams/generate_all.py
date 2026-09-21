#!/usr/bin/env python3
"""Run remaining MongoDB ChatGPT diagram generators sequentially.

    python scripts/chatgpt_diagrams/generate_all.py --dry-run
    python scripts/chatgpt_diagrams/generate_all.py
    python scripts/chatgpt_diagrams/generate_all.py --module 3
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEN = HERE / "generate_module.py"


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> int:
    extra = sys.argv[1:]
    modules = list(range(1, 9))
    if "--module" in extra:
        i = extra.index("--module")
        modules = [int(extra[i + 1])]
        extra = extra[:i] + extra[i + 2 :]

    overall = 0
    for module in modules:
        log(f"===== START module {module:02d} =====")
        result = subprocess.run(
            [sys.executable, str(GEN), "--module", str(module), *extra],
            cwd=str(HERE.parents[1]),
        )
        rc = result.returncode
        log(f"===== END module {module:02d} rc={rc} =====")
        if rc == 3:
            log("Image quota exhausted. Stopping remaining modules.")
            return 3
        if rc != 0:
            overall = rc
            log(f"Continuing after non-zero rc={rc} (resume-safe).")
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
