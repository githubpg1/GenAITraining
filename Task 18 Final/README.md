# Ticket Intelligence System

This is the implementation of Problem 18: Ticket Intelligence System with Multi-Hop Reasoning, Jira MCP, Multi-Model Agents, and ChromaDB Memory.

## Overview

The system is designed to answer compound questions about historical support tickets and take appropriate actions based on validated findings. It uses a multi-agent architecture with distinct roles for planning, execution, and Jira actions, and integrates with Jira via MCP for task management and ticket creation.

## Features

- Multi-hop reasoning to break down complex queries into executable steps.
- Three distinct memory layers: Short-Term, Working, and Long-Term (using ChromaDB).
- Multi-agent architecture with independently configurable models.
- Jira MCP integration for runtime task management and business ticket creation.
- Action gate to prevent duplicate Jira tickets and ensure evidence-based actions.
- Comprehensive logging and traceability.

## Project Structure

```
.
├── agents/
│   ├── atlas/          # Planner Agent
│   ├── scout/          # Executor Agent
│   └── jiraops/        # Jira Action Agent
├── orchestrator/       # Orchestrator to coordinate the execution
├── tools/              # Tool registry and implementations
├── mcp/                # Jira MCP client and server
├── memory/             # Memory management (ChromaDB-backed)
├── schemas/            # Pydantic schemas for data validation
├── prompts/            # Prompts for each agent
├── config/             # Configuration files (models, settings)
├── Plan/               # Directory for runtime plan artifacts
├── tests/              # Unit and integration tests
├── logs/               # Execution logs
├── main.py             # Entry point of the application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── README.md
```

## Installation

1. Clone the repository (or copy the files to your local machine).
2. Create a virtual environment and activate it.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in the required values (LLM API key, Jira credentials, etc.).
5. Ensure you have a running instance of ChromaDB (the system will use a local directory by default) and a Jira instance (or the MCP server will simulate one for testing).

## Usage

Run the main script:
```bash
python main.py
```

The system will process the example query defined in `main.py` and output the result.

## Configuration

- `config/models.yaml`: Configure the models used by each agent (planner, executor, jiraops, embedding).
- `config/settings.yaml`: Configure ChromaDB paths, memory settings, Jira settings, action gate, etc.

## Testing

Run the tests (to be implemented) with:
```bash
pytest tests/
```

## Notes

This is a placeholder implementation meant to demonstrate the structure and flow. The actual logic for LLM calls, tool executions, and Jira interactions needs to be implemented in the respective components.

## License

This project is proprietary and confidential.