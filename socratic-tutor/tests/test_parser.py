from pathlib import Path
from socratic_tutor.data.parser import file_to_record


def test_parser_handles_dialogue(tmp_path: Path):
    text = """<problem>Find the bug</problem>\n<stu_desc>Student is confused</stu_desc>\n<dialogue>\nUser: I tried this.\n<code>\nprint(1)\n</code>\nAssistant: What does this print?\n<alt>What output do you observe?</alt>\n</dialogue>"""
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")
    record = file_to_record(path)
    assert record["problem"] == "Find the bug"
    assert len(record["dialogue"]) == 2
    assert record["dialogue"][0]["code"].strip() == "print(1)"
    assert record["dialogue"][1]["alternatives"]["alt1"] == "What output do you observe?"
