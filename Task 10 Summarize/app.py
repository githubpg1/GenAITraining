import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.email_models import CustomerEmailRequest, EmailResponse
from services.openrouter_service import OpenRouterServiceError, generate_response

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Customer Email AI Assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
_last_request_at = 0.0
MIN_REQUEST_INTERVAL_SECONDS = 2.0


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/process-email", response_model=EmailResponse)
async def process_email(email: CustomerEmailRequest):
    global _last_request_at
    now = time.monotonic()
    if now - _last_request_at < MIN_REQUEST_INTERVAL_SECONDS:
        return EmailResponse(success=False, error="Please wait a moment before trying again.")
    _last_request_at = now
    try:
        result = generate_response(email)
        return EmailResponse(success=True, **result)
    except OpenRouterServiceError:
        return EmailResponse(success=False, error="Unable to process the customer email.")
    except Exception:
        return EmailResponse(success=False, error="Unable to process the customer email.")
