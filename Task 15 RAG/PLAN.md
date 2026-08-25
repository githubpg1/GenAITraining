# Project 15 — Grounded Q&A Over Company Policy Documents

## Goal
Build a complete, grounded RAG assistant for answering questions from company HR policy documents with source attribution, version handling, hallucination prevention, a FastAPI backend, browser UI, and automated tests.

## Confirmed implementation decisions

- **Location:** `ey-agentic-ai-training-02/Tasks/Project 15 RAG`.
- **Repository safety:** Existing projects under the sibling `C:\Users\user\Documents\AiTraining\Tasks` directory are reference-only and must not be modified.
- **UI/API:** FastAPI backend with Jinja templates, static JavaScript, and CSS, reusing the established Tasks 10–11 pattern.
- **LLM:** Direct OpenAI by default; provider and model are configurable through `.env`.
- **Secrets:** `OPENAI_API_KEY` is loaded from the project-local `.env`; no secret is hard-coded, committed, displayed, or logged.
- **Embeddings:** Configurable Sentence Transformers model, default `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector store:** Persistent ChromaDB collection `hr_policy_documents` under `chroma_db/`.
- **Corpus:** Five generated sample PDFs: current time-off, travel/expense, parental leave, benefits, and historical time-off.
- **Offline testing:** Deterministic local/mock generation must support tests without an API key. Live OpenAI calls are optional and only run when configured.
- **OCR:** Scanned PDFs are reported as requiring OCR unless OCR is separately added.

## Scope

1. Inspect setup and install only missing dependencies.
2. Create realistic sample HR policy documents without unsupported gym, Netflix, pet-insurance, or meal-delivery policies.
3. Parse PDFs with page provenance and explicit edge-case handling.
4. Detect sections and create approximately 500–800-token chunks with overlap.
5. Generate deterministic IDs and idempotently persist embeddings in ChromaDB.
6. Retrieve and filter relevant context with metadata and version awareness.
7. Classify requests as `ANSWERABLE`, `AMBIGUOUS`, `OUT_OF_SCOPE`, `INSUFFICIENT_CONTEXT`, or `CONFLICTING_POLICY`.
8. Generate strictly grounded answers, validate citations and numeric claims, and reject unsupported claims.
9. Provide follow-up conversation support while retrieving on every turn.
10. Provide FastAPI `/ask`, a browser chatbot, tests, evaluation questions, and complete setup documentation.

## Verification checklist

- [ ] Target path verified; existing projects unchanged.
- [ ] Python and dependency availability inspected.
- [ ] Only missing dependencies installed and imports verified.
- [ ] `.env` ignored and `.env.example` contains no real key.
- [ ] Five policy PDFs generated and readable.
- [ ] Ingestion succeeds twice without duplicate chunks.
- [ ] Persistent ChromaDB collection and metadata verified.
- [ ] Current, historical, out-of-scope, ambiguous, and injection queries tested.
- [ ] FastAPI endpoint and browser UI smoke-tested.
- [ ] Full pytest suite executed.
- [ ] Actual results and limitations recorded in README.

## Known limitations

- Scanned/image-only PDFs require OCR.
- The initial relevance threshold is configurable and must be calibrated against the evaluation set.
- Direct OpenAI answers require a valid API key and network access; deterministic mock mode is used for offline tests.
- Generated policy PDFs are demonstration data and are not real HR advice.
