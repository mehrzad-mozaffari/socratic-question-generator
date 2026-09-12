from pathlib import Path
import json
import re
import pandas as pd

TAG_NAMES = ["problem", "bug_code", "bug_desc", "bug_fixes", "unit_tests", "stu_desc", "dialogue"]


def extract_tagged_section(text: str, tag: str) -> str:
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def parse_simple_dialogue_sections(text: str):
    sections = {
        "problem": extract_tagged_section(text, "problem"),
        "bug_code": extract_tagged_section(text, "bug_code"),
        "bug_desc": extract_tagged_section(text, "bug_desc"),
        "bug_fixes": extract_tagged_section(text, "bug_fixes"),
    }
    dialogue_text = extract_tagged_section(text, "dialogue")
    rows = []
    for line in dialogue_text.splitlines():
        line = line.strip()
        if line.startswith("User:"):
            rows.append({"speaker": "User", "utterance": line[len("User:"):].strip()})
        elif line.startswith("Assistant:"):
            rows.append({"speaker": "Assistant", "utterance": line[len("Assistant:"):].strip()})
    sections["dialogue"] = rows
    return sections, pd.DataFrame(rows)


def batch_parse_simple(input_folder: Path, output_folder: Path) -> int:
    output_folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(input_folder.glob("*.txt")):
        sections, dialogue_df = parse_simple_dialogue_sections(
            path.read_text(encoding="utf-8", errors="replace")
        )
        base = path.stem
        dialogue_df.to_csv(output_folder / f"{base}_dialogue.csv", index=False)
        (output_folder / f"{base}_full.json").write_text(
            json.dumps(sections, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        count += 1
    return count


def parse_dialogue(dlg_text: str):
    turns = []
    current = None
    in_code = False
    code_lines = []

    def finalize_current():
        nonlocal current, code_lines
        if current is None:
            return
        content = "\n".join(current["content_lines"]).strip()
        code = "\n\n".join(b.strip() for b in current["code_blocks"] if b.strip()) or None
        turns.append({
            "turn": len(turns) + 1,
            "role": current["role"],
            "content": content,
            "code": code,
            "alternatives": {f"alt{i+1}": a for i, a in enumerate(current["alternatives"])},
        })
        current = None
        code_lines = []

    for raw_line in dlg_text.splitlines():
        line = raw_line.rstrip("\n")
        if in_code:
            if line.strip().lower().startswith("</code>"):
                in_code = False
                if current is not None:
                    current["code_blocks"].append("\n".join(code_lines))
                code_lines = []
            else:
                code_lines.append(line)
            continue

        if line.startswith("User:") or line.startswith("Assistant:"):
            finalize_current()
            role = "User" if line.startswith("User:") else "Assistant"
            text = line.split(":", 1)[1].strip()
            current = {
                "role": role,
                "content_lines": [text] if text else [],
                "alternatives": [],
                "code_blocks": [],
            }
            continue

        if line.strip().lower().startswith("<code>"):
            in_code = True
            code_lines = []
            continue

        if line.strip().lower().startswith("<alt>"):
            alt_text = line.split(">", 1)[1].strip()
            if current is not None and alt_text:
                current["alternatives"].append(alt_text)
            continue

        if current is not None and line.strip():
            current["content_lines"].append(line.strip())

    finalize_current()
    return turns


def file_to_record(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    record = {tag: extract_tagged_section(text, tag) for tag in TAG_NAMES}
    record["dialogue"] = parse_dialogue(record["dialogue"]) if record["dialogue"] else []
    record["_source"] = path.name
    return record


def convert_folder(input_dir: Path, outdir: Path, combined_path: Path,
                   pattern="*.txt", recurse=True) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    candidates = sorted(input_dir.rglob(pattern) if recurse else input_dir.glob(pattern))
    if not candidates:
        print(f"No files found in {input_dir} matching {pattern}")
        return 0

    count = 0
    with combined_path.open("w", encoding="utf-8") as fout:
        for path in candidates:
            try:
                record = file_to_record(path)
                per_file = outdir / f"{path.stem}.jsonl"
                per_file.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
                print(f"OK: {path.relative_to(input_dir)} -> {per_file.name}")
            except Exception as exc:
                print(f"ERROR parsing {path}: {exc}")
    print(f"Done. Wrote {count} records to {combined_path}")
    return count
