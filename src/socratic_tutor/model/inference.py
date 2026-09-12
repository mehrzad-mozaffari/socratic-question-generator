"""Compatibility wrapper for direct model inference."""
from .prompting import build_inference_prompt
from .generation import generate_question
from socratic_tutor.tutor.guardrails import enforce_socratic_question


def generate_socratic_question(model, tokenizer, history, problem=None, notes=None,
                               max_new_tokens=48, greedy=True, temperature=0.7, top_p=0.9,
                               repetition_penalty=1.1):
    prompt = build_inference_prompt(history, problem=problem, notes=notes)
    text = generate_question(
        model, tokenizer, prompt, max_new_tokens=max_new_tokens, greedy=greedy,
        temperature=temperature, top_p=top_p, repetition_penalty=repetition_penalty,
    )
    return enforce_socratic_question(text)
