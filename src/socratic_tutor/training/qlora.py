import torch
from peft import LoraConfig
from trl import SFTConfig


def create_lora_config(r=16, alpha=32, dropout=0.05):
    return LoraConfig(
        r=r, lora_alpha=alpha, lora_dropout=dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none", task_type="CAUSAL_LM",
    )


def create_sft_config(cfg):
    has_ampere_or_newer = torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
    return SFTConfig(
        output_dir=cfg["output_dir"],
        num_train_epochs=cfg["epochs"],
        per_device_train_batch_size=cfg["train_batch_size"],
        per_device_eval_batch_size=cfg["eval_batch_size"],
        gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
        learning_rate=cfg["learning_rate"],
        logging_steps=cfg["logging_steps"],
        eval_strategy="steps",
        eval_steps=cfg["eval_steps"],
        save_steps=cfg["save_steps"],
        save_total_limit=cfg["save_total_limit"],
        bf16=bool(has_ampere_or_newer),
        fp16=not bool(has_ampere_or_newer) and torch.cuda.is_available(),
        lr_scheduler_type="cosine",
        dataset_text_field="text",
        warmup_ratio=cfg["warmup_ratio"],
        gradient_checkpointing=True,
        report_to="none",
        max_length=cfg["max_length"],
        packing=False,
    )
