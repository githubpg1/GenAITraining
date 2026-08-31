from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StepResult(BaseModel):
    step_id: int = Field(..., description="Identifier of the step that produced this result")
    status: str = Field(..., description="Status of the step execution (e.g., COMPLETED, FAILED)")
    evidence: List[Dict[str, Any]] = Field(default_factory=list, description="Evidence supporting the result")
    finding: Optional[str] = Field(None, description="The finding or outcome of the step")
    confidence: float = Field(..., description="Confidence score of the finding (0.0 to 1.0)")
    missing_information: List[str] = Field(default_factory=list, description="Any missing information that was required")
    actionable: bool = Field(False, description="Whether the result is actionable (may lead to a Jira action)")

class JiraActionRequest(BaseModel):
    action: str = Field(..., description="Action to perform: CREATE, UPDATE, or SKIP")
    customer_id: str = Field(..., description="Customer ID associated with the finding")
    issue_category: str = Field(..., description="Issue category of the finding")
    summary: str = Field(..., description="Summary for the Jira issue")
    description: str = Field(..., description="Description for the Jira issue")
    labels: List[str] = Field(default_factory=list, description="Labels for the Jira issue")
    evidence: List[Dict[str, Any]] = Field(default_factory=list, description="Evidence supporting the action")

class JiraActionResult(BaseModel):
    action: str = Field(..., description="Action performed: CREATE, UPDATE, or SKIP")
    status: str = Field(..., description="Status of the action (e.g., SUCCESS, FAILED)")
    jira_key: Optional[str] = Field(None, description="Jira issue key if action was CREATE or UPDATE")
    message: str = Field(..., description="Message describing the outcome")