from socratic_tutor.evaluation.metrics import compare_tests
from socratic_tutor.evaluation.log_processing import assign_titles


def test_compare_tests():
    assert compare_tests("assert x == 1", """assert x == 1
assert y == 2""") == 50


def test_assign_titles():
    logs = assign_titles([{"problem": "Write fibonacci(n:int)"}])
    assert logs[0]["title"] == "fibonacci"
