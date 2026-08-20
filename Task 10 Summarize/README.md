# Customer Email AI Assistant

A small FastAPI application that sends a customer email to OpenRouter's **5.6 Luna** model and displays a concise summary and a professional suggested reply. The API key stays on the backend.

## Structure

- `app.py` — FastAPI routes and protection against rapid duplicate requests
- `services/openrouter_service.py` — dotenv loading and OpenRouter integration
- `models/email_models.py` — independent Pydantic validation
- `prompts/customer_support_prompt.py` — support and hallucination-prevention instructions
- `templates/index.html`, `static/` — vanilla HTML, CSS, and JavaScript UI

## Requirements and setup

Python 3.10+ is required. From this directory:

```text
pip install -r requirements.txt
```

The existing `.env` must contain:

```text
API_KEY=your_openrouter_api_key
```

Do not commit `.env`; it is ignored by Git. Copy `.env.example` only as a template. If the key shown in an old `.env` has ever been shared, revoke it and create a replacement.

## Run

From `Task1/Practice`:

```text
uvicorn app:app --reload
```

Open <http://127.0.0.1:8000>.

The application resolves `.env` relative to `app.py`/the project directory, not the shell's current directory. Missing `API_KEY` is handled as a safe generic processing error. The key is never sent to the browser or included in logs/responses.

## Example

From: `customer@example.com`  
Subject: `Unable to access my account`  
Body: `I have been trying to log in since yesterday and need help.`

The output contains an email summary and a customer-facing reply. The Copy reply button copies only the reply text.

## Validation and test scenarios

Try account/login, refund/return, delayed delivery, billing/payment, and general complaint emails. Also verify missing/invalid From, missing Subject, missing Body, a body shorter than 10 characters, a subject over 200 characters, and a body over 10,000 characters. For service testing, temporarily use a test key or mock `requests.post` to verify malformed JSON, OpenRouter failure, and missing `API_KEY`; never use or commit real credentials in tests.

Backend validation runs independently, rejects invalid input before an OpenRouter call, validates JSON and string fields from the model, and rejects outputs over 1,000 summary or 5,000 reply characters.

## Troubleshooting

- `Unable to process...`: check that the key exists in this directory's `.env`, the model identifier is available to your OpenRouter account, and network access is available.
- Validation messages: correct the highlighted input and submit again.
- If a key has been exposed, revoke it immediately and replace the local `.env` value.
