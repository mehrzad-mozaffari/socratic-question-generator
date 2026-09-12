import torch


def generate_question(model, tokenizer, prompt, max_new_tokens=48, greedy=True,
                      temperature=0.7, top_p=0.9, repetition_penalty=1.1):
    """Generate only the new assistant continuation; guardrails are applied by the tutor layer."""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
    with torch.no_grad():
        kwargs = {
            "max_new_tokens": max_new_tokens,
            "do_sample": not greedy,
            "repetition_penalty": repetition_penalty,
            "eos_token_id": tokenizer.eos_token_id,
            "pad_token_id": tokenizer.pad_token_id,
            "use_cache": False,
        }
        if not greedy:
            kwargs.update(top_p=top_p, temperature=temperature)
        output = model.generate(**inputs, **kwargs)
    generated = tokenizer.decode(output[0], skip_special_tokens=True)
    # The original notebook sliced by the prompt string; retain that behavior,
    # while falling back safely if tokenizer decoding normalizes whitespace.
    generated = generated[len(prompt):].strip() if generated.startswith(prompt) else generated.strip()
    return generated
