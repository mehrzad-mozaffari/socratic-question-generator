from socratic_tutor.evaluation.metrics import compare_tests


def test_compare_tests():
    assert compare_tests("assert x == 1", "assert x == 1\nassert y == 2") == 50
