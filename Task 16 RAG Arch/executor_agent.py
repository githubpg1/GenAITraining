#!/usr/bin/env python
"""
Executor Agent for Task 16 RAG Arch.

Responsibilities:
- Read a Query folder created by the Planner.
- Load the state file.
- Execute tasks in the order of their task numbers (assuming linear dependencies).
- For each task, mark it as COMPLETED and optionally create a dummy output file.
- After all tasks, verify final output and mark overall status.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python executor_agent.py <path_to_query_folder>")
        sys.exit(1)

    query_folder = Path(sys.argv[1])
    if not query_folder.is_dir():
        print(f"Error: Query folder does not exist: {query_folder}")
        sys.exit(1)

    state_path = query_folder / "state.json"
    log_path = query_folder / "execution.log"

    def log(message: str):
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
        print(message)

    # Load state
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except Exception as e:
        print(f"Error loading state: {e}")
        sys.exit(1)

    # Get all task files and sort by task number
    task_files = list(query_folder.glob("Task_*.txt"))
    def task_number(task_path):
        # Extract the number from the filename: Task_XX_*.txt
        try:
            return int(task_path.name.split('_')[1])
        except:
            return 0
    task_files.sort(key=task_number)

    # Process each task in order
    for task_path in task_files:
        # Derive task_id from filename: e.g., Task_01_Initialize_Query_Folder.txt -> Task_01_Initialize_Query_Folder
        # Remove the .txt extension and keep the rest.
        task_id = task_path.name[:-4]  # remove '.txt'
        current_state = state.get("tasks", {}).get(task_id, "UNKNOWN")

        if current_state != "PENDING":
            print(f"[Executor] Skipping {task_id} (state: {current_state})")
            log(f"Skipping {task_id} (state: {current_state})")
            continue

        print(f"[Executor] Executing {task_id}")
        log(f"Starting {task_id}")

        # Mark as IN_PROGRESS
        state["tasks"][task_id] = "IN_PROGRESS"
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        log(f"Set {task_id} to IN_PROGRESS")

        # Simulate tool execution: mark as COMPLETED and optionally create a dummy output file
        try:
            # We could parse the task file to get ARTIFACT_LOCATION, but for now we skip.
            # If we wanted to, we could look for a line that starts with "ARTIFACT_LOCATION:" and take the value.
            # For simplicity, we'll just mark as COMPLETED without creating dummy files.
            # If we want to create dummy files, we can do it here.

            # Mark task as COMPLETED
            state["tasks"][task_id] = "COMPLETED"
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            log(f"Set {task_id} to COMPLETED")
        except Exception as e:
            print(f"[Executor] Error executing task {task_id}: {e}")
            log(f"Error executing task {task_id}: {e}")
            state["tasks"][task_id] = "FAILED"
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)

    # After processing all tasks, determine overall status
    all_tasks = state.get("tasks", {})
    if not all_tasks:
        overall_status = "FAILED"
    else:
        if all(status == "COMPLETED" for status in all_tasks.values()):
            overall_status = "COMPLETED"
        elif any(status == "FAILED" for status in all_tasks.values()):
            overall_status = "FAILED"
        else:
            overall_status = "PARTIAL"  # some tasks may still be PENDING or IN_PROGRESS

    state["overall_status"] = overall_status
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)
    print(f"[Executor] Execution finished. Overall status: {overall_status}")
    log(f"Execution finished. Overall status: {overall_status}")

if __name__ == "__main__":
    main()