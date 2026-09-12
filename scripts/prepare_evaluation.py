import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path
from socratic_tutor.evaluation.log_processing import (
    combine_json_files, load_jsonl, save_jsonl, assign_unit_tests, assign_titles, reorder_logs
)
from socratic_tutor.evaluation.reference_unit_tests import unit_tests

cfg = load_config()
logs_dir = resolve_path(cfg["paths"]["chat_logs"])
combined = resolve_path(cfg["paths"]["combined_chat_logs"])
with_tests = resolve_path(cfg["paths"]["chat_logs_with_tests"])
with_titles = resolve_path(cfg["paths"]["chat_logs_with_tests_titles"])
ordered = resolve_path(cfg["paths"]["evaluated_chat_logs"])

count = combine_json_files(logs_dir, combined)
logs = load_jsonl(combined)
save_jsonl(assign_unit_tests(logs, unit_tests), with_tests)
logs = load_jsonl(with_tests)
save_jsonl(assign_titles(logs), with_titles)
logs = load_jsonl(with_titles)
save_jsonl(reorder_logs(logs), ordered)
print(f"Combined {count} chat objects")
print(f"Prepared evaluation logs: {ordered}")
