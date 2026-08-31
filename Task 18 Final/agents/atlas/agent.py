# Atlas Planner Agent
# Responsible for converting user queries into structured execution plans.

import json
from typing import Dict, Any, List
from schemas.plan_schema import PlannerPlan, PlanStep
from tools.registry import ToolRegistry
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from config.settings import settings
from config.models import models

class AtlasPlanner:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()
        # In a real implementation, we would load the model based on the configuration
        # For now, we'll simulate the model with a placeholder
        self.model = models.planner  # This is just a placeholder; actual model loading would be done here

    def generate_plan(self, user_query: str, available_tools: List[str], memory_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structured execution plan based on the user query.
        This is a placeholder implementation. In a real system, this would call the LLM.
        """
        # For demonstration, we'll create a simple plan for the example query.
        # In reality, this would involve prompting the LLM with the user query, available tools, and memory context.
        plan = PlannerPlan(
            plan_id="PLAN-001",
            query=user_query,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Retrieve ticket 4021",
                    tool="ticket_get",
                    inputs={"ticket_id": "4021"},
                    dependencies=[],
                    expected_output="Ticket details including issue category and customer ID",
                    action_possible=False
                ),
                PlanStep(
                    step_id=2,
                    description="Identify issue category",
                    tool="ticket_analysis",  # This would be a tool that analyzes the ticket to get the issue category
                    inputs={},
                    dependencies=[1],
                    expected_output="Issue category of the ticket",
                    action_possible=False
                ),
                PlanStep(
                    step_id=3,
                    description="Find similar customers",
                    tool="semantic_ticket_search",
                    inputs={"query": "login issue", "ticket_id": "4021"},
                    dependencies=[2],
                    expected_output="List of tickets with similar issue category",
                    action_possible=False
                ),
                PlanStep(
                    step_id=4,
                    description="Check churn status",
                    tool="churn_status_lookup",
                    inputs={},
                    dependencies=[3],
                    expected_output="Churn status of the customers found",
                    action_possible=True
                )
            ]
        )
        return plan.dict()

# Example usage (for testing purposes)
if __name__ == "__main__":
    planner = AtlasPlanner()
    # This is a simplified example; in reality, the available_tools and memory_context would be provided by the orchestrator
    plan = planner.generate_plan(
        user_query="Which customers had the same login issue as ticket 4021, and did any of them churn afterward?",
        available_tools=["ticket_get", "ticket_analysis", "semantic_ticket_search", "churn_status_lookup"],
        memory_context={}
    )
    print(json.dumps(plan, indent=2))