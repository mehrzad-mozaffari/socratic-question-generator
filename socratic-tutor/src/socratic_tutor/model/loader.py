import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel


def get_compute_dtype():
    if not torch.cuda.is_available():
        return torch.float32
    major, _ = torch.cuda.get_device_capability(0)
    return torch.bfloat16 if major >= 8 else torch.float16


def make_bnb_config():
    dtype = get_compute_dtype()
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=dtype,
        bnb_4bit_use_double_quant=True,
    )


def load_tokenizer(path, trust_remote_code=True):
    tokenizer = AutoTokenizer.from_pretrained(path, use_fast=True, trust_remote_code=trust_remote_code)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_model(base_model, adapter_dir=None, merged_model_dir="", use_merged=False, trust_remote_code=True):
    bnb_cfg = make_bnb_config()
    if use_merged and merged_model_dir:
        model = AutoModelForCausalLM.from_pretrained(
            merged_model_dir, quantization_config=bnb_cfg, device_map="auto",
            trust_remote_code=trust_remote_code, attn_implementation="eager"
        )
        tokenizer = load_tokenizer(merged_model_dir, trust_remote_code)
    else:
        tokenizer = load_tokenizer(adapter_dir or base_model, trust_remote_code)
        base = AutoModelForCausalLM.from_pretrained(
            base_model, quantization_config=bnb_cfg, device_map="auto",
            trust_remote_code=trust_remote_code, attn_implementation="eager"
        )
        model = PeftModel.from_pretrained(base, adapter_dir) if adapter_dir else base
    model.eval()
    model.config.use_cache = False
    return model, tokenizer
