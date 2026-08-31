"""
Base class for all tools in the Task 16 RAG Arch system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import json
import os
from pathlib import Path


class BaseTool(ABC):
    """
    Abstract base class for a tool.
    Each tool must implement the execute method.
    """

    def __init__(self, tool_id: str, config: Dict[str, Any]):
        """
        Initialize the tool.

        :param tool_id: The identifier of the tool (matches the key in tools.json)
        :param config: The configuration dictionary for this tool (from manifest and environment)
        """
        self.tool_id = tool_id
        self.config = config

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool's action.

        :param inputs: A dictionary of input data (from previous tasks or context)
        :return: A dictionary of output data to be passed to the next task
        """
        pass

    def _write_json(self, data: Dict[str, Any], filepath: Path):
        """Write data as JSON to the given filepath."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _read_json(self, filepath: Path) -> Dict[str, Any]:
        """Read JSON data from the given filepath."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)