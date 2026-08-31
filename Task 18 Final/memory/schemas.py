# Schemas for memory components
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ShortTermMemoryEntry(BaseModel):
    execution_id: str
    query: str
    plan: Dict[str, Any]
    completed_step_ids: List[int] = Field(default_factory=list)
    step_results: Dict[int, Dict[str, Any]] = Field(default_factory=dict)
    current_findings: List[Dict[str, Any]] = Field(default_factory=list)
    current_execution_context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class WorkingMemoryEntry(BaseModel):
    execution_id: str
    step_id: int
    attempt_number: int = Field(default=1)
    tool_inputs: Dict[str, Any] = Field(default_factory=dict)
    partial_retrievals: List[Any] = Field(default_factory=list)
    temporary_candidates: List[Any] = Field(default_factory=list)
    retry_information: Dict[str, Any] = Field(default_factory=dict)
    temporary_validation_state: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class LongTermMemoryEntry(BaseModel):
    finding_id: str = Field(..., description="Unique identifier for the finding")
    customer_id: str = Field(..., description="Customer ID")
    issue_category: str = Field(..., description="Issue category")
    finding_type: str = Field(..., description="Type of finding (e.g., CHURN_AFTER_ISSUE)")
    source_tickets: List[str] = Field(default_factory=list, description="List of ticket IDs that are the source of this finding")
    confidence: float = Field(..., description="Confidence score of the finding (0.0 to 1.0)")
    jira_key: Optional[str] = Field(None, description="Jira issue key if a ticket was created")
    first_seen: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    evidence_hash: str = Field(..., description="Hash of the evidence supporting this finding")