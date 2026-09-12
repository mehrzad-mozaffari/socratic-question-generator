import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, ensure_project_dirs, resolve_path
from socratic_tutor.data.parser import batch_parse_simple, convert_folder

cfg = load_config()
ensure_project_dirs(cfg)
raw = resolve_path(cfg["paths"]["raw_dialogues"])
legacy_out = resolve_path(cfg["paths"]["legacy_parsed"])
parsed = resolve_path(cfg["paths"]["parsed_jsonl"])
combined = resolve_path(cfg["paths"]["training_dataset"])

print("[1/2] Legacy CSV/full-JSON preprocessing")
print(f"Input: {raw}")
print(f"Output: {legacy_out}")
print(f"Processed files: {batch_parse_simple(raw, legacy_out)}")

print("[2/2] Normalized JSONL conversion")
convert_folder(raw, parsed, combined)
