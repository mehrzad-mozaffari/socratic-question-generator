import json
from pathlib import Path

WRONG_TESTS = "assert 1 == 0\nassert 2 == 3"


def load_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")
    return records


def save_jsonl(records, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


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
            if not objects:
                print(f"Skipping unknown JSON structure in {path.name}")
            for obj in objects:
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")
                count += 1
    return count


def assign_unit_tests(logs, correct_tests):
    for log in logs:
        turns = log.get("turns", [])
        last_user_msg = turns[-1].get("user", "").lower() if turns else ""
        if "give up" in last_user_msg or "too confusing" in last_user_msg or "recursion seems too hard" in last_user_msg:
            log["unit_tests"] = WRONG_TESTS
            continue
        p = log.get("problem", "").lower()
        if "factorial_iter" in p or "factorial(n:int)" in p:
            log["unit_tests"] = correct_tests["factorial"]
        elif "gcd" in p:
            log["unit_tests"] = correct_tests["gcd"]
        elif "remove_duplicates" in p:
            log["unit_tests"] = correct_tests["remove_duplicates"]
        elif "palindrome" in p:
            log["unit_tests"] = correct_tests["palindrome"]
        elif "sum_even" in p:
            log["unit_tests"] = correct_tests["sum_even"]
        elif "fibonacci" in p and "sum" not in p:
            log["unit_tests"] = correct_tests["fibonacci"]
        elif "factorial_iter" in p:
            log["unit_tests"] = correct_tests["factorial_iter"]
        elif "sum_squares" in p:
            log["unit_tests"] = correct_tests["sum_squares"]
        elif "sum_list" in p:
            log["unit_tests"] = correct_tests["sum_list"]
        elif "reverse_words" in p:
            log["unit_tests"] = correct_tests["reverse_words"]
        elif "has_duplicates" in p:
            log["unit_tests"] = correct_tests["has_duplicates"]
        elif "max_in_list" in p:
            log["unit_tests"] = correct_tests["max_in_list"]
        elif "count_vowels" in p:
            log["unit_tests"] = correct_tests["count_vowels"]
        elif "reverse_list" in p:
            log["unit_tests"] = correct_tests["reverse_list"]
        elif "reverse_string" in p:
            log["unit_tests"] = correct_tests["reverse_string"]
        elif "fibonacci_sum" in p:
            log["unit_tests"] = correct_tests["fibonacci_sum"]
        else:
            log["unit_tests"] = WRONG_TESTS
    return logs


def assign_titles(logs):
    checks = [
        ("factorial(n:int)", "factorial"), ("gcd", "gcd"),
        ("remove_duplicates", "remove_duplicates"), ("palindrome", "palindrome"),
        ("sum_even", "sum_even"), ("fibonacci(n:int)", "fibonacci"),
        ("sum_squares", "sum_squares"), ("has_duplicates", "has_duplicates"),
        ("sum_list", "sum_list"), ("reverse_words", "reverse_words"),
        ("reverse_string", "reverse_string"), ("is_prime", "is_prime"),
        ("max_in_list", "max_in_list"), ("count_vowels", "count_vowels"),
        ("reverse_list", "reverse_list"), ("fibonacci_sum", "fibonacci_sum"),
        ("factorial_iter", "factorial_iter"),
    ]
    for log in logs:
        p = log.get("problem", "").lower()
        log["title"] = next((title for keyword, title in checks if keyword in p), "coding problem")
    return logs


def reorder_logs(logs):
    ordered = []
    for log in logs:
        item = {"timestamp": log.get("timestamp"), "title": log.get("title")}
        item.update({k: v for k, v in log.items() if k not in {"timestamp", "title"}})
        ordered.append(item)
    return ordered
