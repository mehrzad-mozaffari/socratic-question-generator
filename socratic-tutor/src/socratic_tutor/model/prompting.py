SYSTEM_PROMPT = (
    "You are a patient, Socratic coding tutor. Ask ONE short, targeted question per turn. "
    "No solutions. Focus on verifying assumptions, loop bounds, prints, and debuggers. <= 60 words."
)


def format_context(problem=None, notes=None):
    parts = []
    if problem:
        parts.append(f"Problem: {problem}")
    if notes:
        parts.append(f"Student notes: {notes}")
    return "\n".join(parts)


def render_turn(turn):
    content = turn["content"]
    if turn.get("code"):
        content += f"\n<code>\n{turn['code']}\n</code>"
    return f"{turn['role']}: {content}"


def build_inference_prompt(history, problem=None, notes=None):
    prompt = f"### System\n{SYSTEM_PROMPT}\n\n"
    context = format_context(problem, notes)
    if context:
        prompt += f"### Context\n{context}\n\n"
    prompt += "### Dialogue\n"
    prompt += "\n".join(render_turn(t) for t in history)
    prompt += "\n\n### Assistant\n"
    return prompt
