"""Module 5 lab guides are maintained as Markdown under slide-exercises/module-05/.

Do not regenerate them from this file — an earlier f-string version doubled
JavaScript braces. Edit the .md files directly.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "slide-exercises" / "module-05"


def main() -> None:
    guides = sorted(p.name for p in OUT.glob("*.md"))
    print(f"{len(guides)} lab guides in {OUT.relative_to(OUT.parent.parent)}:")
    for name in guides:
        print(f"  {name}")


if __name__ == "__main__":
    main()
