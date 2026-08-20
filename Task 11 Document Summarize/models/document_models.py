from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    success: bool
    summary: str | None = None
    error: str | None = None


class DocumentText(BaseModel):
    text: str = Field(min_length=1, max_length=50_000)
