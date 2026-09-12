import re

SOLUTION_PATTERNS = [
    r"here is the fix",
    r"use this code",
    r"replace with",
    r"return\s+",
]
FALLBACK_QUESTION = "What do you observe when you check the value at each iteration?"
BLOCKED_RESPONSE = "Before changing code, what output do you get if you print the loop index and variables each iteration?"


def enforce_socratic_question(text: str, max_words=70) -> str:
    text = (text or "").strip().split("\n")[0].strip()
    if not text:
        return FALLBACK_QUESTION
    if any(re.search(pattern, text, re.I) for pattern in SOLUTION_PATTERNS):
        return BLOCKED_RESPONSE
    if not text.endswith(("?", "؟")):
        text = text.rstrip(".! ") + "?"
    if len(text.split()) > max_words:
        text = " ".join(text.split()[:65]) + " ... could you check that?"
    return text
