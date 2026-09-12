"""High-level inference helpers."""
from .prompting import build_inference_prompt
from .generation import generate_question


def generate_socratic_question(model, tokenizer, history, problem=None, notes=None,
                               max_new_tokens=48, greedy=True, temperature=0.7,
                               top_p=0.9):
    prompt = build_inference_prompt(history, problem=problem, notes=notes)
    return generate_question(
        model, tokenizer, prompt,
        max_new_tokens=max_new_tokens,
        greedy=greedy,
        temperature=temperature,
        top_p=top_p,
    )
