"""Run PDF ingestion: python -m src.ingestion.ingest"""
from pathlib import Path
from src.config import PROJECT_ROOT, settings
from src.ingestion.parser import parse_pdf, detect_sections
from src.ingestion.chunker import chunk_sections
from src.retrieval.embeddings import Embedder
from src.retrieval.vector_store import VectorStore


def document_id(path: Path) -> str:
    return path.stem.replace("_", "-").lower()


def ingest_documents() -> int:
    embedder = Embedder()
    store = VectorStore(embedder)
    total = 0
    for path in sorted((PROJECT_ROOT / "documents").rglob("*.pdf")):
        parsed = parse_pdf(path)
        version = "2.0" if "2025" in path.name else {
            "business_travel_expense_policy_2026.pdf": "1.0",
            "parental_leave_policy_2026.pdf": "2.1",
            "employee_benefits_policy_2026.pdf": "4.0",
        }.get(path.name, "3.0")
        effective_date = "2025-01-01" if "2025" in path.name else "2026-01-01"
        name = path.stem.replace("_", " ").replace(" 2025", "").replace(" 2026", "").title()
        chunks = []
        for page in parsed.pages:
            sections = detect_sections(page.text)
            chunks.extend(chunk_sections(sections, document_id(path), name, version, effective_date,
                                         path.name, settings.chunk_size, settings.chunk_overlap,
                                         page.page_number))
        store.upsert(chunks)
        total += len(chunks)
        print(f"Ingested {path.name}: {len(chunks)} chunks")
    print(f"Total chunks upserted: {total}")
    return total


if __name__ == "__main__":
    ingest_documents()
