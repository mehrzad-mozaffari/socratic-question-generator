import json
from pathlib import Path
import random

SYSTEM_PROMPT = (
    "You are a patient, Socratic coding tutor. Ask ONE short, targeted question "
    "per turn that helps the student discover the issue themselves. Do not give solutions."
)


def extract_commentary_examples(dialogues, dialogue_id, window=2):
    examples = []
    for i in range(window, len(dialogues)):
        turn = dialogues[i]
        if turn["speaker"] != "User":
            continue
        context = dialogues[i - window:i + 1]
        input_text = "\n".join(f"[{t['speaker']}]: {t['utterance']}" for t in context)
        examples.append({"dialogue_id": dialogue_id, "input": input_text, "output": ""})
    return examples


def turn_text(role, content, code=None):
    if code:
        return f"{role}: {content}\n<code>\n{code}\n</code>"
    return f"{role}: {content}"


def build_examples(records, use_alts=True, max_hist_tokens=None):
    _ = max_hist_tokens
    examples = []
    for record in records:
        ctx_parts = []
        if record.get("problem"):
            ctx_parts.append(f"Problem: {record['problem']}")
        if record.get("stu_desc"):
            ctx_parts.append(f"Student notes: {record['stu_desc']}")
        ctx = "\n".join(ctx_parts).strip()
        history = []
        for turn in record.get("dialogue", []):
            role = turn["role"]
            content = turn["content"]
            code = turn.get("code") or None
            if role == "Assistant":
                prompt = (
                    f"### System\n{SYSTEM_PROMPT}\n\n"
                    f"### Context\n{ctx}\n\n"
                    f"### Dialogue so far\n" + "\n".join(history) + "\n\n"
                    f"### Assistant\n"
                )
                examples.append({"text": prompt + content.strip()})
                if use_alts and turn.get("alternatives"):
                    for key in sorted(turn["alternatives"]):
                        alt = turn["alternatives"][key].strip()
                        if alt:
                            examples.append({"text": prompt + alt})
                history.append(turn_text("Assistant", content, code))
            else:
                history.append(turn_text("User", content, code))
    return examples


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build_train_eval_datasets(path: Path, train_split=0.9, use_alts=True, seed=42):
    from datasets import Dataset
    records = load_jsonl(path)
    examples = build_examples(records, use_alts=use_alts)
    random.Random(seed).shuffle(examples)
    split = int(train_split * len(examples))
    train = examples[:split]
    eval_data = examples[split:] if split < len(examples) else examples[:1]
    return Dataset.from_list(train), Dataset.from_list(eval_data), examples
