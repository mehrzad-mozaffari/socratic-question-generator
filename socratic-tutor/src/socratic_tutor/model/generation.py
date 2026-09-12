import re
import torch


def apply_guardrails(text: str, max_words=70) -> str:
    text = text.strip().split("\n")[0].strip()
    if not text:
        return "What do you observe when you check the value at each iteration?"
    if not text.endswith(("?", "؟")):
        text = text.rstrip(".! ") + "?"
    if len(text.split()) > max_words:
        text = " ".join(text.split()[:65]) + " ... could you check that?"
    if re.search(r"\b(here is the fix|use this code|replace with|return\s+)\b", text, re.I):
        return "Before changing code, what output do you get if you print the loop index and variables each iteration?"
    return text


def generate_question(model, tokenizer, prompt, max_new_tokens=48, greedy=True, temperature=0.7, top_p=0.9, repetition_penalty=1.1):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
    with torch.no_grad():
        kwargs = dict(
            max_new_tokens=max_new_tokens,
            do_sample=not greedy,
            repetition_penalty=repetition_penalty,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
            use_cache=False,
        )
        if not greedy:
            kwargs.update(top_p=top_p, temperature=temperature)
        output = model.generate(**inputs, **kwargs)
    generated = tokenizer.decode(output[0], skip_special_tokens=True)
    gen = generated[len(prompt):].strip()
    return apply_guardrails(gen)
