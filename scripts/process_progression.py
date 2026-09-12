import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path
from socratic_tutor.data.progression import build_progression

cfg = load_config()
input_dir = resolve_path(cfg["paths"]["progression_input"])
output = resolve_path(cfg["paths"]["progression_csv"])
df = build_progression(input_dir, output)
print(f"Saved {len(df)} progression rows to {output}")
