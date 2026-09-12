from pathlib import Path
from trl import SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer
from socratic_tutor.model.loader import make_bnb_config
from socratic_tutor.training.dataset import load_training_datasets
from socratic_tutor.training.qlora import create_lora_config, create_sft_config


def train(cfg):
    model_cfg = cfg["model"]
    train_cfg = cfg["training"]
    dataset_path = Path(cfg["paths"]["training_dataset"])
    if not dataset_path.is_absolute():
        from socratic_tutor.config import resolve_path
        dataset_path = resolve_path(dataset_path)

    train_ds, eval_ds, examples = load_training_datasets(
        dataset_path,
        train_split=train_cfg["train_split"],
        use_alts=train_cfg["use_alternatives"],
        seed=train_cfg.get("seed", 42),
    )
    print(f"Built {len(examples)} samples. Train={len(train_ds)} Eval={len(eval_ds)}")

    tokenizer = AutoTokenizer.from_pretrained(model_cfg["base_model"], use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_cfg["base_model"],
        quantization_config=make_bnb_config(),
        device_map="auto",
        trust_remote_code=cfg["runtime"]["trust_remote_code"],
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        peft_config=create_lora_config(
            train_cfg["lora_r"], train_cfg["lora_alpha"], train_cfg["lora_dropout"]
        ),
        processing_class=tokenizer,
        args=create_sft_config(train_cfg),
    )
    trainer.train()
    out = Path(train_cfg["output_dir"])
    if not out.is_absolute():
        from socratic_tutor.config import resolve_path
        out = resolve_path(out)
    out.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(out))
    tokenizer.save_pretrained(str(out))
    print(f"Saved LoRA adapter + tokenizer to: {out}")
