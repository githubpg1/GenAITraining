"""Central project configuration loaded from the project-local .env file."""
from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


class Settings:
    llm_provider = os.getenv("LLM_PROVIDER", "openrouter").lower()
    llm_model = os.getenv("LLM_MODEL", "openai/gpt-5.6-luna")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "") or openrouter_api_key
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1") or None
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
    offline_mode = os.getenv("OFFLINE_MODE", "false").lower() == "true"
    request_timeout = _int("LLM_TIMEOUT_SECONDS", 90)
    embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chroma_collection_name = os.getenv("CHROMA_COLLECTION_NAME", "hr_policy_documents")
    chroma_persist_directory = str((PROJECT_ROOT / os.getenv("CHROMA_PERSIST_DIRECTORY", "chroma_db")).resolve())
    top_k = _int("TOP_K", 5)
    relevance_threshold = _float("RELEVANCE_THRESHOLD", 0.40)
    chunk_size = _int("CHUNK_SIZE", 650)
    chunk_overlap = _int("CHUNK_OVERLAP", 100)
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = _int("API_PORT", 8000)


settings = Settings()
