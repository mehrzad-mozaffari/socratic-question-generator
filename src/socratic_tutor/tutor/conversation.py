import json
import time
from pathlib import Path


def gradio_history_to_turns(chat_history, current_user=None):
    history = []
    for item in chat_history or []:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content", "")
            if role in {"user", "assistant"}:
                history.append({"role": role.capitalize(), "content": content})
        else:
            user, assistant = item
            if user:
                history.append({"role": "User", "content": user})
            if assistant:
                history.append({"role": "Assistant", "content": assistant})
    if current_user:
        history.append({"role": "User", "content": current_user})
    return history


def save_transcript(chat_history, problem, notes, log_dir: Path):
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    record = {
        "timestamp": timestamp,
        "problem": problem,
        "stu_notes": notes,
        "turns": [{"user": u, "assistant": a} for u, a in chat_history],
    }
    path = log_dir / f"chat_{timestamp}.jsonl"
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
