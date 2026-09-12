import json
from pathlib import Path

WRONG_TESTS = "assert 1 == 0\nassert 2 == 3"


def combine_json_files(input_folder: Path, output_jsonl: Path):
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_jsonl.open("w", encoding="utf-8") as out:
        for path in sorted(input_folder.glob("*.json*")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"Failed to parse {path.name}")
                continue
            objects = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
            for obj in objects:
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")
                count += 1
    return count


def assign_titles(logs):
    keywords = [
        "factorial", "gcd", "remove_duplicates", "palindrome", "sum_even", "fibonacci",
        "sum_squares", "has_duplicates", "sum_list", "reverse_words", "reverse_string",
        "is_prime", "max_in_list", "count_vowels", "reverse_list", "fibonacci_sum", "factorial_iter"
    ]
    for log in logs:
        p = log.get("problem", "").lower()
        log["title"] = next((k for k in keywords if k in p), "coding problem")
    return logs


def reorder_logs(logs):
    ordered = []
    for log in logs:
        item = {"timestamp": log.get("timestamp"), "title": log.get("title")}
        item.update({k: v for k, v in log.items() if k not in {"timestamp", "title"}})
        ordered.append(item)
    return ordered
