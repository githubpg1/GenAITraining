#!/usr/bin/env python
"""
Planner Agent for Task 16 RAG Arch.

Responsibilities:
- Accept a new customer support ticket (Query).
- Create a unique runtime Query folder under Plan/.
- Read the static specification to understand planning rules.
- Dynamically decide which tasks are needed.
- Dynamically create/provision required tools (record in tools.json).
- Generate task files (Task_01_*.txt, ...) inside the Query folder.
- Write initial state.json with all tasks set to PENDING.
"""

import os
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# TODO: Import utility functions if needed
# from .planner_utils import sanitize_folder_name, load_spec, etc.

PLAN_ROOT = Path(__file__).parent / "Plan"
SPEC_PATH = PLAN_ROOT / "RUNTIME_EXECUTOR_PLAN_SPECIFICATION.txt"


def sanitize_folder_name(query: str) -> str:
    """Convert query to a filesystem-safe folder name."""
    # Remove problematic characters, replace spaces with underscores, limit length
    safe = re.sub(r'[^\w\s-]', '', query).strip().lower()
    safe = re.sub(r'[-\s]+', '_', safe)
    # Add timestamp and optional UUID to ensure uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{safe}_{unique_id}"[:100]  # limit length


def load_spec() -> str:
    """Load the static specification text."""
    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def determine_required_capabilities(query: str, spec: str) -> List[str]:
    """
    Determine which logical capabilities are needed for this query.
    For MVP, we return a fixed set; later can add branching logic.
    """
    # Base capabilities always needed
    base_caps = [
        "query_folder_manager",
        "task_file_writer",
        "runtime_state_store",
        "execution_log_writer",
        "environment_config_loader",
        "secret_validator",
        "corpus_inspector",
        "metadata_validator",
        "ticket_query_analyzer",
        "gpt_query_normalizer",
        "embedding_service",
        "chroma_vector_store",
        "candidate_result_processor",
        "search_result_formatter",
        "acceptance_evaluator",
        # recovery_task_generator is created on demand
    ]
    # TODO: Add logic for optional branches (metadata filter, re-ranking, etc.)
    return base_caps


def ensure_tool_manifest(query_folder: Path, capabilities: List[str]) -> Path:
    """
    Create or update tools.json in the query folder with definitions for each capability.
    Returns path to tools.json.
    """
    manifest_path = query_folder / "tools.json"
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = {"tools": {}, "version": "1.0"}

    for cap in capabilities:
        if cap not in manifest["tools"]:
            # Minimal tool definition; actual implementation details are filled by the tool itself
            manifest["tools"][cap] = {
                "tool_id": cap,
                "name": cap.replace("_", " ").title(),
                "purpose": f"Capability for {cap}",
                "implementation": f"tools.{cap}",  # placeholder
                "config_ref": "model_config.yaml",
                "dependencies": [],
                "version": "1.0.0",
                "status": "ready"
            }
    # Write back
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    return manifest_path


def generate_task_file(query_folder: Path, task_id: int, task_name: str,
                       objective: str, input_ctx: str, primary_tool: str,
                       action: str, expected_output: str, artifact_location: str,
                       validation: str, failure_condition: str,
                       recovery_next_action: str,
                       task_deps: List[str], tool_deps: List[str]) -> Path:
    """
    Create a single Task_<id>_<name>.txt file.
    """
    filename = f"Task_{task_id:02d}_{task_name.replace(' ', '_')}.txt"
    filepath = query_folder / filename
    content = f"""TASK_ID: {task_id}
TASK_NAME: {task_name}

OBJECTIVE:
{objective}

INPUT:
{input_ctx}

PRIMARY_TOOL:
{primary_tool}

TOOL_VERSION:
latest  # resolved from tools.json at runtime

ACTION:
{action}

EXPECTED_OUTPUT:
{expected_output}

ARTIFACT_LOCATION:
{artifact_location}

VALIDATION:
{validation}

FAILURE_CONDITION:
{failure_condition}

RECOVERY/NEXT_ACTION:
{recovery_next_action}

TASK_DEPENDENCIES:
{', '.join(task_deps) if task_deps else 'None'}

TOOL_DEPENDENCIES:
{', '.join(tool_deps) if tool_deps else 'None'}

STATE:
PENDING
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def plan_and_create(query: str) -> Path:
    """
    Main entry point: create plan for the given query.
    Returns the path to the created Query folder.
    """
    # 1. Sanitize and create folder
    folder_name = sanitize_folder_name(query)
    query_folder = PLAN_ROOT / folder_name
    query_folder.mkdir(parents=True, exist_ok=False)
    print(f"[Planner] Created Query folder: {query_folder}")

    # 2. Load spec (for logging/validation)
    spec = load_spec()
    # In a real implementation, we would parse the spec for rules.
    # For now, we just note that we loaded it.
    print("[Planner] Loaded specification.")

    # 3. Determine required capabilities
    capabilities = determine_required_capabilities(query, spec)
    print(f"[Planner] Required capabilities: {capabilities}")

    # 4. Ensure tool manifest
    manifest_path = ensure_tool_manifest(query_folder, capabilities)
    print(f"[Planner] Tool manifest ready at: {manifest_path}")

    # 5. Generate task files (example set; in reality, order and number may vary)
    # We'll create a simple linear chain for demonstration.
    tasks = [
        {
            "id": 1,
            "name": "Initialize_Query_Folder",
            "objective": "Create and validate the unique Query folder.",
            "input_ctx": f"Query: {query}",
            "primary_tool": "query_folder_manager",
            "action": "Validate folder exists and is writable.",
            "expected_output": "Folder path confirmed.",
            "artifact_location": "N/A",
            "validation": "Folder exists and is accessible.",
            "failure_condition": "Folder creation failed or not accessible.",
            "recovery_next_action": "Abort and signal failure.",
            "task_deps": [],
            "tool_deps": []
        },
        {
            "id": 2,
            "name": "Load_Environment_Config",
            "objective": "Load environment variables and model configuration.",
            "input_ctx": "Paths to .env and model_config.yaml",
            "primary_tool": "environment_config_loader",
            "action": "Read .env, load model_config.yaml, validate required fields.",
            "expected_output": "Configuration object.",
            "artifact_location": "config.json (in query folder)",
            "validation": "All required config present.",
            "failure_condition": "Missing API key or model config.",
            "recovery_next_action": "Abort with clear error message.",
            "task_deps": ["Task_01_Initialize_Query_Folder"],
            "tool_deps": ["environment_config_loader"]
        },
        {
            "id": 3,
            "name": "Validate_Corpus",
            "objective": "Ensure historical ticket corpus is present and readable.",
            "input_ctx": "Path to historical_tickets folder",
            "primary_tool": "corpus_inspector",
            "action": "Check folder exists, count .txt files, basic sanity.",
            "expected_output": "Corpus validation report.",
            "artifact_location": "corpus_status.json",
            "validation": "At least one ticket file present.",
            "failure_condition": "No ticket files found.",
            "recovery_next_action": "Trigger ingestion recovery if supported.",
            "task_deps": ["Task_02_Load_Environment_Config"],
            "tool_deps": ["corpus_inspector"]
        },
        {
            "id": 4,
            "name": "Analyze_Query",
            "objective": "Extract issue, symptoms, entities from the customer query.",
            "input_ctx": "Raw query string",
            "primary_tool": "ticket_query_analyzer",
            "action": "Parse query into structured analysis.",
            "expected_output": "Query analysis JSON.",
            "artifact_location": "query_analysis.json",
            "validation": "Contains issue and symptoms fields.",
            "failure_condition": "Unable to extract meaningful components.",
            "recovery_next_action": "Use raw query as fallback.",
            "task_deps": ["Task_03_Validate_Corpus"],
            "tool_deps": ["ticket_query_analyzer"]
        },
        {
            "id": 5,
            "name": "Normalize_Query_With_GPT",
            "objective": "Use GPT-5.6 Luna to understand/normalize the query.",
            "input_ctx": "Query analysis from previous step",
            "primary_tool": "gpt_query_normalizer",
            "action": "Call LLM API with prompt to produce normalized search representation.",
            "expected_output": "Normalized query text.",
            "artifact_location": "normalized_query.txt",
            "validation": "Non-empty string, length > 0.",
            "failure_condition": "LLM API call failed or returned empty.",
            "recovery_next_action": "Fall back to raw query.",
            "task_deps": ["Task_04_Analyze_Query"],
            "tool_deps": ["gpt_query_normalizer"]
        },
        {
            "id": 6,
            "name": "Generate_Query_Embedding",
            "objective": "Convert normalized query to vector using embedding model.",
            "input_ctx": "Normalized query text",
            "primary_tool": "embedding_service",
            "action": "Embed the text using the configured embedding model.",
            "expected_output": "Embedding vector (list of floats).",
            "artifact_location": "query_embedding.json",
            "validation": "Vector of expected dimension, not all zeros.",
            "failure_condition": "Embedding generation failed.",
            "recovery_next_action": "Abort search.",
            "task_deps": ["Task_05_Normalize_Query_With_GPT"],
            "tool_deps": ["embedding_service"]
        },
        {
            "id": 7,
            "name": "Search_ChromaDB",
            "objective": "Query the persistent ChromaDB for similar historical chunks.",
            "input_ctx": "Query embedding vector",
            "primary_tool": "chroma_vector_store",
            "action": "Perform vector similarity search, retrieve top-K candidates.",
            "expected_output": "List of candidate chunks with metadata and scores.",
            "artifact_location": "raw_candidates.json",
            "validation": "Returns a list (may be empty).",
            "failure_condition": "ChromaDB query error or collection missing.",
            "recovery_next_action": "Signal failure; possibly trigger ingestion.",
            "task_deps": ["Task_06_Generate_Query_Embedding"],
            "tool_deps": ["chroma_vector_store"]
        },
        {
            "id": 8,
            "name": "Process_And_Rank_Results",
            "objective": "Filter, deduplicate by ticket ID, rank candidates.",
            "input_ctx": "Raw candidates from ChromaDB",
            "primary_tool": "candidate_result_processor",
            "action": "Apply relevance threshold, group by ticket_id, pick best chunk per ticket, sort by score.",
            "expected_output": "Ranked list of unique ticket results.",
            "artifact_location": "processed_results.json",
            "validation": "List length <= final_top_k and >= 0.",
            "failure_condition": "Processing error (e.g., invalid data).",
            "recovery_next_action": "Return empty list.",
            "task_deps": ["Task_07_Search_ChromaDB"],
            "tool_deps": ["candidate_result_processor"]
        },
        {
            "id": 9,
            "name": "Format_Final_Results",
            "objective": "Prepare final output with required fields.",
            "input_ctx": "Processed results",
            "primary_tool": "search_result_formatter",
            "action": "Format each result to include ticket_id, matching_text, score, resolution_status.",
            "expected_output": "Final results JSON or text.",
            "artifact_location": "final_results.json",
            "validation": "Contains required fields for each result.",
            "failure_condition": "Formatting failed.",
            "recovery_next_action": "Return empty results.",
            "task_deps": ["Task_08_Process_And_Rank_Results"],
            "tool_deps": ["search_result_formatter"]
        },
        {
            "id": 10,
            "name": "Evaluate_Acceptance",
            "objective": "Check if the mandatory paraphrase test passes (Recall@3).",
            "input_ctx": "Final results and known expected ticket ID (if available).",
            "primary_tool": "acceptance_evaluator",
            "action": "Determine if expected historical ticket is within Top 3.",
            "expected_output": "PASS/FAIL with details.",
            "artifact_location": "acceptance_result.json",
            "validation": "Boolean pass flag present.",
            "failure_condition": "Evaluation error.",
            "recovery_next_action": "Mark query as failed if acceptance is required and fails.",
            "task_deps": ["Task_09_Format_Final_Results"],
            "tool_deps": ["acceptance_evaluator"]
        }
    ]

    for task in tasks:
        generate_task_file(
            query_folder=query_folder,
            task_id=task["id"],
            task_name=task["name"],
            objective=task["objective"],
            input_ctx=task["input_ctx"],
            primary_tool=task["primary_tool"],
            action=task["action"],
            expected_output=task["expected_output"],
            artifact_location=task["artifact_location"],
            validation=task["validation"],
            failure_condition=task["failure_condition"],
            recovery_next_action=task["recovery_next_action"],
            task_deps=task["task_deps"],
            tool_deps=task["tool_deps"]
        )
        print(f"[Planner] Generated {task['name']} task file.")

    # 6. Write initial state file
    state_path = query_folder / "state.json"
    initial_state = {
        "query": query,
        "created_at": datetime.now().isoformat(),
        "tasks": {f"Task_{t['id']:02d}_{t['name'].replace(' ', '_')}": "PENDING" for t in tasks},
        "overall_status": "PENDING"
    }
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(initial_state, f, indent=2)
    print(f"[Planner] Initial state written to {state_path}")

    return query_folder


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query_input = " ".join(sys.argv[1:])
    else:
        # Example default for testing
        query_input = "App keeps logging me out."
    print(f"[Planner] Received query: {query_input}")
    folder = plan_and_create(query_input)
    print(f"[Planner] Planning complete. Query folder: {folder}")
    print("[Planner] Next step: run the Executor Agent on this folder.")