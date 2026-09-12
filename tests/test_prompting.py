from socratic_tutor.model.prompting import build_inference_prompt


def test_prompt_contains_context_and_code():
    prompt = build_inference_prompt(
        [{"role": "User", "content": "It fails", "code": "print(1)"}],
        problem="Debug this",
        notes="Check the loop",
    )
    assert "Problem: Debug this" in prompt
    assert """<code>
print(1)
</code>""" in prompt
    assert prompt.endswith("""### Assistant
""")
