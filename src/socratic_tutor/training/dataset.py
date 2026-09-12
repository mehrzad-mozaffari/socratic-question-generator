from pathlib import Path
from socratic_tutor.data.dataset_builder import build_train_eval_datasets


def load_training_datasets(path: str | Path, train_split=0.9, use_alts=True, seed=42):
    return build_train_eval_datasets(Path(path), train_split=train_split, use_alts=use_alts, seed=seed)
