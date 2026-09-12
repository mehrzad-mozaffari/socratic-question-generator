from pathlib import Path
from typing import Any, Dict
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path = ROOT / "config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(path_value: str | Path, root: Path = ROOT) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else root / path


def ensure_project_dirs(cfg: Dict[str, Any]) -> None:
    for value in cfg.get("paths", {}).values():
        p = resolve_path(value)
        # If the configured path has a file suffix, create its parent.
        target = p.parent if p.suffix else p
        target.mkdir(parents=True, exist_ok=True)
