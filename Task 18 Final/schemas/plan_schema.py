from pydantic import BaseModel, Field
from typing import List, Optional

class PlanStep(BaseModel):
    step_id: int = Field(..., description="Unique identifier for the step")
    description: str = Field(..., description="Description of the step")
    tool: str = Field(..., description="Tool to be used for the step")
    inputs: dict = Field(default_factory=dict, description="Inputs for the tool")
    dependencies: List[int] = Field(default_factory=list, description="List of step IDs that this step depends on")
    expected_output: str = Field(..., description="Expected output of the step")
    action_possible: bool = Field(default=False, description="Whether the step could lead to an actionable finding")

class PlannerPlan(BaseModel):
    plan_id: str = Field(..., description="Unique identifier for the plan")
    query: str = Field(..., description="The user query that this plan is addressing")
    steps: List[PlanStep] = Field(..., description="List of steps in the plan")