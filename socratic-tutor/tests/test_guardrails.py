from socratic_tutor.tutor.guardrails import enforce_socratic_question


def test_guardrails_add_question_mark():
    assert enforce_socratic_question("What value do you get") == "What value do you get?"


def test_guardrails_blocks_solution_language():
    result = enforce_socratic_question("Here is the fix: return x")
    assert "Before changing code" in result
