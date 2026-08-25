import re

VERIFICATION_FAILURE = "I couldn't verify that answer against the available HR policy documents."


def validate_answer(answer: str, citations: list[dict], retrieved: list[dict]) -> bool:
    allowed = {(r["metadata"].get("document_name"), r["metadata"].get("section")) for r in retrieved}
    if not citations or any((c.get("document"), c.get("section")) not in allowed for c in citations):
        return False
    context = " ".join(r["text"] for r in retrieved)
    for number in re.findall(r"\$?\b\d+(?:\.\d+)?\b", answer):
        if number not in context:
            return False
    return True
