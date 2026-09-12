from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path = ROOT / "config.yaml") -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(path_value: str | Path, root: Path = ROOT) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else root / path


def ensure_project_dirs(cfg: dict[str, Any]) -> None:
    """Create configured directories and parents for configured files."""
    for value in cfg.get("paths", {}).values():
        p = resolve_path(value)
        target = p.parent if p.suffix else p
        target.mkdir(parents=True, exist_ok=True)
