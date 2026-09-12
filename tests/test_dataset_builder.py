from socratic_tutor.data.dataset_builder import build_examples


def test_build_examples_creates_assistant_targets():
    records = [{
        "problem": "Loop bug", "stu_desc": "",
        "dialogue": [
            {"role": "User", "content": "It is wrong", "code": None, "alternatives": {}},
            {"role": "Assistant", "content": "What value do you expect?", "code": None,
             "alternatives": {"alt1": "What should happen?"}},
        ],
    }]
    examples = build_examples(records)
    assert len(examples) == 2
    assert all("### Assistant" in item["text"] for item in examples)
