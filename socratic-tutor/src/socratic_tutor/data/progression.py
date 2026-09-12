import json
from pathlib import Path
import pandas as pd


def process_dialogue_progression(dialogue_json: dict, dialogue_id: str) -> pd.DataFrame:
    dialogue = dialogue_json.get("dialogue", [])
    total_turns = len(dialogue)
    records = []
    for i, turn in enumerate(dialogue):
        stage = "Early" if i < total_turns * 0.33 else "Mid" if i < total_turns * 0.66 else "Late"
        records.append({
            "dialogue_id": dialogue_id,
            "turn_number": i + 1,
            "speaker": turn.get("role", turn.get("speaker", "")),
            "utterance": turn.get("content", turn.get("utterance", "")),
            "turn_stage": stage,
        })
    return pd.DataFrame(records)


def build_progression(input_dir: Path, output_path: Path) -> pd.DataFrame:
    """Read either normalized JSONL records or legacy *_full.json records."""
    frames = []
    for path in sorted(input_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    frames.append(process_dialogue_progression(data, data.get("_source", path.stem)))
    for path in sorted(input_dir.glob("*_full.json")):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        frames.append(process_dialogue_progression(data, path.stem.replace("_full", "")))
    columns = ["dialogue_id", "turn_number", "speaker", "utterance", "turn_stage"]
    result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=columns)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return result
