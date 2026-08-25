from enum import Enum
from pydantic import BaseModel, Field


class Classification(str, Enum):
    ANSWERABLE = "ANSWERABLE"
    AMBIGUOUS = "AMBIGUOUS"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"
    CONFLICTING_POLICY = "CONFLICTING_POLICY"


class Citation(BaseModel):
    document: str
    section: str
    page: int | None = None
    version: str | None = None
    effective_date: str | None = None
    source_file: str | None = None


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list)


class AskResponse(BaseModel):
    answer: str
    classification: Classification
    confidence: str
    sources: list[Citation] = Field(default_factory=list)
    supporting_context: list[str] = Field(default_factory=list)
