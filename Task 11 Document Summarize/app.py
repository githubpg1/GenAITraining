import logging
import time
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from models.document_models import SummaryResponse
from services.document_service import DocumentServiceError, extract_text, summarize_document

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
_last_request_at = 0.0
MIN_REQUEST_INTERVAL_SECONDS = 2.0
app = FastAPI(title="Document Summary AI")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/summarize-document", response_model=SummaryResponse)
async def summarize(file: UploadFile = File(...)):
    global _last_request_at
    now = time.monotonic()
    if now - _last_request_at < MIN_REQUEST_INTERVAL_SECONDS:
        return SummaryResponse(success=False, error="Please wait a moment before trying again.")
    _last_request_at = now
    try:
        content = await file.read()
        if len(content) > MAX_UPLOAD_BYTES:
            raise DocumentServiceError("The file must be 10 MB or smaller.")
        text = extract_text(file.filename or "", content)
        return SummaryResponse(success=True, summary=summarize_document(text))
    except DocumentServiceError as exc:
        message = str(exc)
        if message in {"Only PDF and Word (.docx) files are supported.", "The file must be 10 MB or smaller.", "The document does not contain extractable text.", "The document is too long to summarize."}:
            return SummaryResponse(success=False, error=message)
        return SummaryResponse(success=False, error="We couldn't generate a summary right now. Please try again.")
    except Exception:
        logger.exception("Unexpected document summary error")
        return SummaryResponse(success=False, error="We couldn't generate a summary right now. Please try again.")
