"""Load course.config.yaml from the repository root."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError("PyYAML is required: pip install pyyaml") from exc

_REPO = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO / "course.config.yaml"


@lru_cache(maxsize=1)
def load_config(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or _CONFIG_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Course config not found: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid course config in {path}")
    return data


def repo_root(config_path: Path | None = None) -> Path:
    if config_path is not None:
        return config_path.resolve().parent
    return _REPO


def course_info(config_path: Path | None = None) -> dict[str, Any]:
    return load_config(config_path)["course"]


def path(key: str, config_path: Path | None = None) -> Path:
    root = repo_root(config_path)
    rel = load_config(config_path)["paths"][key]
    return root / rel


def deck_md(config_path: Path | None = None) -> Path:
    return path("deck_md", config_path)


def deck_html(config_path: Path | None = None) -> Path:
    return path("deck_html", config_path)


def speaker_notes(config_path: Path | None = None) -> Path:
    return path("speaker_notes", config_path)


def lab_guides_dir(config_path: Path | None = None) -> Path:
    return path("lab_guides", config_path)


def assets_dir(config_path: Path | None = None) -> Path:
    return path("assets", config_path)


def module_names(config_path: Path | None = None) -> dict[int, str]:
    modules = load_config(config_path).get("modules", [])
    return {int(m["id"]): str(m["title"]) for m in modules}


def modules(config_path: Path | None = None) -> list[dict[str, Any]]:
    return list(load_config(config_path).get("modules", []))
