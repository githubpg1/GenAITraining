from src.config import settings


def retrieve(question: str, store, top_k: int | None = None) -> list[dict]:
    candidates = store.query(question, top_k or settings.top_k)
    return [item for item in candidates if item["score"] >= settings.relevance_threshold]
