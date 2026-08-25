# Project 15 — Grounded Q&A Over Company Policy Documents

A local demonstration RAG application for answering HR policy questions with provenance, version handling, relevance filtering, and grounded responses.

## Repository placement

This project is located at `ey-agentic-ai-training-02/Tasks/Project 15 RAG`. The sibling `C:\Users\user\Documents\AiTraining\Tasks` folder was inspected for patterns and remains unchanged. FastAPI/Jinja/vanilla JavaScript conventions from Tasks 10–11 were reused conceptually.

## Setup

Python 3.12.10 was discovered on this machine. Create or select an environment, then install the packages listed in `requirements.txt`. The Windows-compatible pins for `chroma-hnswlib` and `onnxruntime` avoid the native DLL/wheel failures encountered with the newest builds. The key is loaded from `.env` and is not hard-coded. `OFFLINE_MODE=true` enables deterministic mock generation; otherwise a configured key enables the LLM path. Tests use deterministic mock generation and do not require a key.

OpenRouter's verified model ID for GPT-5.6 Luna is `openai/gpt-5.6-luna` (not `gpt-5.6-luna`). Set `LLM_PROVIDER=openrouter`, `OPENAI_BASE_URL=https://openrouter.ai/api/v1`, `LLM_MODEL=openai/gpt-5.6-luna`, and provide `OPENROUTER_API_KEY` in `.env`. The code aliases this value to the OpenAI-compatible client key. GPT-5.6 Luna does not accept `temperature`, so the client omits it for GPT-5.6 models. If the key is missing or the provider is unsupported, `/ask` returns a clear configuration error instead of silently using mock output.

Default configuration includes OpenAI provider, `gpt-4.1-mini`, `sentence-transformers/all-MiniLM-L6-v2`, Chroma collection `hr_policy_documents`, persistent storage in `chroma_db/`, top-k 5, and relevance threshold 0.40. The threshold is an initial value and should be calibrated against the evaluation set.

## Generate and ingest policies

Run `python generate_policies.py`, then `python -m src.ingestion.ingest`. Ingestion uses page-preserving PDF extraction, section-aware chunks, deterministic IDs, and Chroma upsert semantics, so repeated runs do not duplicate chunks.

Scanned PDFs with no extractable text are reported as requiring OCR rather than silently ingested.

## Run the API and UI

Run `uvicorn src.api.app:app --reload` and open `http://127.0.0.1:8000`. The API endpoint is `POST /ask` with `{ "question": "..." }`. The browser UI displays classification, confidence, sources, metadata, and expandable context.

Without a configured OpenAI key, the current implementation uses deterministic mock generation for the local demonstration. With a key, the configured OpenAI model is used.

## Tests

Run `pytest -q`. The evaluation questions are in `evaluation/evaluation_questions.json`.

## Architecture

`PDF → page extraction → section detection → chunking → Sentence Transformers embeddings → persistent ChromaDB → similarity filtering → classification → grounded generation → citation/numeric validation → API/UI response`.

The validator rejects unsupported citations and numeric claims. Retrieved documents are treated as untrusted data and cannot override the system instructions. Current and historical source metadata are preserved for version-aware responses.

## Corpus

The generated demonstration corpus contains current time-off, business travel and expense, parental leave, employee benefits, and historical 2025 time-off policies. It intentionally does not contain gym membership, Netflix, pet insurance, or meal-delivery reimbursement policies. Absence from the corpus is not treated as an explicit policy denial.

## Troubleshooting

- **Missing API key:** configure `OPENAI_API_KEY` in the project `.env`; no key is needed for deterministic tests.
- **Missing dependency:** install only the packages in `requirements.txt` in the selected environment.
- **Chroma failure:** use Python 3.12 with the pinned `chroma-hnswlib==0.7.5` and `onnxruntime==1.20.1`, remove only a disposable/rebuildable `chroma_db/`, then rerun ingestion. Do not mix databases created by different Chroma versions.
- **PDF parsing failure:** verify the file is readable and contains extractable text; scanned documents require OCR.
- **Model/API failure:** check the configured provider/model, key permissions, network access, and timeout; never place the key in source code or logs.

See `PLAN.md` for the complete implementation plan, scope, decisions, verification checklist, and limitations.
