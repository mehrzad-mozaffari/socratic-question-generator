# Socratic Coding Tutor

A research-oriented LLM-based Socratic debugging tutor. 
The main pipeline: 
dialogue parsing -> progression analysis -> SFT dataset construction -> QLoRA training -> inference -> Gradio tutoring -> chat-log enrichment -> reference-test evaluation -> visualization

## Architecture

```text
Raw TXT dialogues
   │
   ├── legacy parser ──> CSV + *_full.json
   │
   └── normalized parser ──> per-file JSONL + combined JSONL
                                      │
                                      ▼
                              SFT dataset builder
                                      │
                                      ▼
                              QLoRA / Phi-3-mini
                                      │
                                      ▼
                             Base model + LoRA
                                      │
                                      ▼
                         SocraticTutor orchestration
                         ┌──────────┼──────────┐
                         ▼          ▼          ▼
                      Prompt    Generate    Guardrails
                                      │
                                      ▼
                                 Gradio UI
                                      │
                                      ▼
                                  Chat logs
                                      │
                         prepare_evaluation.py
                                      │
                                      ▼
                              test-coverage eval
                                      │
                              ┌───────┴───────┐
                              ▼               ▼
                             CSV            figures
```

## Project structure

```text
socratic-tutor/
├── README.md
├── config.yaml
├── pyproject.toml
├── requirements.txt
├── data/
│   ├── raw/dialogues/
│   ├── processed/
│   │   ├── legacy_parsed/
│   │   ├── jsonl/
│   │   └── progression/
│   └── evaluation/
├── models/
├── logs/chat/
├── results/
│   ├── evaluation/
│   └── figures/
├── notebooks/
├── scripts/
├── src/socratic_tutor/
│   ├── config.py
│   ├── data/
│   ├── model/
│   ├── training/
│   ├── tutor/
│   ├── evaluation/
│   └── ui/
└── tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For GPU training, install the PyTorch build appropriate for your CUDA environment if the default package is not suitable.

## 1. Add source dialogues

Put the original `.txt` dialogue files under:

```text
data/raw/dialogues/
```

The parser expects tags such as `<problem>`, `<bug_code>`, `<bug_desc>`, `<bug_fixes>`, `<unit_tests>`, `<stu_desc>`, and `<dialogue>`. Inside `<dialogue>`, it recognizes `User:`, `Assistant:`, `<code>...</code>`, and `<alt>`.

## 2. Preprocess

```bash
python scripts/preprocess_data.py
```

This runs both preserved preprocessing paths:

- legacy CSV + `*_full.json` export
- normalized per-file JSONL + `combined.jsonl`

## 3. Dialogue progression

```bash
python scripts/process_progression.py
```

The original Early/Mid/Late rule is preserved: first 33%, middle 33%, and final portion of each dialogue.

## 4. Inspect/build SFT examples

```bash
python scripts/build_dataset.py
```

Each assistant turn becomes a training target. Assistant alternatives are also included when `training.use_alternatives: true`.

## 5. Train with QLoRA

```bash
python scripts/train.py
```

Default training settings are the settings present in the original notebook: `microsoft/Phi-3-mini-4k-instruct`, 4-bit NF4 quantization, LoRA rank 16, alpha 32, dropout 0.05, two epochs, batch size 2, gradient accumulation 8, learning rate `2e-4`, cosine schedule, and maximum sequence length 1024.

The trained adapter is written to `models/socratic_phi3_lora/`.

## 6. Run the Socratic tutor

```bash
python scripts/run_tutor.py
```

The application loads the base model plus LoRA adapter through one shared model-loading implementation. The tutor constructs the prompt, generates a response, and applies the original short-question/solution-language guardrails.

## 7. Prepare chat logs for evaluation

After collecting transcripts in `logs/chat/`:

```bash
python scripts/prepare_evaluation.py
```

This reproduces the notebook's sequence:

1. combine JSON chat logs
2. assign unit tests
3. add problem titles
4. reorder `title` after `timestamp`

## 8. Evaluate

```bash
python scripts/evaluate.py
```

The current metric is the percentage of reference unit-test lines that appear verbatim in the user-submitted tests.

## 9. Visualize

```bash
python scripts/visualize.py
```

Figures are written to `results/figures/`.

## 10. Run tests

```bash
pytest
```

The tests cover parsing, dataset construction, prompting, guardrails, and evaluation matching.

## Important research behavior

The tutor is designed to ask one short Socratic question rather than directly reveal a programming fix. The guardrail layer checks for solution-like language and falls back to a diagnostic question when necessary.
