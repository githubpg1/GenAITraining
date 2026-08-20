# Document Summary AI

A FastAPI application that accepts PDF or Word `.docx` uploads, extracts their text, sends it to OpenRouter's **OpenAI: GPT-5.6 Luna Pro** model, and displays a concise summary.

## Setup

Python 3.10+ is required. From this folder:

```text
pip install -r requirements.txt
```

Create or edit `.env` in this same folder:

```text
API_KEY=your_openrouter_api_key
```

Never commit `.env`. The server loads it relative to `app.py`, so the application can be started from another working directory. The API key is never sent to the browser.

## Run

```text
uvicorn app:app --reload
```

Open <http://127.0.0.1:8001> if using the command below, or <http://127.0.0.1:8000> if that port is available:

```text
uvicorn app:app --reload --port 8001
```

## Supported files

- PDF (`.pdf`)
- Microsoft Word Open XML (`.docx`)
- Maximum upload size: 10 MB
- Maximum extracted text sent to the model: 50,000 characters

Scanned/image-only PDFs need OCR and may not contain extractable text. The summary output is validated as JSON and limited to 5,000 characters. Invalid files, missing API keys, model failures, and malformed model output receive safe user-facing errors.
