# Tool Registry for the Ticket Intelligence System
# Central registry of all tools available to agents.

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class ToolMetadata:
    name: str
    purpose: str
    owner: str  # e.g., "retrieval", "memory", "jira"
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    side_effect: bool = False
    allowed_agents: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)
    retryable: bool = False

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolMetadata] = {}
        self._register_tools()

    def _register_tools(self):
        # Register all tools here. In a real system, we would scan the tools directory or import them.
        # For now, we'll register a few placeholder tools.
        self.register_tool(ToolMetadata(
            name="ticket_get",
            purpose="Retrieve a ticket by ID",
            owner="retrieval",
            input_schema={"ticket_id": "str"},
            output_schema={"ticket_id": "str", "issue_category": "str", "customer_id": "str"},
            side_effect=False,
            allowed_agents=["Scout"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="ticket_search",
            purpose="Search tickets using filters",
            owner="retrieval",
            input_schema={"filters": "dict"},
            output_schema={"tickets": "list"},
            side_effect=False,
            allowed_agents=["Scout"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="semantic_ticket_search",
            purpose="Find tickets semantically similar to a query",
            owner="retrieval",
            input_schema={"query": "str", "limit": "int"},
            output_schema={"results": "list"},
            side_effect=False,
            allowed_agents=["Scout"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="churn_status_lookup",
            purpose="Check customer churn status",
            owner="retrieval",
            input_schema={"customer_id": "str"},
            output_schema={"churned": "bool", "churn_date": "str"},
            side_effect=False,
            allowed_agents=["Scout"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="stm_read",
            purpose="Read current run state",
            owner="memory",
            input_schema={"execution_id": "str"},
            output_schema={"state": "dict"},
            side_effect=False,
            allowed_agents=["Atlas", "Scout", "JiraOps"],
            retryable=False
        ))
        self.register_tool(ToolMetadata(
            name="stm_update",
            purpose="Update current run state",
            owner="memory",
            input_schema={"execution_id": "str", "updates": "dict"},
            output_schema={"success": "bool"},
            side_effect=True,
            allowed_agents=["Atlas", "Scout", "JiraOps"],
            retryable=False
        ))
        self.register_tool(ToolMetadata(
            name="working_memory_create",
            purpose="Create working memory for a step",
            owner="memory",
            input_schema={"execution_id": "str", "step_id": "int"},
            output_schema={"success": "bool"},
            side_effect=True,
            allowed_agents=["Scout"],
            retryable=False
        ))
        self.register_tool(ToolMetadata(
            name="working_memory_clear",
            purpose="Clear working memory for a step",
            owner="memory",
            input_schema={"execution_id": "str", "step_id": "int"},
            output_schema={"success": "bool"},
            side_effect=True,
            allowed_agents=["Scout"],
            retryable=False
        ))
        self.register_tool(ToolMetadata(
            name="ltm_search",
            purpose="Search long-term memory",
            owner="memory",
            input_schema={"query": "str", "limit": "int"},
            output_schema={"results": "list"},
            side_effect=False,
            allowed_agents=["Atlas", "Scout", "JiraOps"],
            retryable=False
        ))
        self.register_tool(ToolMetadata(
            name="jira.create_runtime_task",
            purpose="Create a runtime task in Jira",
            owner="jira",
            input_schema={
                "execution_id": "str",
                "plan_id": "str",
                "task_id": "str",
                "summary": "str",
                "description": "str",
                "dependencies": "list",
                "tools": "list",
                "expected_output": "str",
                "acceptance_criteria": "list",
                "labels": "list"
            },
            output_schema={"success": "bool", "jira_key": "str", "jira_id": "str", "status": "str"},
            side_effect=True,
            allowed_agents=["Orchestrator"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="jira.update_runtime_task",
            purpose="Update a runtime task in Jira",
            owner="jira",
            input_schema={
                "jira_key": "str",
                "status": "str",
                "execution_id": "str",
                "task_id": "str"
            },
            output_schema={"success": "bool", "jira_key": "str", "status": "str"},
            side_effect=True,
            allowed_agents=["Orchestrator"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="jira.add_runtime_task_comment",
            purpose="Add a comment to a runtime task in Jira",
            owner="jira",
            input_schema={
                "jira_key": "str",
                "task_id": "str",
                "execution_id": "str",
                "output_json": "dict"
            },
            output_schema={"success": "bool", "comment_id": "str"},
            side_effect=True,
            allowed_agents=["Orchestrator"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="jira.create_ticket",
            purpose="Create a business Jira ticket",
            owner="jira",
            input_schema={
                "project": "str",
                "issue_type": "str",
                "summary": "str",
                "description": "str",
                "labels": "list",
                "customer_id": "str",
                "issue_category": "str",
                "evidence": "list"
            },
            output_schema={"success": "bool", "jira_key": "str", "jira_id": "str"},
            side_effect=True,
            allowed_agents=["JiraOps"],
            retryable=True
        ))
        self.register_tool(ToolMetadata(
            name="jira.update_ticket",
            purpose="Update a business Jira ticket",
            owner="jira",
            input_schema={
                "jira_key": "str",
                "fields": "dict",
                "comment": "str"
            },
            output_schema={"success": "bool", "jira_key": "str"},
            side_effect=True,
            allowed_agents=["JiraOps"],
            retryable=True
        ))

    def register_tool(self, tool: ToolMetadata):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolMetadata]:
        return self._tools.get(name)

    def get_tool_names(self) -> List[str]:
        return list(self._tools.keys())

    def get_tools_by_owner(self, owner: str) -> List[ToolMetadata]:
        return [tool for tool in self._tools.values() if tool.owner == owner]

    def get_tools_by_agent(self, agent: str) -> List[ToolMetadata]:
        return [tool for tool in self._tools.values() if agent in tool.allowed_agents]

# Example usage (for testing purposes)
if __name__ == "__main__":
    registry = ToolRegistry()
    print("Registered tools:")
    for name in registry.get_tool_names():
        tool = registry.get_tool(name)
        print(f"  {name}: {tool.purpose} (allowed agents: {tool.allowed_agents})")