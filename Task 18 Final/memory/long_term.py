# Long-Term Memory component for the Ticket Intelligence System
# Persists validated business findings across sessions.

from typing import Dict, Any, Optional, List
from memory.chroma_manager import ChromaManager
from memory.schemas import LongTermMemoryEntry
import json
from config.settings import settings

class LongTermMemory:
    def __init__(self, chroma_manager: ChromaManager = None):
        self.chroma = chroma_manager or ChromaManager()

    def search(self, query_text: str, limit: int = None) -> List[LongTermMemoryEntry]:
        """
        Search long-term memory for entries matching the query.
        """
        return self.chroma.ltm_search(query_text, limit)

    def get(self, finding_id: str) -> Optional[LongTermMemoryEntry]:
        """
        Get a specific long-term memory entry by its ID.
        """
        return self.chroma.ltm_get(finding_id)

    def add(self, entry: LongTermMemoryEntry):
        """
        Add a new entry to long-term memory.
        """
        self.chroma.ltm_add(entry)

    def update(self, finding_id: str, updates: Dict[str, Any]):
        """
        Update an existing long-term memory entry.
        """
        self.chroma.ltm_update(finding_id, updates)

    def delete(self, finding_id: str):
        """
        Delete an entry from long-term memory.
        """
        self.chroma.ltm_delete(finding_id)

    def link_jira(self, finding_id: str, jira_key: str):
        """
        Link a long-term memory entry to a Jira issue key.
        """
        self.chroma.ltm_link_jira(finding_id, jira_key)

    # Helper methods for specific LTM operations
    def add_finding(self, customer_id: str, issue_category: str, finding_type: str,
                    source_tickets: List[str], confidence: float, jira_key: Optional[str] = None) -> str:
        """
        Create and add a new finding to long-term memory.
        Returns the finding_id of the new entry.
        """
        # Generate a deterministic finding ID based on customer_id, issue_category, and finding_type
        # We use SHA256 for a fixed-length ID, but we can use any deterministic method.
        import hashlib
        finding_string = f"{customer_id}|{issue_category}|{finding_type}"
        finding_id = hashlib.sha256(finding_string.encode()).hexdigest()

        # Check if we already have an entry with this ID (idempotency)
        existing = self.get(finding_id)
        if existing:
            # Update the existing entry with new information if needed
            # For example, we might update the source_tickets, confidence, last_seen, and jira_key
            updates = {
                "source_tickets": list(set(existing.source_tickets + source_tickets)),
                "confidence": max(existing.confidence, confidence),  # Take the higher confidence
                "last_seen": __import__('datetime').datetime.now(),
            }
            if jira_key:
                updates["jira_key"] = jira_key
            self.update(finding_id, updates)
            return finding_id

        # Create a new entry
        from datetime import datetime
        entry = LongTermMemoryEntry(
            finding_id=finding_id,
            customer_id=customer_id,
            issue_category=issue_category,
            finding_type=finding_type,
            source_tickets=source_tickets,
            confidence=confidence,
            jira_key=jira_key,
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            evidence_hash=""  # In a real system, we would compute a hash of the evidence
        )
        self.add(entry)
        return finding_id

    def get_related_finding(self, customer_id: str, issue_category: str, finding_type: str) -> Optional[LongTermMemoryEntry]:
        """
        Get a related finding from long-term memory based on customer_id, issue_category, and finding_type.
        This uses the deterministic ID to look up the exact finding.
        """
        import hashlib
        finding_string = f"{customer_id}|{issue_category}|{finding_type}"
        finding_id = hashlib.sha256(finding_string.encode()).hexdigest()
        return self.get(finding_id)

# Example usage (for testing purposes)
if __name__ == "__main__":
    ltm = LongTermMemory()
    # Add a finding
    finding_id = ltm.add_finding(
        customer_id="CUST-1001",
        issue_category="Login Failure",
        finding_type="CHURN_AFTER_ISSUE",
        source_tickets=["4021", "4031"],
        confidence=0.94,
        jira_key="SUP-1001"
    )
    print(f"Added finding with ID: {finding_id}")
    # Retrieve the finding
    finding = ltm.get(finding_id)
    print(f"Retrieved finding: {finding}")
    # Check for a related finding
    related = ltm.get_related_finding("CUST-1001", "Login Failure", "CHURN_AFTER_ISSUE")
    print(f"Related finding: {related}")