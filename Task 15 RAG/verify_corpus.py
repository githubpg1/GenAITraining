"""Verify policy files and the persistent Chroma corpus without calling an LLM."""
import json
from pathlib import Path
import chromadb
from src.config import PROJECT_ROOT, settings
from src.ingestion.parser import parse_pdf

MANIFEST_PATH = PROJECT_ROOT / "corpus_manifest.json"


def verify() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
    collection = client.get_or_create_collection(settings.chroma_collection_name)
    stored = collection.get(include=["metadatas", "documents"])
    metadata = stored.get("metadatas", [])
    documents = stored.get("documents", [])
    by_source: dict[str, list[tuple[dict, str]]] = {}
    for item, text in zip(metadata, documents):
        by_source.setdefault(item.get("source_file", "<missing>"), []).append((item, text))

    failures: list[str] = []
    print(f"collection={collection.name}")
    print(f"stored_chunks={collection.count()}")
    print("documents=")
    for expected in manifest["documents"]:
        path = PROJECT_ROOT / "documents" / ("historical" if "2025" in expected["source_file"] else "current") / expected["source_file"]
        if not path.exists():
            failures.append(f"missing file: {expected['source_file']}")
            print(f"- {expected['source_file']}: FILE_MISSING")
            continue
        try:
            parsed = parse_pdf(path)
            print(f"- {expected['source_file']}: pages={len(parsed.pages)} chars={len(parsed.text)} chunks={len(by_source.get(expected['source_file'], []))}")
        except ValueError as exc:
            failures.append(str(exc))
            print(f"- {expected['source_file']}: PARSE_FAILED")
            continue
        rows = by_source.get(expected["source_file"], [])
        if not rows:
            failures.append(f"not indexed: {expected['source_file']}")
            continue
        for fact in expected["required_facts"]:
            if not any(fact.lower() in text.lower() for _, text in rows):
                failures.append(f"missing fact in Chroma: {expected['source_file']} -> {fact}")
        for item, text in rows:
            required = ("document_id", "document_name", "section", "section_number", "version", "effective_date", "source_file", "page_number")
            missing = [key for key in required if not item.get(key)]
            if missing or not text.strip() or not isinstance(item.get("page_number"), int):
                failures.append(f"invalid metadata: {expected['source_file']} -> {missing or 'page_number/text'}")

    print(f"distinct_sources={len(by_source)}")
    if failures:
        print("status=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify())
