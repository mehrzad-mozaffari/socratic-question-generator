import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path
from socratic_tutor.evaluation.evaluate import evaluate_logs, save_evaluation
from socratic_tutor.evaluation.reference_unit_tests import unit_tests

cfg = load_config()
logs = resolve_path(cfg["paths"]["evaluated_chat_logs"])
out = resolve_path(cfg["paths"]["evaluation_csv"])
df = evaluate_logs(logs, unit_tests)
save_evaluation(df, out)
print(f"Evaluation complete: {out}")
print(df.head())
