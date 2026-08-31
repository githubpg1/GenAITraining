#!/usr/bin/env python
"""
Submit a new customer support ticket and run the Planner and Executor agents.

Usage:
    python submit_ticket.py --ticket "App keeps logging me out."
    or
    python submit_ticket.py   (uses a default example ticket)
"""

import sys
import os
from pathlib import Path

# Add the project root to the sys.path so we can import the planner and executor can be imported
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from planner_agent import plan_and_create
import executor_agent  # we will call its main after adjusting sys.argv

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Submit a customer support ticket and run the RAG pipeline.")
    parser.add_argument("--ticket", type=str, help="The customer support ticket text.")
    args = parser.parse_args()

    if args.ticket:
        query = args.ticket
    else:
        # Default example from the requirements
        query = "App keeps logging me out."

    print(f"[Submit] Received query: {query}")

    # Step 1: Run the Planner to create the Query folder
    query_folder = plan_and_create(query)
    print(f"[Submit] Planner created query folder: {query_folder}")

    # Step 2: Run the Executor on that folder
    # The executor_agent.main() expects sys.argv[1] to be the path to the query folder.
    old_sys_argv = sys.argv
    sys.argv = [sys.argv[0], str(query_folder)]
    try:
        executor_agent.main()
    finally:
        sys.argv = old_sys_argv

    print(f"[Submit] Execution completed. Check the query folder for results: {query_folder}")

if __name__ == "__main__":
    main()
"""
Submit a new customer support ticket and run the Planner and Executor agents.

Usage:
    python submit_ticket.py --ticket "App keeps logging me out."
    or
    python submit_ticket.py   (uses a default example ticket)
"""

import sys
import os
from pathlib import Path

# Add the project root to the sys.path so we can import the agents
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from planner_agent import plan_and_create
from executor_agent import main as executor_main

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Submit a customer support ticket and run the RAG pipeline.")
    parser.add_argument("--ticket", type=str, help="The customer support ticket text.")
    args = parser.parse_args()

    if args.ticket:
        query = args.ticket
    else:
        # Default example from the requirements
        query = "App keeps logging me out."

    print(f"[Submit] Received query: {query}")

    # Step 1: Run the Planner to create the Query folder
    query_folder = plan_and_create(query)
    print(f"[Submit] Planner created query folder: {query_folder}")

    # Step 2: Run the Executor on that folder
    # We'll call the executor_agent's main function but we need to pass the query folder as an argument.
    # Since executor_agent.py expects sys.argv[1], we can temporarily modify sys.argv.
    old_sys_argv = sys.argv
    sys.argv = [sys.argv[0], str(query_folder)]
    try:
        executor_main()
    finally:
        sys.argv = old_sys_argv

    print(f"[Submit] Execution completed. Check the query folder for results: {query_folder}")

if __name__ == "__main__":
    main()