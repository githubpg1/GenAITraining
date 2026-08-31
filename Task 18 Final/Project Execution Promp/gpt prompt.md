# Problem 18 — Master Implementation Prompt

## Ticket Intelligence System
**Multi-Hop Reasoning + Jira MCP + Multi-Model Agents + ChromaDB Memory + Runtime Jira Task Orchestration**

### Role

You are a senior Agentic AI Engineer, AI Systems Architect, Python Engineer, Prompt Engineer, RAG Engineer, MCP Engineer, and Test Automation Engineer.

Your responsibility is to design and implement the complete Problem 18 system described below.

Build a **working, executable, testable, modular project**. Do not provide only conceptual code, pseudo-code, placeholders, TODO comments, or architectural suggestions.

---

## 1. Mandatory First Step — Read the Existing Project

Before writing or modifying **any** source code:

1. Inspect the complete project directory.
2. Locate the Problem 18 requirement/problem statement.
3. Locate the existing Problem 18 execution plan.
4. Locate the Goal → Task → Subtask definitions.
5. Locate the existing Planner Agent.
6. Locate the existing Executor Agent.
7. Locate the existing tool registry.
8. Locate the existing ChromaDB implementation.
9. Locate the 100-ticket Excel dataset.
10. Locate configuration files.
11. Locate `.env` / `.env.example`.
12. Locate existing prompts.
13. Locate existing tests.
14. Locate existing Jira/MCP implementation, if any.

Do not assume the project structure. Do not overwrite existing functionality blindly.

Create `PROJECT_ANALYSIS.md` containing:

- Existing project structure
- Existing components
- Existing agents
- Existing tools
- Existing prompts
- Existing data
- Existing ChromaDB implementation
- Existing model configuration
- Existing Jira/MCP implementation
- Existing tests
- Reusable components
- Components requiring modification
- Components requiring creation
- Potential conflicts
- Migration requirements

---

## 2. Requirement Reconciliation

Read all available project documentation and reconcile differences.

Problem 18 takes precedence over older requirements where it explicitly extends or changes them.

Do not delete useful earlier functionality.

The architecture must evolve from:

```text
semantic retrieval
```

to:

```text
multi-hop reasoning
+
runtime task orchestration
+
Jira task management
+
Jira MCP
+
multi-agent execution
+
multi-model routing
+
ChromaDB memory
+
long-term deduplication
+
auditability
```

---

## 3. Primary Business Objective

Build a Ticket Intelligence System capable of answering compound questions about historical support tickets and taking appropriate actions based on validated findings.

Example:

> Which customers had the same login issue as ticket 4021, and did any of them churn afterward?

The system must:

1. Understand the user query.
2. Determine required information.
3. Generate a dynamic multi-step execution plan.
4. Create Jira tasks representing executable plan steps.
5. Execute those tasks through the Executor Agent.
6. Use historical ticket data and semantic search.
7. Use ChromaDB for retrieval and memory.
8. Maintain Short-Term Memory.
9. Maintain Working Memory.
10. Maintain Long-Term Memory.
11. Determine whether findings are new or previously known.
12. Search Jira before creating duplicates.
13. Create/update Jira issues through Jira MCP.
14. Update runtime Jira task status during execution.
15. Add each task's Executor output as a JSON-formatted Jira comment.
16. Make dependent tasks consume previous task JSON output.
17. Never fabricate unavailable information.
18. Prevent duplicate business Jira tickets.
19. Provide a final result after successful execution.
20. Provide complete execution traceability.

---

## 4. Required Agent Architecture

### Agent 1 — ATLAS — Planner Agent

Responsibilities:

- Understand user query.
- Identify entities.
- Identify required information.
- Decompose compound questions.
- Select runtime tasks.
- Determine task dependencies.
- Select tools.
- Identify possible side effects.
- Define expected outputs.
- Define success/failure criteria.
- Produce structured execution plan.

ATLAS must not:

- Create business Jira issues.
- Update business Jira issues.
- Execute arbitrary tools.
- Invent data.
- Bypass action governance.

**Model:** strongest configured reasoning model.

The model must be externally configurable and never hardcoded in source code.

### Agent 2 — SCOUT — Executor Agent

Responsibilities:

- Execute exactly the runtime task assigned by the Orchestrator.
- Read task instructions.
- Resolve task inputs.
- Read previous task JSON output.
- Invoke authorized tools.
- Validate results.
- Perform relevance grading where required.
- Retry recoverable failures.
- Produce structured JSON output.
- Update the runtime Jira task status.
- Add JSON output as Jira comment through MCP.
- Make output available to subsequent tasks.

SCOUT must not:

- Redesign the plan.
- Invent business steps.
- Fabricate missing information.
- Create arbitrary business tasks.
- Directly call Jira REST APIs.
- Bypass Jira MCP.
- Execute tools not explicitly authorized for the task.
- Create business Jira issues independently of JiraOps/action governance.

**Model:** smaller/cheaper configured model.

### Agent 3 — JIRAOPS — Jira Action Agent

Responsibilities:

- Convert validated actionable findings into Jira actions.
- Search existing Jira issues.
- Determine `CREATE / UPDATE / SKIP`.
- Prepare Jira payloads.
- Invoke Jira MCP tools.
- Return structured Jira action results.

**Model:** lightweight configured model.

JIRAOPS must not:

- Directly access Jira REST APIs.
- Act without evidence.
- Create duplicate Jira issues.
- Treat missing information as known information.

### Component 4 — ORCHESTRATOR

Prefer deterministic application code rather than another LLM agent.

Responsibilities:

- Accept runtime input.
- Start execution.
- Initialize memory.
- Invoke Atlas.
- Validate plan.
- Create Jira runtime tasks.
- Resolve dependencies.
- Invoke Scout.
- Pass structured prior outputs to dependent tasks.
- Manage memory lifecycle.
- Invoke JiraOps when actionable findings appear.
- Persist final results.
- Generate final user response.

---

## 5. Model Configuration

Never hardcode model names.

Create:

```text
config/models.yaml
```

Example:

```yaml
planner:
  provider: openai
  model: <configured-value>
  temperature: 0

executor:
  provider: openai
  model: <configured-value>
  temperature: 0

jiraops:
  provider: openai
  model: <configured-value>
  temperature: 0

embedding:
  provider: <configured-provider>
  model: <configured-embedding-model>
```

Changing any model must not require source-code modification.

Also create:

```text
config/settings.yaml
```

for:

- ChromaDB path
- collection names
- top_k
- similarity threshold
- confidence threshold
- maximum retries
- retry backoff
- Jira project key
- Jira runtime task issue type
- Jira business issue type
- labels
- memory settings
- runtime plan directory
- Jira status mapping
- action-gate configuration

---

## 6. Secret Management

Use `.env` for secrets:

```text
LLM_API_KEY=
JIRA_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=
```

Adapt variable names to the selected provider if necessary.

Never put secrets in source code, prompts, task files, Jira comments, ChromaDB, logs, JSON outputs, Git, or README files.

Create/update `.env.example` and ensure `.env` is gitignored.

---

## 7. Project Structure

Adapt the following to the existing project:

```text
problem18/
├── agents/
│   ├── atlas/
│   │   ├── agent.py
│   │   ├── prompt.py
│   │   └── schemas.py
│   ├── scout/
│   │   ├── agent.py
│   │   ├── prompt.py
│   │   └── schemas.py
│   └── jiraops/
│       ├── agent.py
│       ├── prompt.py
│       └── schemas.py
├── orchestrator/
│   ├── orchestrator.py
│   ├── dependency_engine.py
│   └── lifecycle.py
├── tools/
│   ├── registry.py
│   ├── ticket_tools.py
│   ├── search_tools.py
│   ├── memory_tools.py
│   ├── validation_tools.py
│   └── runtime_tools.py
├── mcp/
│   ├── client/
│   │   └── jira_mcp_client.py
│   └── server/
│       └── jira_mcp_server.py
├── memory/
│   ├── chroma_manager.py
│   ├── short_term.py
│   ├── working.py
│   ├── long_term.py
│   └── schemas.py
├── data/
├── schemas/
├── prompts/
├── config/
├── Plan/
├── tests/
├── logs/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 8. ChromaDB Requirement

ChromaDB is required.

Use separate logical collections:

```text
problem18_ticket_chunks
problem18_short_term_memory
problem18_working_memory
problem18_long_term_memory
```

Do not implement one generic memory blob.

---

## 9. Ticket Collection

Each ticket/chunk should contain:

```text
id
document
metadata
```

Metadata:

```text
ticket_id
customer_id
customer_name
issue_category
status
priority
channel
resolution
churned_after_issue
churn_date
existing_jira_key
created_date
source_file
chunk_index
```

Use the configured embedding model for both document and query embeddings.

---

## 10. Three-Layer Memory

### Short-Term Memory

Current execution/run.

Store:

```text
run_id
query
plan
completed_step_ids
step_results
current findings
current execution context
```

It survives between steps of the same run but is not automatically permanent.

### Working Memory

Current step only.

Key:

```text
run_id + step_id
```

Store:

```text
attempt number
tool inputs
partial retrievals
temporary candidates
retry information
temporary validation state
```

Clear it when the step reaches:

```text
COMPLETED
FAILED
SKIPPED
BLOCKED
```

No Working Memory from one step may leak into another.

### Long-Term Memory

Cross-session validated business findings.

Example:

```json
{
  "finding_id": "...",
  "customer_id": "CUST-1001",
  "issue_category": "Login Failure",
  "finding_type": "CHURN_AFTER_ISSUE",
  "source_tickets": ["4021", "4031"],
  "confidence": 0.94,
  "jira_key": "SUP-123",
  "first_seen": "...",
  "last_seen": "...",
  "evidence_hash": "..."
}
```

LTM must survive application restart and must be searched before business Jira creation.

---

## 11. Dataset

Use the supplied:

```text
problem_18_ticket_intelligence_100_tickets.xlsx
```

as the canonical test dataset.

Do not replace it with invented data.

Validate:

- exactly 100 ticket records
- unique Ticket IDs
- valid Customer IDs
- valid issue categories
- churn fields
- Jira fields
- dates
- statuses

Use the dataset for deterministic acceptance tests.

---

## 12. Runtime Input and Query Folders

Every user query is a new runtime execution.

Create:

```text
Plan/<unique-query-folder>/
```

Example:

```text
Plan/
└── Query_<execution_id>_<sanitized_query>/
    ├── plan.json
    ├── execution.json
    ├── task_registry.json
    ├── TASK-001/
    │   ├── task.json
    │   ├── input.json
    │   ├── result.json
    │   └── execution.log
    ├── TASK-002/
    │   ├── task.json
    │   ├── input.json
    │   ├── result.json
    │   └── execution.log
    └── final_result.json
```

Never use the raw query as an unsafe filesystem path and never overwrite another execution.

---

## 13. Critical Requirement — Jira Is the Runtime Task Manager

For **every runtime user input**:

1. Atlas generates the executable plan.
2. Orchestrator validates it.
3. For each executable plan step, create a corresponding Jira runtime task.
4. Jira runtime tasks must be created through Jira MCP.
5. Each Jira task contains:
   - execution ID
   - plan ID
   - task ID
   - summary
   - objective
   - dependencies
   - expected output
   - tools
   - acceptance criteria
   - status
6. Jira tasks are linked to the runtime execution.
7. Scout executes those tasks.
8. Runtime task status is updated.
9. Executor output is posted as JSON in a Jira comment.
10. Dependent tasks consume the previous task's structured JSON output.

Jira is therefore part of runtime execution state.

---

## 14. Runtime Jira Task Lifecycle

Use:

```text
PENDING
  ↓
IN_PROGRESS
  ↓
COMPLETED
```

or:

```text
PENDING
  ↓
IN_PROGRESS
  ↓
FAILED
```

or:

```text
PENDING → BLOCKED
```

or:

```text
PENDING → SKIPPED
```

Create configurable mapping:

```text
internal_status → Jira_status
```

Example:

```text
PENDING     → To Do
IN_PROGRESS → In Progress
COMPLETED   → Done
FAILED      → Failed
BLOCKED     → Blocked
SKIPPED     → Done
```

---

## 15. Jira MCP Server

Implement a proper Jira MCP server.

There must be no direct Jira API calls from Atlas, Scout, JiraOps, or Orchestrator.

Mandatory MCP tools:

```text
jira.create_runtime_task
jira.update_runtime_task
jira.add_runtime_task_comment
jira.search_tickets
jira.search_tickets_by_category
jira.get_ticket
jira.create_ticket
jira.update_ticket
```

Optional:

```text
jira.add_label
jira.link_tickets
jira.get_transitions
jira.transition_issue
```

All Jira operations must flow:

```text
Agent/Application
→ MCP Client
→ Jira MCP Server
→ Jira
```

---

## 16. Jira MCP Tool Registry

Implement a canonical registry.

### `jira.create_runtime_task`

Input:

```json
{
  "execution_id": "...",
  "plan_id": "...",
  "task_id": "...",
  "summary": "...",
  "description": "...",
  "dependencies": [],
  "tools": [],
  "expected_output": "...",
  "acceptance_criteria": [],
  "labels": []
}
```

Output:

```json
{
  "success": true,
  "jira_key": "...",
  "jira_id": "...",
  "status": "..."
}
```

Side effect: `true`

### `jira.update_runtime_task`

Input:

```json
{
  "jira_key": "...",
  "status": "...",
  "execution_id": "...",
  "task_id": "..."
}
```

Output:

```json
{
  "success": true,
  "jira_key": "...",
  "status": "..."
}
```

Side effect: `true`

### `jira.add_runtime_task_comment`

Input:

```json
{
  "jira_key": "...",
  "task_id": "...",
  "execution_id": "...",
  "output_json": {}
}
```

Output:

```json
{
  "success": true,
  "comment_id": "..."
}
```

Side effect: `true`

### `jira.search_tickets`

Input:

```json
{
  "query": "...",
  "customer_id": "...",
  "issue_category": "...",
  "limit": 10
}
```

Side effect: `false`

### `jira.search_tickets_by_category`

Input:

```json
{
  "customer_id": "...",
  "issue_category": "..."
}
```

Side effect: `false`

### `jira.create_ticket`

Input:

```json
{
  "project": "...",
  "issue_type": "...",
  "summary": "...",
  "description": "...",
  "labels": [],
  "customer_id": "...",
  "issue_category": "...",
  "evidence": []
}
```

Side effect: `true`

### `jira.update_ticket`

Input:

```json
{
  "jira_key": "...",
  "fields": {},
  "comment": "..."
}
```

Side effect: `true`

### `jira.get_ticket`

Input:

```json
{
  "jira_key": "..."
}
```

Side effect: `false`

Every tool must define:

- canonical name
- purpose
- owner
- input schema
- output schema
- side-effect flag
- allowed agents
- failure conditions
- retryability

---

## 17. Non-Jira Tool Registry

Include at least:

### Environment

```text
validate_environment
get_runtime_config
get_model_config
```

### Runtime

```text
read_customer_query
create_query_folder
write_runtime_artifact
write_execution_log
```

### Data

```text
list_ticket_files
read_ticket_file
parse_ticket
chunk_ticket
validate_ticket_dataset
```

### Ticket Search

```text
ticket_get
ticket_search
customer_ticket_search
churn_status_lookup
churn_date_lookup
```

### Semantic Search

```text
embedding_generate
chromadb_get_collection
chromadb_query
chromadb_get
chromadb_upsert
validate_chroma_collection
rank_search_results
evaluate_top_k
```

### Memory

```text
stm_create
stm_read
stm_write
stm_update
stm_finalize

working_memory_create
working_memory_read
working_memory_write
working_memory_clear

ltm_search
ltm_insert
ltm_update
ltm_link_jira
ltm_get_related_finding
```

### Governance

```text
validate_finding
validate_evidence
validate_confidence
check_duplicate_finding
action_gate
```

### Execution

```text
resolve_task_inputs
validate_task
write_task_result
write_execution_log
```

---

## 18. Agent Tool Permissions

### ATLAS

Allowed:

```text
read_customer_query
get_runtime_config
get_model_config
ltm_search
validate_environment
inspect task registry
inspect tool registry
```

Not allowed:

```text
Jira CREATE
Jira UPDATE
Jira runtime task mutation
arbitrary ticket mutation
```

### SCOUT

Allowed:

```text
ticket_get
ticket_search
customer_ticket_search
churn_status_lookup
churn_date_lookup
semantic_ticket_search
embedding_generate
ChromaDB retrieval
STM
Working Memory
LTM search
validation tools
controlled runtime task status interface
```

SCOUT must not directly execute business Jira CREATE/UPDATE.

### JIRAOPS

Allowed:

```text
LTM search
Jira search
Jira category search
Jira get
Jira create
Jira update
```

### ORCHESTRATOR

Allowed:

```text
lifecycle tools
memory lifecycle
Jira runtime task orchestration
agent invocation
action gate
```

Use explicit permissions.

---

## 19. Runtime Task Schema

Every task generated by Atlas must use a structured schema:

```json
{
  "task_id": "TASK-001",
  "execution_id": "RUN-...",
  "plan_id": "PLAN-...",
  "summary": "Retrieve reference ticket 4021",
  "objective": "...",
  "assigned_agent": "SCOUT",
  "input": {
    "ticket_id": "4021"
  },
  "input_sources": [],
  "depends_on": [],
  "tools": [
    "ticket_get"
  ],
  "expected_output": "...",
  "success_condition": "...",
  "failure_condition": "...",
  "acceptance_criteria": [
    "Ticket 4021 exists",
    "Issue category is available"
  ],
  "memory_read": [
    "short_term"
  ],
  "memory_write": [
    "short_term"
  ],
  "side_effect": false,
  "status": "PENDING"
}
```

Every task must be executable without requiring the Executor to guess missing information.

---

## 20. Jira Runtime Task Description

The Jira task description must contain:

```text
EXECUTION ID
PLAN ID
TASK ID
TASK SUMMARY
OBJECTIVE
INPUT
DEPENDENCIES
TOOLS
EXPECTED OUTPUT
VALIDATION
ACCEPTANCE CRITERIA
FAILURE CONDITION
RECOVERY GUIDANCE
MEMORY INPUT
MEMORY OUTPUT
SIDE EFFECT
```

Never put secrets into Jira.

---

## 21. Executor JSON Contract

Executor output must be machine-readable JSON:

```json
{
  "execution_id": "RUN-123",
  "task_id": "TASK-004",
  "status": "COMPLETED",
  "result": {
    "ticket_id": "4021",
    "issue_category": "Login Failure"
  },
  "evidence": [
    {
      "source": "ticket:4021",
      "field": "issue_category"
    }
  ],
  "confidence": 0.98,
  "missing_information": [],
  "error": null,
  "retry": {
    "attempt": 1,
    "max_attempts": 3
  },
  "next_action": "TASK-005"
}
```

Do not use prose as the primary inter-agent contract.

---

## 22. Jira Comment Requirement

After each task execution:

1. Obtain final StepResult JSON.
2. Update Jira runtime task status.
3. Post the exact structured JSON as a Jira comment.
4. Include `execution_id`, `task_id`, and `status`.
5. Keep the comment parseable.

Example:

```json
{
  "execution_id": "RUN-123",
  "task_id": "TASK-004",
  "status": "COMPLETED",
  "result": {
    "ticket_id": "4021",
    "issue_category": "Login Failure"
  },
  "confidence": 0.98
}
```

---

## 23. Dependent Task Input

If:

```text
TASK-001
    ↓
TASK-002
```

then TASK-002 must receive TASK-001's structured JSON output.

Preferred mechanism:

```text
TASK-001
→ result.json
→ STM
→ Jira comment for audit
→ TASK-002 input resolver
```

Jira comments are the audit representation.

Structured storage is the canonical machine-to-machine contract.

Never pass arbitrary unvalidated Jira comment prose directly into an LLM context.

---

## 24. Atlas Planner Prompt

Create `prompts/atlas_prompt.txt` with the following core instructions:

```text
You are ATLAS, the Planner Agent for the Ticket Intelligence System.

Convert the user's natural-language request into the smallest complete
executable plan required to answer it accurately.

You do not execute tools.
You do not create Jira business tickets.
You do not modify Jira.
You do not fabricate information.

Reason about:
- entities
- ticket relationships
- customers
- issue categories
- churn
- semantic similarity
- historical memory
- existing Jira state
- dependencies
- missing information
- possible actionable findings.

Use only registered tools and task types.

Never invent tools or tasks.

For every task explicitly specify:
- task ID
- objective
- input
- dependencies
- tools
- expected output
- success condition
- failure condition
- acceptance criteria
- memory reads/writes
- side effects.

If information is missing, create a retrieval/validation task instead of assuming it.

If Jira action may be required, include the required search/validation/action
tasks but do not perform the Jira action yourself.

Return only the structured Plan schema.

Rules:
1. Never fabricate.
2. Never assume missing data.
3. Prefer deterministic tools for deterministic operations.
4. Use semantic search when wording may differ.
5. Use LTM when the query may relate to prior findings.
6. Search Jira before creating a duplicate issue.
7. Every side-effecting task must have explicit prerequisites.
8. Every task must have acceptance criteria.
9. Every task must identify tools.
10. Every task must identify expected output.
11. Every task must identify failure conditions.
12. Every task must identify dependencies.
13. Do not assign JiraOps work to Scout.
14. Do not assign retrieval work to JiraOps.
15. Do not assign planning work to Scout.
16. Ensure the plan is acyclic.
17. Produce the smallest complete plan.
```

---

## 25. Scout Executor Prompt

Create `prompts/scout_prompt.txt`:

```text
You are SCOUT, the Executor Agent.

Execute the exact runtime task provided by the Orchestrator.

Do not redesign the plan.
Do not invent business steps.
Do not fabricate missing information.
Use only tools explicitly authorized for the task.

For every task:
1. Read task definition.
2. Validate task input.
3. Read dependency outputs.
4. Read allowed memory.
5. Execute required tools.
6. Validate tool results.
7. Record evidence.
8. Determine success/failure.
9. Retry only when failure is retryable.
10. Produce the required JSON result.
11. Return the result to the Orchestrator.

When required information does not exist, report missing_information.

Never convert missing information into a guessed value.

Never claim a tool succeeded unless its result confirms success.

Never create or update a business Jira issue directly.

Output must conform to the StepResult JSON schema.
```

---

## 26. JiraOps Prompt

Create `prompts/jiraops_prompt.txt`:

```text
You are JIRAOPS, the Jira Action Agent.

Execute approved Jira business actions.

You receive a validated Finding and an Action Gate decision.

Allowed decisions:

CREATE
UPDATE
SKIP

Never create an issue solely because the user mentioned a problem.

Before CREATE:
1. Validate finding completeness.
2. Validate evidence.
3. Search Long-Term Memory.
4. Search Jira for existing related issues.
5. Determine whether the finding is genuinely new.

CREATE is allowed only when:
- evidence is sufficient
- required fields exist
- confidence meets configured threshold
- no equivalent finding exists
- no equivalent Jira issue exists
- Action Gate explicitly allows CREATE.

UPDATE is allowed only when:
- existing Jira issue is identified
- update is supported by new evidence
- Action Gate allows UPDATE.

SKIP when:
- finding is already known
- equivalent Jira issue exists
- evidence is insufficient
- required information is missing.

Never invent Jira fields.
Never invent customer information.
Never invent churn status.
Never call Jira directly.

All Jira operations MUST use Jira MCP tools.

Return only structured JiraActionResult JSON.
```

---

## 27. Orchestrator Flow

Implement:

```text
USER INPUT
    ↓
Create execution ID
    ↓
Create unique Query folder
    ↓
Initialize STM
    ↓
Read LTM context
    ↓
Validate environment
    ↓
Invoke ATLAS
    ↓
Validate Plan
    ↓
Create Jira runtime tasks
    ↓
Execute dependency graph
    ↓
For each task:
    create/initialize Working Memory
    ↓
    Jira task = IN_PROGRESS
    ↓
    resolve inputs
    ↓
    invoke SCOUT
    ↓
    validate StepResult
    ↓
    persist structured output
    ↓
    update Jira runtime task
    ↓
    add JSON Jira comment
    ↓
    promote approved result to STM
    ↓
    clear Working Memory
    ↓
    continue
    ↓
When actionable finding appears:
    ↓
Action Gate
    ↓
JIRAOPS
    ↓
Jira MCP
    ↓
CREATE / UPDATE / SKIP
    ↓
Persist Jira relationship in LTM
    ↓
Continue dependent tasks
    ↓
All tasks complete
    ↓
Generate final answer
    ↓
Persist final result
    ↓
Mark execution complete
```

---

## 28. Finding Identity and Idempotency

Implement deterministic finding identity using at least:

```text
customer_id
issue_category
finding_type
```

Example:

```text
SHA256(
    customer_id
    + "|"
    + issue_category
    + "|"
    + finding_type
)
```

Use it for idempotency.

Do not use the natural-language query as the primary duplicate key.

---

## 29. Action Gate

Before business Jira CREATE/UPDATE evaluate:

1. Finding completeness.
2. Evidence.
3. Confidence.
4. Existing LTM finding.
5. Existing Jira issue.
6. Required fields.
7. Business action policy.

Return:

```json
{
  "allowed": true,
  "decision": "CREATE|UPDATE|SKIP|BLOCKED",
  "reason": "...",
  "finding_id": "..."
}
```

No side effect is allowed without an allowed Action Gate decision.

---

## 30. Missing Information Policy

Distinguish:

```text
FALSE
UNKNOWN
NOT_FOUND
INCOMPLETE
ERROR
```

Never convert `UNKNOWN` to `FALSE`.

Never convert `NOT_FOUND` into a negative business conclusion.

If required information for a Jira action is unavailable:

- report missing information
- do not fabricate
- Action Gate = BLOCKED
- do not create a business Jira ticket

---

## 31. Semantic Search

Implement:

```text
query understanding
→ search representation
→ embedding
→ ChromaDB query
→ candidates
→ deduplicate ticket IDs
→ rank/filter
→ top 3–4 results
```

Required fields:

```text
ticket_id
matching_chunk
similarity/distance
resolution_status
customer_id
issue_category
source_file
chunk_id
chunk_index
```

The paraphrase test must succeed.

Example:

Historical issue:

> Session expires randomly every few minutes.

Query:

> App keeps logging me out.

The correct historical ticket must appear within Top 3.

---

## 32. Dynamic Task Generation

Do not use one hardcoded task sequence for every query.

Atlas determines the smallest complete plan at runtime.

Possible plan:

```text
Retrieve reference ticket
→ semantic search
→ identify matching customers
→ check churn
→ check LTM
→ check Jira
→ evaluate action
→ create/update Jira if allowed
→ persist finding
→ final result
```

This is only an example. Atlas must decide the actual plan.

---

## 33. Jira Runtime Task Naming

Recommended summary:

```text
[P18][<execution_id>][<task_id>] <task summary>
```

Recommended labels:

```text
problem18
runtime-task
<execution_id>
<agent>
```

Maintain:

```text
task_id → jira_key
```

in execution state, STM, and runtime artifacts.

---

## 34. Jira Task Dependencies

If Jira supports issue links/dependencies, use them.

Otherwise maintain dependencies in the task description and execution state.

Example:

```text
TASK-003
depends_on:
TASK-001
TASK-002
```

Do not execute TASK-003 until required dependencies are `COMPLETED`.

If a dependency fails, mark the dependent task `BLOCKED` unless a valid recovery path exists.

---

## 35. Execution Logging

Capture:

```text
execution_id
plan_id
task_id
agent
model
tool
timestamp
status
duration
retry_count
input_reference
output_reference
memory_read
memory_write
jira_key
error
```

Never log secrets.

---

## 36. Error Handling

Use structured errors such as:

```json
{
  "error_code": "CHROMA_COLLECTION_NOT_FOUND",
  "message": "...",
  "recoverable": true,
  "retryable": false,
  "source": "chromadb"
}
```

Support at least:

```text
MODEL_UNAVAILABLE
API_KEY_MISSING
JIRA_CONNECTION_FAILED
JIRA_AUTH_FAILED
MCP_CONNECTION_FAILED
MCP_TOOL_FAILED
CHROMA_COLLECTION_NOT_FOUND
CHROMA_QUERY_FAILED
EMBEDDING_FAILED
DATA_NOT_FOUND
INVALID_TASK
INVALID_PLAN
MISSING_REQUIRED_INPUT
INSUFFICIENT_EVIDENCE
DUPLICATE_FINDING
ACTION_BLOCKED
```

Never swallow exceptions silently.

---

## 37. Retry Policy

Use configurable bounded retries:

```yaml
max_retries: 3
```

Retry only errors explicitly marked retryable.

Do not retry:

- invalid input
- missing data
- authorization failure
- schema validation failure
- business-rule rejection

Log every retry.

---

## 38. Security

Never expose:

- API keys
- Jira tokens
- credentials
- environment secrets

in prompts, Jira, ChromaDB metadata, logs, task files, or final responses.

Use least-privilege tool permissions.

---

## 39. Testing

### Unit Tests

Test:

- Plan schema
- Task schema
- StepResult schema
- Finding identity
- duplicate detection
- memory isolation
- Action Gate
- tool registry
- model configuration
- error handling

### Integration Tests

Test:

- ChromaDB ingestion
- ChromaDB retrieval
- memory persistence
- Jira MCP client/server
- Jira task creation
- Jira status update
- Jira JSON comments

### E2E Test 1 — New Finding

Expected:

```text
Query
→ Atlas
→ dynamic plan
→ Jira runtime tasks
→ Scout
→ churn finding
→ Action Gate
→ JiraOps
→ Jira MCP CREATE
→ Jira key
→ LTM persistence
→ final answer
```

Verify correct Jira fields.

### E2E Test 2 — Existing Finding

Run a related query in a later session.

Expected:

```text
LTM recall
→ existing finding
→ existing Jira
→ NO duplicate business CREATE
→ final answer identifies recalled finding
```

A new runtime execution/task set is allowed; a duplicate business Jira issue is not.

### E2E Test 3 — Missing Information

Expected:

```text
missing information
→ no fabrication
→ Action Gate BLOCKED
→ no business Jira ticket
→ explicit final response
```

---

## 40. Additional Tests

### Jira Runtime Task Test

Verify:

1. Jira runtime tasks are created.
2. Every planned task has a Jira key.
3. Statuses change.
4. JSON comments are posted.
5. Dependent tasks receive structured previous output.
6. Failed tasks block invalid dependents.
7. Completed tasks cannot execute twice accidentally.

### Idempotency Test

Run the same query twice.

First run:

```text
runtime tasks created
business Jira created if finding is new
```

Second run:

```text
new runtime execution/tasks
existing finding = TRUE
existing Jira = TRUE
business Jira CREATE = FALSE
```

### Working Memory Isolation Test

Write temporary data to TASK-001 Working Memory.

After TASK-001 completes, clear it.

Verify TASK-002 cannot retrieve TASK-001 temporary state.

### Model Swappability Test

Change planner, executor, and JiraOps models only in configuration.

Verify each agent uses its newly configured model without source-code changes.

---

## 41. Prompt Versioning

Externalize prompts:

```text
prompts/atlas_prompt.txt
prompts/scout_prompt.txt
prompts/jiraops_prompt.txt
```

Every execution log must record:

```text
agent
prompt_version
model
timestamp
```

---

## 42. Plan Validation

Before creating Jira runtime tasks validate:

- JSON
- schema
- unique task IDs
- known agents
- known tools
- valid dependencies
- no cycles
- valid input references
- valid memory references
- side-effect prerequisites
- acceptance criteria
- failure condition

If invalid:

```text
Do not create runtime Jira tasks.
Return PLAN_VALIDATION_FAILED.
```

---

## 43. Task Validation

Before execution validate:

- task ID
- execution ID
- plan ID
- agent
- tools
- dependencies
- input
- expected output
- acceptance criteria

If invalid:

```text
Jira task = BLOCKED
```

and add a JSON failure comment.

---

## 44. Final User Response

Return:

1. Answer.
2. Key findings.
3. Evidence/source tickets.
4. Fresh findings.
5. Recalled findings.
6. Jira actions.
7. Jira keys.
8. Missing information.
9. Limitations.

Do not expose hidden chain-of-thought.

Example:

```text
RESULT:

Three customers had issues matching ticket 4021's login-failure pattern.

Customer CUST-1005 subsequently churned.

FRESH FINDING:
CUST-1005 / Login Failure / Churn

JIRA ACTION:
Created SUP-1042 through Jira MCP.

RECALLED:
No previous finding for this customer/category was found in long-term memory.

MISSING INFORMATION:
None.
```

---

## 45. Critical Architectural Rules

### Agentic design

Use LLMs for:

- query understanding
- planning
- relevance reasoning where needed
- structured Jira field preparation

Use deterministic code/tools for:

- ticket retrieval
- ChromaDB retrieval
- Jira MCP invocation
- memory persistence
- schema validation
- duplicate identity
- status transitions
- retry counters
- dependency resolution
- filesystem operations

### MCP

No direct Jira REST API implementation in:

- Atlas
- Scout
- JiraOps
- Orchestrator

All Jira operations must flow:

```text
Agent/Application
→ MCP Client
→ Jira MCP Server
→ Jira
```

### Memory

Do not use one generic memory object.

Clearly distinguish:

```text
SHORT_TERM_MEMORY
WORKING_MEMORY
LONG_TERM_MEMORY
```

Each needs:

- schema
- lifecycle
- read policy
- write policy
- owner
- isolation rules

---

## 46. Critical Jira Distinction

There are **two different Jira concepts**.

### A. Runtime Execution Task

Created for every plan step.

Purpose: execution tracking.

Example:

```text
[P18][RUN-123][TASK-004] Search Historical Tickets
```

### B. Business Jira Issue

Created only when a validated actionable finding requires it.

Purpose: actual customer/support issue tracking.

Do not confuse them.

A new user query creates runtime Jira tasks. It does **not** automatically mean a business Jira issue must be created.

Business Jira creation follows:

```text
Finding
→ Evidence
→ LTM
→ Jira duplicate check
→ Action Gate
→ JiraOps
→ MCP CREATE
```

---

## 47. Required Documentation

Generate:

```text
README.md
PROJECT_ANALYSIS.md
ARCHITECTURE.md
AGENT_DESIGN.md
TOOL_REGISTRY.md
MEMORY_ARCHITECTURE.md
JIRA_MCP.md
RUNTIME_EXECUTION.md
DATA_MODEL.md
TEST_PLAN.md
TRACEABILITY.md
CONFIGURATION.md
```

Documentation must reflect actual implementation. Do not document nonexistent functionality.

---

## 48. Traceability

Maintain:

```text
Requirement
→ Goal
→ Task
→ Subtask
→ Implementation
→ Runtime Task
→ Tool
→ Test Case
→ Evidence
```

Example:

```text
FR-003 Jira MCP
→ G14
→ G14-T01
→ G14-T01-ST01
→ jira_mcp_server.py
→ jira.search_tickets
→ TC-MCP-001
```

---

## 49. Implementation Order

Unless existing architecture requires otherwise:

1. Inspect existing project.
2. Reconcile requirements.
3. Architecture/configuration.
4. Data validation.
5. Schemas.
6. ChromaDB ticket ingestion/retrieval.
7. Memory architecture.
8. Tool registry.
9. Jira MCP server.
10. Jira MCP client.
11. Atlas Planner.
12. Scout Executor.
13. JiraOps.
14. Orchestrator.
15. Runtime Jira task generation.
16. Jira status/comment lifecycle.
17. Action Gate and idempotency.
18. End-to-end tests.
19. Documentation.

---

## 50. Development Rules

Follow strictly:

1. Never hardcode model names.
2. Never hardcode API keys.
3. Never hardcode Jira credentials.
4. Never directly call Jira APIs from agents.
5. Never bypass MCP.
6. Never assume one model for all agents.
7. Never use one generic memory layer.
8. Never leak Working Memory between steps.
9. Never fabricate missing data.
10. Never create duplicate business Jira issues.
11. Never use a fixed runtime task sequence for all queries.
12. Never allow unregistered tools.
13. Never allow unauthorized agents to call tools.
14. Never allow side effects without Action Gate.
15. Never confuse runtime Jira tasks with business Jira issues.
16. Never use natural-language output as the primary inter-agent contract.
17. Use structured JSON between tasks.
18. Validate every LLM structured response.
19. Bound retries.
20. Log execution states.
21. Isolate runtime executions.
22. Preserve existing working functionality unless requirements require change.
23. Prefer deterministic code for deterministic operations.
24. Do not claim completion until tests actually pass.

---

## 51. Definition of Done

The project is complete only when:

- [ ] Existing project inspected before implementation.
- [ ] Problem 18 requirements reconciled.
- [ ] Goal → Task → Subtask traceability exists.
- [ ] Atlas exists.
- [ ] Scout exists.
- [ ] JiraOps exists.
- [ ] Orchestrator exists.
- [ ] Agents use independently configurable models.
- [ ] Model configuration is externalized.
- [ ] API secrets are externalized.
- [ ] 100-ticket dataset is validated.
- [ ] ChromaDB ticket collection exists.
- [ ] Semantic search works.
- [ ] Paraphrase Top-3 test passes.
- [ ] Short-Term Memory works.
- [ ] Working Memory works.
- [ ] Working Memory clears after each step.
- [ ] Long-Term Memory persists across sessions.
- [ ] Finding identity is deterministic.
- [ ] Duplicate detection works.
- [ ] Jira MCP server works.
- [ ] Jira MCP client works.
- [ ] Runtime Jira tasks are created for every plan step.
- [ ] Runtime Jira statuses are updated.
- [ ] Executor output is posted as JSON Jira comments.
- [ ] Dependent tasks consume structured previous-task output.
- [ ] Business Jira CREATE works through MCP.
- [ ] Business Jira UPDATE works through MCP.
- [ ] Jira duplicate search works.
- [ ] Action Gate works.
- [ ] Missing information blocks unsupported actions.
- [ ] No hallucinated values are accepted.
- [ ] Fresh vs recalled information is distinguishable.
- [ ] MCP failures are handled.
- [ ] Model failures are handled.
- [ ] ChromaDB failures are handled.
- [ ] Retry logic is bounded.
- [ ] Runtime query folders are isolated.
- [ ] Execution logs are generated.
- [ ] Three mandatory E2E tests pass.
- [ ] Idempotency test passes.
- [ ] Working Memory isolation test passes.
- [ ] Model-swapping test passes.
- [ ] Documentation matches implementation.

---

## 52. Final Implementation Instruction

Do not start by writing the entire project blindly.

First:

1. Inspect files.
2. Analyze the existing implementation.
3. Produce/update `PROJECT_ANALYSIS.md`.
4. Identify reusable code.
5. Identify gaps against this specification.
6. Produce/update architecture.
7. Implement incrementally.
8. Run tests after each major subsystem.
9. Fix failures.
10. Run complete end-to-end tests.
11. Only then report completion.

When reporting implementation status, provide:

- Files created
- Files modified
- Agents implemented
- Tools implemented
- MCP tools implemented
- ChromaDB collections
- Memory layers
- Model configuration
- Runtime Jira task behavior
- Business Jira behavior
- Tests executed
- Tests passed
- Tests failed
- Remaining limitations

Do not claim a feature is implemented unless the code and tests demonstrate it.

The final system must be a genuinely executable:

```text
multi-agent
+
multi-model
+
MCP-enabled
+
ChromaDB-backed
+
memory-aware
+
Jira-orchestrated
+
idempotent
+
auditable
```

Ticket Intelligence System.
