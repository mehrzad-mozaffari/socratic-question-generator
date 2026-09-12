def compare_tests(user_tests: str, reference_tests: str) -> float:
    """Percentage of non-empty reference test lines present in user tests."""
    user_lines = {line.strip() for line in user_tests.strip().splitlines() if line.strip()}
    ref_lines = [line.strip() for line in reference_tests.strip().splitlines() if line.strip()]
    if not ref_lines:
        return 0.0
    match_count = sum(1 for line in ref_lines if line in user_lines)
    return match_count / len(ref_lines) * 100
