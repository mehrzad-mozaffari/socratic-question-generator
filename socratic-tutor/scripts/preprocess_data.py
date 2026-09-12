import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, ensure_project_dirs, resolve_path
from socratic_tutor.data.parser import convert_folder

cfg = load_config()
ensure_project_dirs(cfg)
input_dir = resolve_path(cfg["paths"]["raw_dialogues"])
out_dir = resolve_path(cfg["paths"]["parsed_jsonl"])
combined = resolve_path(cfg["paths"]["training_dataset"])
convert_folder(input_dir, out_dir, combined)
