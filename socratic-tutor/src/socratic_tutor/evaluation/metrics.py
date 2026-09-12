def compare_tests(user_tests: str, reference_tests: str) -> float:
    user_lines = {line.strip() for line in user_tests.strip().splitlines() if line.strip()}
    ref_lines = [line.strip() for line in reference_tests.strip().splitlines() if line.strip()]
    if not ref_lines:
        return 0.0
    matches = sum(1 for line in ref_lines if line in user_lines)
    return matches / len(ref_lines) * 100
