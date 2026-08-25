from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from src.models.schemas import AskRequest, AskResponse, Classification, Citation
from src.retrieval.embeddings import Embedder
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import retrieve
from src.generation.generator import generate_answer, LLMConfigurationError
from src.generation.grounding_validator import validate_answer, VERIFICATION_FAILURE

app = FastAPI(title="HR Policy Assistant")
_store = None


def get_store():
    global _store
    if _store is None:
        _store = VectorStore(Embedder())
    return _store


@app.get("/", response_class=HTMLResponse)
def home():
    return (Path(__file__).parents[2] / "ui" / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    try:
        results = retrieve(question, get_store())
        generated = generate_answer(question, results)
        citations = generated.get("citations", [])
        classification = generated.get("classification", Classification.INSUFFICIENT_CONTEXT.value)
        if classification == Classification.ANSWERABLE.value and not validate_answer(generated.get("answer", ""), citations, results):
            generated["answer"] = VERIFICATION_FAILURE
            generated["classification"] = Classification.INSUFFICIENT_CONTEXT.value
        return AskResponse(answer=generated.get("answer", VERIFICATION_FAILURE), classification=classification, confidence=generated.get("confidence", "LOW"), sources=[Citation(**c) for c in citations], supporting_context=[r["text"] for r in results])
    except HTTPException:
        raise
    except LLMConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Policy service unavailable: {type(exc).__name__}") from exc
