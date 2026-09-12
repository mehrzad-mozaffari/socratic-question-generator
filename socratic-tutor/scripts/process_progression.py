import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path
from socratic_tutor.data.progression import build_progression

cfg = load_config()
# Progression requires per-dialogue JSON files. If you want this exact legacy
# analysis, export them alongside the normalized JSONL records first.
input_dir = resolve_path(cfg["paths"]["parsed_jsonl"])
output = resolve_path(cfg["paths"]["progression_csv"])
print("Progression analysis expects *_full.json files in the configured input directory.")
print(f"Configured input: {input_dir}")
print(f"Output: {output}")
build_progression(input_dir, output)
