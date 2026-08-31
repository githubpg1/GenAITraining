# Working Memory component for the Ticket Intelligence System
# Holds the intermediate state of the currently executing step.

from typing import Dict, Any, Optional
from memory.chroma_manager import ChromaManager
from memory.schemas import WorkingMemoryEntry
import json
from config.settings import settings

class WorkingMemory:
    def __init__(self, chroma_manager: ChromaManager = None):
        self.chroma = chroma_manager or ChromaManager()

    def create(self, execution_id: str, step_id: int):
        """
        Initialize working memory for a step.
        """
        entry = WorkingMemoryEntry(
            execution_id=execution_id,
            step_id=step_id,
            attempt_number=1,
            tool_inputs={},
            partial_retrievals=[],
            temporary_candidates=[],
            retry_information={},
            temporary_validation_state={}
        )
        self.chroma.wm_add(execution_id, step_id, entry)

    def read(self, execution_id: str, step_id: int) -> Optional[WorkingMemoryEntry]:
        """
        Read the working memory for a specific step in an execution.
        """
        return self.chroma.wm_get(execution_id, step_id)

    def update(self, execution_id: str, step_id: int, updates: Dict[str, Any]):
        """
        Update the working memory for a step.
        """
        self.chroma.wm_update(execution_id, step_id, updates)

    def clear(self, execution_id: str, step_id: int):
        """
        Clear the working memory for a step after it completes.
        """
        self.chroma.wm_clear(execution_id, step_id)

    # Helper methods for specific WM operations
    def set_tool_inputs(self, execution_id: str, step_id: int, inputs: Dict[str, Any]):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.tool_inputs = inputs
            self.update(execution_id, step_id, {"tool_inputs": inputs})

    def add_partial_retrieval(self, execution_id: str, step_id: int, retrieval: Any):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.partial_retrievals.append(retrieval)
            self.update(execution_id, step_id, {"partial_retrievals": wm.partial_retrievals})

    def add_temporary_candidate(self, execution_id: str, step_id: int, candidate: Any):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.temporary_candidates.append(candidate)
            self.update(execution_id, step_id, {"temporary_candidates": wm.temporary_candidates})

    def set_retry_information(self, execution_id: str, step_id: int, retry_info: Dict[str, Any]):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.retry_information = retry_info
            self.update(execution_id, step_id, {"retry_information": retry_info})

    def set_temporary_validation_state(self, execution_id: str, step_id: int, validation_state: Dict[str, Any]):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.temporary_validation_state = validation_state
            self.update(execution_id, step_id, {"temporary_validation_state": validation_state})

    def increment_attempt(self, execution_id: str, step_id: int):
        wm = self.read(execution_id, step_id)
        if wm:
            wm.attempt_number += 1
            self.update(execution_id, step_id, {"attempt_number": wm.attempt_number})

# Example usage (for testing purposes)
if __name__ == "__main__":
    wm = WorkingMemory()
    execution_id = "test-execution-001"
    step_id = 1
    wm.create(execution_id, step_id)
    print("WM created:", wm.read(execution_id, step_id))
    wm.set_tool_inputs(execution_id, step_id, {"ticket_id": "4021"})
    print("After setting tool inputs:", wm.read(execution_id, step_id))