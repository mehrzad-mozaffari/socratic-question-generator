import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, ensure_project_dirs
from socratic_tutor.training.train import train

cfg = load_config()
ensure_project_dirs(cfg)
train(cfg)
