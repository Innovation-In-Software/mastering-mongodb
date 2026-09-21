"""Optional custom SVG generators registered for regenerate-marp-diagram-svgs.py."""
from __future__ import annotations

from module01_diagrams import DIAGRAMS as MODULE01_DIAGRAMS
from module02_diagrams import DIAGRAMS as MODULE02_DIAGRAMS
from module03_diagrams import DIAGRAMS as MODULE03_DIAGRAMS
from module04_diagrams import DIAGRAMS as MODULE04_DIAGRAMS
from module05_diagrams import DIAGRAMS as MODULE05_DIAGRAMS

CUSTOM_DIAGRAMS = {
    **{f"module-01/{name}": fn for name, fn in MODULE01_DIAGRAMS.items()},
    **{f"module-02/{name}": fn for name, fn in MODULE02_DIAGRAMS.items()},
    **{f"module-03/{name}": fn for name, fn in MODULE03_DIAGRAMS.items()},
    **{f"module-04/{name}": fn for name, fn in MODULE04_DIAGRAMS.items()},
    **{f"module-05/{name}": fn for name, fn in MODULE05_DIAGRAMS.items()},
}
