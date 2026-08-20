import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from models.email_models import CustomerEmailRequest
from prompts.customer_support_prompt import SYSTEM_PROMPT

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_DIR, ".env")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# OpenRouter requires the provider-qualified model ID, not the display name.
MODEL_NAME = "openai/gpt-5.6-luna-pro"
MAX_SUMMARY_LENGTH = 1_000
MAX_REPLY_LENGTH = 5_000

load_dotenv(dotenv_path=ENV_FILE)


class OpenRouterServiceError(RuntimeError):
    pass


def _validated_result(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise OpenRouterServiceError("The model returned an invalid response.")
    summary = payload.get("summary")
    reply = payload.get("reply")
    if not isinstance(summary, str) or not summary.strip():
        raise OpenRouterServiceError("The model returned an invalid summary.")
    if not isinstance(reply, str) or not reply.strip():
        raise OpenRouterServiceError("The model returned an invalid reply.")
    if len(summary) > MAX_SUMMARY_LENGTH or len(reply) > MAX_REPLY_LENGTH:
        raise OpenRouterServiceError("The model response exceeded the allowed length.")
    return {"summary": summary.strip(), "reply": reply.strip()}


def generate_response(email: CustomerEmailRequest) -> dict[str, str]:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise OpenRouterServiceError("API_KEY is not configured.")

    user_prompt = (
        "Customer Email\n\n"
        f"From:\n{email.from_}\n\n"
        f"Subject:\n{email.subject}\n\n"
        f"Body:\n{email.body}"
    )
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return _validated_result(json.loads(content))
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise OpenRouterServiceError("Unable to process the model response.") from exc
