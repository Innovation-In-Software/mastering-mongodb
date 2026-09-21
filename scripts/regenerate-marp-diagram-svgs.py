#!/usr/bin/env python3
"""Re-render auto-generated module diagram SVGs using the latest monospace panel renderer."""

from __future__ import annotations

from pathlib import Path

from marp_svg_common import lines_from_monospace_svg, monospace_panel_svg

try:
    from custom_diagram_svgs import CUSTOM_DIAGRAMS
except ImportError:
    CUSTOM_DIAGRAMS = {}


def main() -> int:
    assets = Path(__file__).resolve().parent.parent / "slides" / "assets"
    total = 0

    for rel_path, generator in CUSTOM_DIAGRAMS.items():
        svg_path = assets / Path(*rel_path.split("/"))
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text(generator(), encoding="utf-8")
        print(f"Updated custom {rel_path}")
        total += 1

    for module_dir in sorted(assets.glob("module-*")):
        if module_dir.name in {"module-01", "module-02", "module-03"}:
            continue
        for svg_path in sorted(module_dir.glob("*.svg")):
            rel = f"{module_dir.name}/{svg_path.name}"
            if rel in CUSTOM_DIAGRAMS:
                continue
            original = svg_path.read_text(encoding="utf-8")
            lines = lines_from_monospace_svg(original)
            if not lines:
                continue
            updated = monospace_panel_svg(lines)
            if updated != original:
                svg_path.write_text(updated, encoding="utf-8")
                print(f"Updated {svg_path.relative_to(assets.parent)}")
                total += 1
    print(f"Done. {total} SVG(s) re-rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
