import json
from openai import OpenAI
from src.config import settings
from src.generation.prompts import SYSTEM_PROMPT
from src.models.schemas import Classification


class LLMConfigurationError(RuntimeError):
    """Raised when live LLM mode is enabled without a configured key."""


def classify(question: str, retrieved: list[dict]) -> Classification:
    q = question.lower()
    if any(term in q for term in ("ignore the", "industry standard", "general knowledge")):
        return Classification.OUT_OF_SCOPE
    if "how much leave" in q and not any(term in q for term in ("vacation", "parental", "medical")):
        return Classification.AMBIGUOUS
    if not retrieved:
        return Classification.OUT_OF_SCOPE
    return Classification.ANSWERABLE


def mock_answer(question: str, retrieved: list[dict]) -> dict:
    classification = classify(question, retrieved)
    if classification == Classification.AMBIGUOUS:
        return {"answer": "Which type of leave do you mean: vacation, parental, or another type?", "classification": classification.value, "confidence": "HIGH", "citations": []}
    if classification == Classification.OUT_OF_SCOPE:
        return {"answer": "I couldn't find information about that in the available HR policy documents.", "classification": classification.value, "confidence": "HIGH", "citations": []}
    source = retrieved[0]["metadata"]
    q = question.lower()
    if "2025" in q:
        matching = [r for r in retrieved if r["metadata"].get("version") == "2.0"]
        if matching:
            source, text = matching[0]["metadata"], matching[0]["text"]
        else:
            text = retrieved[0]["text"]
    else:
        text = retrieved[0]["text"]
    answer = text.split("\n", 1)[-1]
    citation = {"document": source.get("document_name"), "section": source.get("section"), "page": source.get("page_number"), "version": source.get("version"), "effective_date": source.get("effective_date"), "source_file": source.get("source_file")}
    return {"answer": answer, "classification": Classification.ANSWERABLE.value, "confidence": "HIGH", "citations": [citation]}


def generate_answer(question: str, retrieved: list[dict], use_mock: bool | None = None) -> dict:
    if use_mock is None:
        use_mock = settings.offline_mode
    if use_mock:
        return mock_answer(question, retrieved)
    if settings.llm_provider not in {"openai", "openrouter", "ollama"}:
        raise LLMConfigurationError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
    if settings.llm_provider == "openai" and not settings.openai_api_key:
        raise LLMConfigurationError("OPENAI_API_KEY is not configured. Please add it to the project's .env file.")
    base_url = settings.ollama_base_url if settings.llm_provider == "ollama" else settings.openai_base_url
    api_key = "ollama" if settings.llm_provider == "ollama" else settings.openai_api_key
    client = OpenAI(api_key=api_key, base_url=base_url, timeout=settings.request_timeout)
    context = "\n\n".join(r["text"] for r in retrieved)
    request = {
        "model": settings.llm_model,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": f"Question: {question}\nContext:\n{context}"}],
    }
    # GPT-5.6 Luna is a reasoning model and does not accept temperature.
    if not settings.llm_model.lower().startswith("openai/gpt-5.6"):
        request["temperature"] = 0
    response = client.chat.completions.create(**request)
    return json.loads(response.choices[0].message.content)
