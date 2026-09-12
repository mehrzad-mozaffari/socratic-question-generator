from socratic_tutor.evaluation.metrics import compare_tests


def test_compare_tests_full_match():
    reference = "assert a == 1\nassert b == 2"
    assert compare_tests(reference, reference) == 100.0


def test_compare_tests_partial_match():
    reference = "assert a == 1\nassert b == 2"
    user = "assert a == 1"
    assert compare_tests(user, reference) == 50.0
