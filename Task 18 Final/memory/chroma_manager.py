# ChromaDB Manager for the Ticket Intelligence System
# Manages ChromaDB client and collections for different memory layers.

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb
from typing import List, Dict, Any, Optional
from memory.schemas import ShortTermMemoryEntry, WorkingMemoryEntry, LongTermMemoryEntry
import json
import hashlib
from config.settings import settings

class ChromaManager:
    def __init__(self, path: str = None):
        self.path = path or settings.chroma_db_path
        self.client = chromadb.PersistentClient(path=self.path)
        self.collections = {}
        self._initialize_collections()

    def _initialize_collections(self):
        # Initialize or get the collections for each memory layer
        collection_names = [
            settings.ticket_chunks_collection,
            settings.short_term_memory_collection,
            settings.working_memory_collection,
            settings.long_term_memory_collection
        ]
        for name in collection_names:
            self.collections[name] = self.client.get_or_create_collection(name)

    def add_ticket_chunk(self, ticket_id: str, document: str, metadata: Dict[str, Any]):
        """
        Add a ticket chunk to the ticket_chunks collection.
        """
        collection = self.collections[settings.ticket_chunks_collection]
        # Generate a unique ID for the chunk
        chunk_id = f"{ticket_id}_{hashlib.md5(document.encode()).hexdigest()}"
        collection.add(
            ids=[chunk_id],
            documents=[document],
            metadatas=[metadata]
        )

    def query_ticket_chunks(self, query_text: str, n_results: int = None) -> Dict[str, Any]:
        """
        Query the ticket_chunks collection for similar tickets.
        """
        n_results = n_results or settings.top_k
        collection = self.collections[settings.ticket_chunks_collection]
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    # Short-Term Memory methods
    def stm_add(self, execution_id: str, entry: ShortTermMemoryEntry):
        collection = self.collections[settings.short_term_memory_collection]
        # We use the execution_id as the ID for the STM entry
        collection.add(
            ids=[execution_id],
            documents=[json.dumps(entry.dict())],
            metadatas=[{"execution_id": execution_id, "type": "short_term"}]
        )

    def stm_get(self, execution_id: str) -> Optional[ShortTermMemoryEntry]:
        collection = self.collections[settings.short_term_memory_collection]
        results = collection.get(ids=[execution_id])
        if results and results['documents']:
            entry_dict = json.loads(results['documents'][0])
            return ShortTermMemoryEntry(**entry_dict)
        return None

    def stm_update(self, execution_id: str, updates: Dict[str, Any]):
        # In ChromaDB, updating is done by deleting and adding, or we can use the update method if available.
        # For simplicity, we'll delete and add.
        self.stm_delete(execution_id)
        entry = self.stm_get(execution_id)
        if entry:
            # Update the entry with the new data
            for key, value in updates.items():
                setattr(entry, key, value)
        else:
            # If there's no existing entry, we create a new one? But STM should exist.
            # We'll just create a minimal entry for safety.
            entry = ShortTermMemoryEntry(
                execution_id=execution_id,
                query=updates.get("query", ""),
                plan=updates.get("plan", {}),
                completed_step_ids=updates.get("completed_step_ids", []),
                step_results=updates.get("step_results", {}),
                current_findings=updates.get("current_findings", []),
                current_execution_context=updates.get("current_execution_context", {})
            )
        self.stm_add(execution_id, entry)

    def stm_delete(self, execution_id: str):
        collection = self.collections[settings.short_term_memory_collection]
        collection.delete(ids=[execution_id])

    def stm_finalize(self, execution_id: str):
        # In a real system, we might move STM to LTM or archive it.
        # For now, we just delete it after the execution is over? But the requirement says STM is for one run.
        # We'll delete it when the execution is complete (as per the orchestrator).
        self.stm_delete(execution_id)

    # Working Memory methods
    def wm_add(self, execution_id: str, step_id: int, entry: WorkingMemoryEntry):
        collection = self.collections[settings.working_memory_collection]
        # Use a composite ID for working memory: execution_id + step_id
        wm_id = f"{execution_id}_{step_id}"
        collection.add(
            ids=[wm_id],
            documents=[json.dumps(entry.dict())],
            metadatas=[{"execution_id": execution_id, "step_id": step_id, "type": "working"}]
        )

    def wm_get(self, execution_id: str, step_id: int) -> Optional[WorkingMemoryEntry]:
        collection = self.collections[settings.working_memory_collection]
        wm_id = f"{execution_id}_{step_id}"
        results = collection.get(ids=[wm_id])
        if results and results['documents']:
            entry_dict = json.loads(results['documents'][0])
            return WorkingMemoryEntry(**entry_dict)
        return None

    def wm_update(self, execution_id: str, step_id: int, updates: Dict[str, Any]):
        wm_id = f"{execution_id}_{step_id}"
        self.wm_delete(execution_id, step_id)
        entry = self.wm_get(execution_id, step_id)
        if entry:
            for key, value in updates.items():
                setattr(entry, key, value)
        else:
            entry = WorkingMemoryEntry(
                execution_id=execution_id,
                step_id=step_id,
                attempt_number=updates.get("attempt_number", 1),
                tool_inputs=updates.get("tool_inputs", {}),
                partial_retrievals=updates.get("partial_retrievals", []),
                temporary_candidates=updates.get("temporary_candidates", []),
                retry_information=updates.get("retry_information", {}),
                temporary_validation_state=updates.get("temporary_validation_state", {})
            )
        self.wm_add(execution_id, step_id, entry)

    def wm_clear(self, execution_id: str, step_id: int):
        wm_id = f"{execution_id}_{step_id}"
        collection = self.collections[settings.working_memory_collection]
        collection.delete(ids=[wm_id])

    # Long-Term Memory methods
    def ltm_add(self, entry: LongTermMemoryEntry):
        collection = self.collections[settings.long_term_memory_collection]
        # Use the finding_id as the ID for the LTM entry
        collection.add(
            ids=[entry.finding_id],
            documents=[json.dumps(entry.dict())],
            metadatas=[{"finding_id": entry.finding_id, "type": "long_term"}]
        )

    def ltm_get(self, finding_id: str) -> Optional[LongTermMemoryEntry]:
        collection = self.collections[settings.long_term_memory_collection]
        results = collection.get(ids=[finding_id])
        if results and results['documents']:
            entry_dict = json.loads(results['documents'][0])
            return LongTermMemoryEntry(**entry_dict)
        return None

    def ltm_search(self, query_text: str, n_results: int = None) -> List[LongTermMemoryEntry]:
        collection = self.collections[settings.long_term_memory_collection]
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results or settings.top_k
        )
        entries = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                entry_dict = json.loads(doc)
                entries.append(LongTermMemoryEntry(**entry_dict))
        return entries

    def ltm_update(self, finding_id: str, updates: Dict[str, Any]):
        entry = self.ltm_get(finding_id)
        if entry:
            for key, value in updates.items():
                setattr(entry, key, value)
            # In ChromaDB, we update by deleting and adding
            self.ltm_delete(finding_id)
            self.ltm_add(entry)

    def ltm_delete(self, finding_id: str):
        collection = self.collections[settings.long_term_memory_collection]
        collection.delete(ids=[finding_id])

    def ltm_link_jira(self, finding_id: str, jira_key: str):
        entry = self.ltm_get(finding_id)
        if entry:
            entry.jira_key = jira_key
            self.ltm_update(finding_id, entry.dict())

# Example usage (for testing purposes)
if __name__ == "__main__":
    # This is just a simple test to see if the ChromaManager can be instantiated.
    # In a real test, we would use a temporary directory.
    try:
        manager = ChromaManager(path="./test_chroma_db")
        print("ChromaManager initialized successfully.")
        # We would then test adding and retrieving data.
    except Exception as e:
        print(f"Failed to initialize ChromaManager: {e}")