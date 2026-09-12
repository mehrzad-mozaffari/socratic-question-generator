import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path
from socratic_tutor.data.dataset_builder import build_train_eval_datasets

cfg = load_config()
train, evaluation, examples = build_train_eval_datasets(
    resolve_path(cfg["paths"]["training_dataset"]),
    train_split=cfg["training"]["train_split"],
    use_alts=cfg["training"]["use_alternatives"],
)
print(f"Examples: {len(examples)} | Train: {len(train)} | Eval: {len(evaluation)}")
if examples:
    print(examples[0]["text"][:1000])
