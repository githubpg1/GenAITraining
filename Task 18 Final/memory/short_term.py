# Short-Term Memory component for the Ticket Intelligence System
# Holds the current question's plan and results gathered so far in one run.

from typing import Dict, Any, Optional, List
from memory.chroma_manager import ChromaManager
from memory.schemas import ShortTermMemoryEntry
import json
from config.settings import settings

class ShortTermMemory:
    def __init__(self, chroma_manager: ChromaManager = None):
        self.chroma = chroma_manager or ChromaManager()

    def create(self, execution_id: str, query: str):
        """
        Initialize short-term memory for a new execution.
        """
        # In a real system, we might load any initial context here.
        # For now, we just create an empty STM entry.
        entry = ShortTermMemoryEntry(
            execution_id=execution_id,
            query=query,
            plan={},
            completed_step_ids=[],
            step_results={},
            current_findings=[],
            current_execution_context={}
        )
        self.chroma.stm_add(execution_id, entry)

    def read(self, execution_id: str) -> Optional[ShortTermMemoryEntry]:
        """
        Read the current short-term memory state for an execution.
        """
        return self.chroma.stm_get(execution_id)

    def update(self, execution_id: str, updates: Dict[str, Any]):
        """
        Update the short-term memory with new information.
        """
        self.chroma.stm_update(execution_id, updates)

    def finalize(self, execution_id: str):
        """
        Finalize the short-term memory for an execution.
        In a real system, we might move relevant information to long-term memory.
        """
        # For now, we just clear the STM after the execution is complete.
        # But note: the orchestrator should call this after generating the final result.
        self.chroma.stm_finalize(execution_id)

    # Helper methods for specific STM operations
    def add_plan(self, execution_id: str, plan: Dict[str, Any]):
        stm = self.read(execution_id)
        if stm:
            stm.plan = plan
            self.update(execution_id, {"plan": plan})

    def add_step_result(self, execution_id: str, step_id: int, result: Dict[str, Any]):
        stm = self.read(execution_id)
        if stm:
            stm.step_results[step_id] = result
            if step_id not in stm.completed_step_ids:
                stm.completed_step_ids.append(step_id)
            self.update(execution_id, {
                "step_results": stm.step_results,
                "completed_step_ids": stm.completed_step_ids
            })

    def add_finding(self, execution_id: str, finding: Dict[str, Any]):
        stm = self.read(execution_id)
        if stm:
            stm.current_findings.append(finding)
            self.update(execution_id, {"current_findings": stm.current_findings})

    def update_execution_context(self, execution_id: str, context: Dict[str, Any]):
        stm = self.read(execution_id)
        if stm:
            stm.current_execution_context.update(context)
            self.update(execution_id, {"current_execution_context": stm.current_execution_context})

# Example usage (for testing purposes)
if __name__ == "__main__":
    stm = ShortTermMemory()
    execution_id = "test-execution-001"
    stm.create(execution_id, "Which customers had the same login issue as ticket 4021?")
    print("STM created:", stm.read(execution_id))
    stm.add_plan(execution_id, {"plan_id": "PLAN-001", "steps": []})
    print("After adding plan:", stm.read(execution_id))