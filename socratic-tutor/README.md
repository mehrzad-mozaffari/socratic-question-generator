# Socratic Coding Tutor

An LLM-based Socratic debugging tutor that generates one short, targeted question at a time instead of directly revealing programming solutions.

## Project pipeline

```text
Raw dialogue files
      ↓
Data parsing / normalization
      ↓
SFT dataset construction
      ↓
QLoRA fine-tuning (Phi-3-mini)
      ↓
LoRA adapter
      ↓
Socratic Tutor
  ├── prompt construction
  ├── LLM generation
  └── guardrails
      ↓
Gradio chatbot
      ↓
Chat logs
      ↓
Evaluation against reference unit tests
      ↓
CSV + figures
```

## Structure

- `src/socratic_tutor/`: reusable application and research code
- `scripts/`: command-line entry points
- `data/`: raw and processed datasets
- `models/`: local model/LoRA artifacts
- `logs/`: chatbot transcripts
- `results/`: evaluation outputs and figures
- `tests/`: automated tests
- `notebooks/`: exploratory research notebooks

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For GPU training, install the PyTorch build appropriate for your CUDA environment before installing the remaining requirements if necessary.

## Data preprocessing

Put source dialogue `.txt` files under `data/raw/dialogues/` and run:

```bash
python scripts/preprocess_data.py
```

This creates normalized JSONL records and the combined training JSONL according to `config.yaml`.

## Build / inspect the training dataset

```bash
python scripts/build_dataset.py
```

## QLoRA training

```bash
python scripts/train.py
```

The default configuration follows the original notebook: `microsoft/Phi-3-mini-4k-instruct`, 4-bit NF4 quantization, LoRA rank 16, alpha 32, dropout 0.05, two epochs, batch size 2, and gradient accumulation 8.

## Run the tutor

After training:

```bash
python scripts/run_tutor.py
```

The application loads the base model plus the LoRA adapter and starts the Gradio interface.

## Evaluation

Place your processed chat-log dataset at the configured evaluation path, then run:

```bash
python scripts/evaluate.py
python scripts/visualize.py
```

## Important design principle

The tutor should not directly reveal the student's bug or provide the exact code fix. The guardrail layer converts unsafe solution-like generations into a diagnostic Socratic question.

## Research note

The original notebook contained data preprocessing, progression analysis, training, inference, chatbot UI, chat-log enrichment, reference tests, evaluation, and visualization in one file. This repository separates those concerns while preserving the original pipeline and model choices.
