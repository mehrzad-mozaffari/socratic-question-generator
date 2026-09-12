import re

SOLUTION_PATTERNS = [
    r"here is the fix",
    r"use this code",
    r"replace with",
    r"return\s+",
]


def enforce_socratic_question(text: str, max_words=70) -> str:
    text = text.strip().split("\n")[0].strip()
    if not text:
        return "What do you observe when you check the value at each iteration?"
    if any(re.search(p, text, re.I) for p in SOLUTION_PATTERNS):
        return "Before changing code, what output do you get if you print the loop index and variables each iteration?"
    if not text.endswith(("?", "؟")):
        text = text.rstrip(".! ") + "?"
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:65]) + " ... could you check that?"
    return text
