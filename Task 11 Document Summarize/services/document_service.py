import json
import os
from pathlib import Path
from typing import Any

import io

import requests
from dotenv import load_dotenv
from docx import Document
from pypdf import PdfReader

from prompts.document_summary_prompt import SYSTEM_PROMPT

PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR / ".env"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-5.6-luna-pro"
MAX_DOCUMENT_CHARS = 50_000
MAX_SUMMARY_CHARS = 5_000
load_dotenv(dotenv_path=ENV_FILE)


class DocumentServiceError(RuntimeError):
    pass


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    try:
        if suffix == ".pdf":
            text = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(content)).pages)
        elif suffix == ".docx":
            text = "\n".join(paragraph.text for paragraph in Document(io.BytesIO(content)).paragraphs)
        else:
            raise DocumentServiceError("Only PDF and Word (.docx) files are supported.")
    except DocumentServiceError:
        raise
    except Exception as exc:
        raise DocumentServiceError("The document could not be read.") from exc
    text = text.strip()
    if not text:
        raise DocumentServiceError("The document does not contain extractable text.")
    if len(text) > MAX_DOCUMENT_CHARS:
        raise DocumentServiceError("The document is too long to summarize.")
    return text


def _parse_summary(payload: Any) -> str:
    if not isinstance(payload, dict) or not isinstance(payload.get("summary"), str) or not payload["summary"].strip():
        raise DocumentServiceError("The model returned an invalid summary.")
    summary = payload["summary"].strip()
    if len(summary) > MAX_SUMMARY_CHARS:
        raise DocumentServiceError("The summary exceeded the allowed length.")
    return summary


def summarize_document(text: str) -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise DocumentServiceError("API_KEY is not configured.")
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": MODEL_NAME, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}], "temperature": 0.1, "response_format": {"type": "json_object"}},
            timeout=60,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return _parse_summary(json.loads(content))
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise DocumentServiceError("Unable to generate a document summary.") from exc
