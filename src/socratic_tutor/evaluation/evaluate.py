from pathlib import Path
import json
import pandas as pd
from .metrics import compare_tests


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def evaluate_logs(logs_path: Path, reference_tests: dict) -> pd.DataFrame:
    rows = []
    for log in load_jsonl(logs_path):
        title = log.get("title", "").lower()
        ref = reference_tests.get(title)
        if ref is None:
            print(f"No reference tests for: {title}")
            continue
        user_tests = log.get("unit_tests", "").strip()
        rows.append({
            "timestamp": log.get("timestamp"),
            "title": log.get("title"),
            "unit_test_pass_rate": compare_tests(user_tests, ref),
            "user_test_lines": len([x for x in user_tests.splitlines() if x.strip()]),
            "reference_test_lines": len([x for x in ref.splitlines() if x.strip()]),
        })
    return pd.DataFrame(rows)


def save_evaluation(df: pd.DataFrame, output_csv: Path):
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
