from pathlib import Path
from socratic_tutor.data.parser import file_to_record, parse_simple_dialogue_sections


def test_parser_handles_dialogue(tmp_path: Path):
    text = """<problem>Find the bug</problem>
<stu_desc>Student is confused</stu_desc>
<dialogue>
User: I tried this.
<code>
print(1)
</code>
Assistant: What does this print?
<alt>What output do you observe?
</dialogue>"""
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")
    record = file_to_record(path)
    assert record["problem"] == "Find the bug"
    assert len(record["dialogue"]) == 2
    assert record["dialogue"][0]["code"].strip() == "print(1)"
    assert record["dialogue"][1]["alternatives"]["alt1"] == "What output do you observe?"


def test_simple_parser_returns_dataframe():
    _, df = parse_simple_dialogue_sections("""<dialogue>
User: hello
Assistant: what happened?
</dialogue>""")
    assert list(df["speaker"]) == ["User", "Assistant"]
