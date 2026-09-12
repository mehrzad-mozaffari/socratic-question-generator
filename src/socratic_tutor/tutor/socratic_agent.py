from socratic_tutor.model.prompting import build_inference_prompt
from socratic_tutor.model.generation import generate_question
from socratic_tutor.tutor.guardrails import enforce_socratic_question


class SocraticTutor:
    """High-level tutor: prompt -> generation -> guardrails."""
    def __init__(self, model, tokenizer, max_new_tokens=48, greedy=True,
                 temperature=0.7, top_p=0.9, repetition_penalty=1.1):
        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens
        self.greedy = greedy
        self.temperature = temperature
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty

    def ask(self, history, problem=None, notes=None):
        prompt = build_inference_prompt(history, problem=problem, notes=notes)
        generated = generate_question(
            self.model, self.tokenizer, prompt,
            max_new_tokens=self.max_new_tokens,
            greedy=self.greedy,
            temperature=self.temperature,
            top_p=self.top_p,
            repetition_penalty=self.repetition_penalty,
        )
        return enforce_socratic_question(generated)
