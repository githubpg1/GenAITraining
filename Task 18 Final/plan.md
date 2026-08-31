# Problem 18 — End-to-End Execution Plan

For this problem, I recommend **3 AI agents**, not 4 or 5.

The clean architecture is:

**1. Atlas — Planner Agent**
Strong reasoning model. Converts the compound user question into a structured execution plan.

**2. Scout — Executor Agent**
Cheaper/faster model. Executes each step, retrieves data, evaluates relevance, retries when necessary, and determines whether the evidence is sufficient.

**3. JiraOps — Jira Agent**
Lightweight model. Handles Jira-specific action decisions and structured field construction through the MCP client.

There should also be a **non-LLM Orchestrator/Runtime**, but I would treat that as an application service, **not an AI agent**. It coordinates the agents, memory, execution state, and tool calls.

So the final architecture is:

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Runtime          │
                         │ Orchestrator     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Atlas            │
                         │ Planner Agent    │
                         │ Strong Model     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Short-Term       │
                         │ Memory           │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Scout            │
                         │ Executor Agent   │
                         │ Smaller Model    │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       Retrieval Tools     Working Memory      Long-Term Memory
                                  │
                                  ▼
                         Evidence / Finding
                                  │
                           Action Required?
                              │       │
                             NO      YES
                              │       │
                              │       ▼
                              │ ┌──────────────────┐
                              │ │ JiraOps          │
                              │ │ Jira Agent       │
                              │ │ Lightweight      │
                              │ │ Model            │
                              │ └────────┬─────────┘
                              │          │
                              │          ▼
                              │    MCP Client
                              │          │
                              │          ▼
                              │    Jira MCP Server
                              │          │
                              │          ▼
                              │         Jira
                              │
                              └──────────┬──────────┘
                                         │
                                         ▼
                                  Long-Term Memory
                                         │
                                         ▼
                                  Final Response
```

---

# 1. Agent responsibility matrix

| Agent    | Name             | Primary responsibility                                                  | Model                      |
| -------- | ---------------- | ----------------------------------------------------------------------- | -------------------------- |
| Planner  | **Atlas**        | Understand compound question and generate execution plan                | Strongest configured model |
| Executor | **Scout**        | Execute plan steps, retrieve evidence, grade relevance, retry, validate | Smaller/cheaper model      |
| Jira     | **JiraOps**      | Determine create/update action and construct Jira payload               | Lightweight model          |
| Runtime  | **Orchestrator** | Coordinate the entire execution lifecycle                               | No LLM                     |

The key principle is:

> **Model selection belongs to configuration, not to agent implementation.**

---

# 2. What the Orchestrator does

The Orchestrator is important even though it is not an AI agent.

It controls:

```text
User request
   ↓
Load config
   ↓
Create execution_id
   ↓
Initialize Short-Term Memory
   ↓
Call Atlas
   ↓
Validate plan
   ↓
Loop through plan
   ↓
Initialize Working Memory for step
   ↓
Call Scout
   ↓
Evaluate result
   ↓
If action required → JiraOps
   ↓
Persist relevant information to Long-Term Memory
   ↓
Clear Working Memory
   ↓
Continue next step
   ↓
Generate final response
```

It should be deterministic.

The LLM should not be responsible for controlling memory lifecycle or arbitrarily deciding what internal state is allowed to persist.

---

# 3. End-to-end task breakdown

I would divide the implementation into **15 major tasks**.

## Task 01 — Analyze and normalize the problem

Objective:

Convert the natural-language requirement into explicit functional requirements.

### Outputs

```text
requirements.md
traceability.md
acceptance_criteria.md
```

### Dependencies

None.

---

# Task 02 — Define system architecture

Design:

* Agents
* Orchestrator
* Memory layers
* MCP client/server
* Tool registry
* Configuration
* Data sources
* Execution lifecycle

### Output

```text
architecture.md
architecture_diagram
```

### Depends on

Task 01.

---

# Task 03 — Define configuration framework

This is especially important because your model requirement is explicit.

Create:

```text
config/
    model_config.yaml
    app_config.yaml
    jira_config.yaml
```

Conceptually:

```yaml
planner:
  model: <configurable-model>

executor:
  model: <configurable-model>

jira_agent:
  model: <configurable-model>
```

No agent should contain hardcoded model IDs.

### Output

Central configuration loader.

### Depends on

Task 02.

---

# Task 04 — Define common data contracts

All three agents need structured communication.

Create schemas for:

### PlannerPlan

```text
query
plan_id
steps[]
```

### PlanStep

```text
step_id
description
tool
inputs
dependencies
expected_output
action_possible
```

### StepResult

```text
step_id
status
evidence
finding
confidence
missing_information
actionable
```

### JiraActionRequest

```text
action
customer_id
issue_category
summary
description
labels
evidence
```

### JiraActionResult

```text
action
status
jira_key
message
```

This prevents agents from communicating through uncontrolled free-form text.

### Depends on

Task 02.

---

# Task 05 — Build the ticket data layer

Use the 100-ticket Excel dataset created earlier.

Primary purpose:

* ticket retrieval
* customer lookup
* semantic similarity
* issue-category lookup
* churn lookup
* historical ticket lookup

The current dataset becomes the base test data.

### Tools required

```text
ticket_search
ticket_get
customer_ticket_search
issue_category_search
churn_status_lookup
```

### Depends on

Task 04.

---

# Task 06 — Build semantic retrieval layer

Because Problem 18 extends the previous semantic-search capability, keep the RAG/retrieval layer independent of the agents.

Pipeline:

```text
Excel / ticket data
        ↓
Loader
        ↓
Chunk/document creation
        ↓
Embeddings
        ↓
Vector DB
        ↓
Retriever
```

The Executor should call retrieval tools rather than directly implementing vector-search internals.

### Tools

```text
semantic_ticket_search
similar_ticket_search
```

### Depends on

Task 05.

---

# Task 07 — Implement Atlas Planner Agent

Atlas receives:

```text
user_question
available_tools
memory_context
```

Atlas returns:

```json
{
  "plan_id": "PLAN-001",
  "steps": [
    {
      "step_id": 1,
      "description": "Retrieve ticket 4021",
      "tool": "ticket_get",
      "dependencies": []
    },
    {
      "step_id": 2,
      "description": "Identify issue category",
      "tool": "ticket_analysis",
      "dependencies": [1]
    }
  ]
}
```

### Atlas must NOT

* execute tools
* create Jira
* mutate memory
* directly access Jira
* invent missing information

It only plans.

### Depends on

Tasks 03, 04, 05, 06.

---

# 8. Task 08 — Implement Scout Executor Agent

Scout receives one step at a time.

Its responsibilities:

```text
Execute tool
      ↓
Inspect result
      ↓
Grade relevance
      ↓
Extract evidence
      ↓
Determine completeness
      ↓
Retry when appropriate
      ↓
Return structured result
```

For example:

```text
Step 4:
Determine which matching customers subsequently churned.
```

Scout can:

1. retrieve matching customers
2. retrieve churn records
3. compare the records
4. determine whether evidence is sufficient

### Retry logic

For example:

```text
Attempt 1 → irrelevant result
      ↓
modify query
      ↓
Attempt 2
      ↓
relevant result
```

Retry count should be configured.

### Depends on

Tasks 03–06.

---

# 9. Task 09 — Implement memory subsystem

This should be treated as a dedicated architectural component.

## 9.1 Short-Term Memory

Store:

```text
execution_id
user_query
plan
completed_step_results
current_findings
actions
final response state
```

Lifetime:

**One run**

---

## 9.2 Working Memory

Store:

```text
execution_id
step_id
attempt number
partial retrieval
candidate records
retry state
intermediate reasoning inputs
```

Lifetime:

**One step**

At completion:

```python
working_memory.clear(step_id)
```

This is a hard lifecycle boundary.

---

## 9.3 Long-Term Memory

Persist:

```text
customer
issue category
finding
source tickets
action taken
jira key
timestamp
confidence
```

Example:

```json
{
  "customer_id": "CUST-1001",
  "finding_type": "CHURN_AFTER_LOGIN_FAILURE",
  "issue_category": "Login Failure",
  "jira_key": "SUP-1001",
  "source_ticket_ids": ["4021"],
  "action": "JIRA_CREATED"
}
```

### Depends on

Task 04.

---

# 10. Task 10 — Implement memory deduplication service

This deserves its own task.

Before JiraOps creates anything:

```text
Finding
  ↓
Long-Term Memory lookup
  ↓
Equivalent finding?
```

Also:

```text
Jira category/customer lookup
```

Decision:

```text
No existing finding → CREATE
Existing finding + Jira exists → SKIP
Existing finding but Jira missing → CREATE
Existing Jira but finding new → UPDATE/REUSE depending on policy
```

This is your **idempotency layer**.

Do not rely on an LLM's memory.

### Depends on

Tasks 04 and 09.

---

# 11. Task 11 — Build Jira MCP Server

This is a core requirement.

The Jira MCP Server should expose:

```text
create_ticket
update_ticket
search_tickets
search_tickets_by_category
get_ticket
```

Conceptually:

```text
MCP Server
│
├── create_ticket
├── update_ticket
├── search_tickets
├── search_tickets_by_category
└── get_ticket
```

The underlying Jira implementation could use the actual Jira API or a mock Jira implementation, but the agent-facing interface remains MCP.

### Depends on

Task 04.

---

# 12. Task 12 — Build Jira MCP Client

JiraOps should never talk to Jira directly.

The interaction must be:

```text
JiraOps
   ↓
MCP Client
   ↓
MCP Server
   ↓
Jira
```

The MCP client should:

* discover tools
* invoke tools
* validate arguments
* capture tool results
* handle MCP errors

### Depends on

Task 11.

---

# 13. Task 13 — Implement JiraOps Agent

JiraOps receives:

```text
validated finding
+
memory check result
+
available Jira tools
```

It determines:

```text
CREATE
UPDATE
SKIP
```

Example:

```text
Finding:
CUST-1001 churned after Login Failure

Memory:
No equivalent new finding

Jira:
No matching Jira

Decision:
CREATE
```

Then:

```text
JiraOps
   ↓
MCP Client
   ↓
search_tickets_by_category
   ↓
create_ticket
```

### JiraOps must not

* invent customer information
* invent churn information
* bypass MCP
* create Jira from incomplete evidence

### Depends on

Tasks 03, 04, 10, 11, 12.

---

# 14. Task 14 — Implement action gate

Before any Jira action:

```text
                  Finding
                     │
                     ▼
             Required evidence?
                  /       \
                NO         YES
                │            │
                ▼            ▼
           STOP ACTION   Memory check
                              │
                              ▼
                       Existing action?
                         /          \
                       YES          NO
                        │            │
                        ▼            ▼
                      SKIP         JiraOps
```

Required evidence should include whatever is necessary for your Jira schema, for example:

```text
customer_id
issue_category
actionable finding
supporting source
sufficient confidence
```

This is what protects Test Case 3.

---

# 15. Task 15 — Implement final response and observability

The final response should not simply be:

> "A Jira ticket was created."

It should be traceable.

Recommended structure:

```text
Answer

Fresh findings:
...

Previously known:
...

Jira actions:
...

Missing information:
...

Execution summary:
...
```

Additionally, an execution trace should be available.

Example:

```text
Execution ID: RUN-007

PLAN
Step 1 → completed
Step 2 → completed
Step 3 → completed
Step 4 → completed

MEMORY
LTM recall → CUST-1001 / SUP-1001
Fresh evidence → ticket 4021

JIRA
search → existing SUP-1001
action → SKIPPED
```

---

# 16. Tool Registry

The tool registry should be centralized.

I would categorize tools like this.

## Retrieval tools

| Tool                     | Purpose                           |
| ------------------------ | --------------------------------- |
| `ticket_get`             | Retrieve a ticket by ID           |
| `ticket_search`          | Search tickets using filters      |
| `semantic_ticket_search` | Find semantically similar tickets |
| `customer_ticket_search` | Retrieve tickets for customer     |
| `issue_category_search`  | Find tickets by category          |
| `churn_status_lookup`    | Check customer churn status       |
| `churn_date_lookup`      | Retrieve churn date               |

---

## Memory tools

| Tool                    | Purpose                    |
| ----------------------- | -------------------------- |
| `stm_get`               | Read current run state     |
| `stm_update`            | Update current run state   |
| `working_memory_get`    | Read current step state    |
| `working_memory_update` | Update step state          |
| `working_memory_clear`  | Clear completed step state |
| `ltm_search`            | Search previous findings   |
| `ltm_store`             | Persist new finding        |
| `ltm_update`            | Update existing memory     |

---

## Jira MCP tools

| Tool                              | Purpose                 |
| --------------------------------- | ----------------------- |
| `jira.create_ticket`              | Create issue            |
| `jira.update_ticket`              | Update issue            |
| `jira.search_tickets`             | Search Jira             |
| `jira.search_tickets_by_category` | Search Jira by category |
| `jira.get_ticket`                 | Get Jira issue          |

The `jira.*` tools should be exposed through MCP, not implemented as direct Executor functions.

---

# 17. Tool registry metadata

I recommend every registered tool having metadata like:

```json
{
  "name": "semantic_ticket_search",
  "description": "Find tickets semantically similar to a query",
  "owner": "retrieval",
  "agent_access": ["Scout"],
  "input_schema": {},
  "output_schema": {},
  "side_effect": false
}
```

For Jira:

```json
{
  "name": "jira.create_ticket",
  "owner": "Jira MCP",
  "agent_access": ["JiraOps"],
  "side_effect": true,
  "requires_evidence": true
}
```

This is extremely useful.

Your Orchestrator can then enforce:

```text
side_effect = true
         ↓
require action gate
```

---

# 18. Agent-to-tool permissions

Do not give every agent every tool.

### Atlas

Allowed:

```text
memory read
tool registry read
```

Not allowed:

```text
Jira creation
Jira update
data mutation
```

### Scout

Allowed:

```text
ticket retrieval
semantic search
customer search
churn lookup
memory read
memory write for run state
```

Not allowed directly:

```text
jira.create_ticket
jira.update_ticket
```

### JiraOps

Allowed:

```text
Jira MCP tools
long-term memory lookup
```

This separation is important.

---

# 19. Complete dependency graph

The implementation dependency should be:

```text
Task 01
  │
  ▼
Task 02
  │
  ├──────────────┐
  ▼              ▼
Task 03        Task 04
  │              │
  │        ┌─────┼─────────────┐
  │        ▼     ▼             ▼
  │      Task 05 Task 09     Task 11
  │        │       │            │
  │        ▼       ▼            ▼
  │      Task 06 Task 10     Task 12
  │        │       │            │
  └────────┴───┬───┴────────────┘
               ▼
            Task 07
               │
               ▼
            Task 08
               │
               ▼
            Task 14
               │
               ▼
            Task 13
               │
               ▼
            Task 15
               │
               ▼
          Integration Tests
```

But in practice some branches can be developed in parallel.

---

# 20. Recommended implementation phases

## Phase 1 — Foundation

Implement:

```text
01 Requirements
02 Architecture
03 Config
04 Schemas
```

Deliverable:

**Architecture skeleton**

---

## Phase 2 — Data and Retrieval

Implement:

```text
05 Ticket data
06 Semantic retrieval
```

Deliverable:

**Ticket intelligence layer**

---

## Phase 3 — Agents

Implement:

```text
07 Atlas
08 Scout
```

Deliverable:

**Multi-hop Planner → Executor**

At this point the system should answer the original compound question without Jira.

---

## Phase 4 — Memory

Implement:

```text
09 Three memories
10 Deduplication
```

Deliverable:

**Stateful agent**

---

## Phase 5 — Jira MCP

Implement:

```text
11 MCP Server
12 MCP Client
13 JiraOps
14 Action Gate
```

Deliverable:

**Agentic action capability**

---

## Phase 6 — Full integration

Implement:

```text
15 Observability
Integration tests
```

Deliverable:

**Complete Problem 18 system**

---

# 21. Runtime execution plan

Let's use the exact example:

> Which customers had the same login issue as ticket 4021, and did any of them churn afterward?

The runtime should behave approximately like this.

### Step 1

User submits query.

```text
RUN-001
```

Orchestrator initializes:

```text
Short-Term Memory = {}
Working Memory = {}
```

---

### Step 2

Atlas receives:

```text
Question
Available tools
Relevant long-term context
```

Atlas generates:

```text
1. Retrieve 4021
2. Determine issue category
3. Find similar customers
4. Check churn
5. Determine fresh vs known finding
6. Perform action if required
```

Plan saved to Short-Term Memory.

---

### Step 3

Scout executes Step 1.

Working Memory:

```text
step = 1
```

Retrieves ticket 4021.

Result:

```text
Login Failure
Customer = CUST-1001
```

Step complete.

Working Memory cleared.

---

### Step 4

Scout executes Step 2.

Working Memory is recreated:

```text
step = 2
```

It determines:

```text
Issue Category = Login Failure
```

Clear working memory.

---

### Step 5

Scout executes Step 3.

Semantic search finds:

```text
CUST-1001
CUST-1002
CUST-1003
...
```

---

### Step 6

Scout checks churn.

Potential result:

```text
CUST-1001 → churned
CUST-1002 → churned
CUST-1003 → churned
```

Now you have actionable findings.

---

# 22. Memory decision

Before Jira action:

```text
Search Long-Term Memory
```

Suppose:

```text
CUST-1001
existing finding = yes
Jira = SUP-1001
```

while:

```text
CUST-1003
existing finding = no
Jira = none
```

Then:

```text
CUST-1001 → previously known → don't duplicate
CUST-1003 → genuinely new → Jira action
```

This is exactly the behavior Problem 18 is asking for.

---

# 23. Jira execution

For CUST-1003:

```text
Scout
 ↓
Actionable finding
 ↓
Action Gate
 ↓
JiraOps
 ↓
MCP Client
 ↓
search_tickets_by_category
 ↓
No equivalent ticket
 ↓
create_ticket
 ↓
Jira response
 ↓
SUP-1234
```

Then long-term memory stores:

```text
CUST-1003
LOGIN_FAILURE
CHURN
SUP-1234
```

---

# 24. Working-memory lifecycle

This deserves explicit implementation.

For every step:

```text
create(step_id)
      ↓
execute
      ↓
retry if needed
      ↓
produce result
      ↓
commit relevant result to STM
      ↓
clear(step_id)
```

Never:

```text
Step 1 working memory
        ↓
automatically remain
        ↓
Step 2
```

The only state that crosses step boundaries should be **explicitly promoted state**.

That gives you:

```text
Working Memory
      ↓
validated
      ↓
Short-Term Memory
```

rather than uncontrolled leakage.

---

# 25. Long-term memory lifecycle

Only information satisfying persistence criteria should enter LTM.

For example:

```text
temporary retrieval
        ↓
NO
```

but:

```text
validated finding
        ↓
action performed
        ↓
YES
```

Potential LTM record types:

```text
FINDING
ACTION
JIRA_RELATIONSHIP
CUSTOMER_RISK
PREVIOUS_RESPONSE
```

Don't dump the entire conversation into LTM.

That would violate the requirement's distinction between memory types.

---

# 26. Test strategy

You need at least these three mandatory end-to-end tests.

## Test 1 — New Finding + Jira Creation

Input:

```text
Which customers had the same login issue as ticket 4021,
and did any of them churn afterward?
```

Expected:

```text
Planner produces multi-step plan
Executor executes steps
Churn finding discovered
LTM says not previously known
JiraOps invoked
MCP search executed
MCP create_ticket executed
Jira key returned
LTM updated
```

Evidence to capture:

```text
Plan
Step trace
Evidence
Memory lookup
MCP call
Jira result
LTM record
```

---

# 27. Test 2 — Related question in later session

Session 1:

```text
Finding discovered
Jira SUP-XXXX created
LTM updated
```

Session 2:

```text
Related question about same customer
```

Expected:

```text
LTM recall
Existing finding detected
Existing Jira detected
No duplicate Jira
Finding marked as previously known
```

Critical assertions:

```text
create_ticket count = 0
```

for the already-known finding.

---

# 28. Test 3 — Missing information

Example:

```text
Which customers churned after the issue,
and what was their exact churn date?
```

Suppose churn date isn't available.

Expected:

```text
Agent explicitly reports:
"Churn date could not be found in available data."
```

And:

```text
Jira creation = 0
```

No inferred date.

No fabricated Jira action.

---

# 29. Additional tests I strongly recommend

The requirement only mandates three tests, but a robust implementation should have more.

### Test 4 — Jira update

Existing Jira found but additional information is newly discovered.

Expected:

```text
update_ticket
```

rather than `create_ticket`.

### Test 5 — MCP failure

Simulate:

```text
MCP server unavailable
```

Expected:

```text
Finding retained
Jira action reported as failed
System does not claim ticket was created
```

### Test 6 — Retrieval failure + retry

First search fails.

Expected:

```text
retry
```

Then successful result.

### Test 7 — Working memory isolation

Verify:

```text
Step 1 temporary data ≠ Step 2 working context
```

### Test 8 — Model independence

Change:

```text
Planner model
```

without changing:

```text
Executor/Jira code
```

and vice versa.

This proves the multi-model architecture is real.

---

# 30. Acceptance criteria

I would make the final acceptance checklist look like this:

| Area             | Acceptance criterion                             |
| ---------------- | ------------------------------------------------ |
| Planning         | Compound questions decomposed into ordered steps |
| Planner model    | Strongest model configurable independently       |
| Execution        | Steps executed in dependency order               |
| Executor model   | Independent configurable model                   |
| Jira Agent       | Separate agent exists                            |
| Jira model       | Independently configurable                       |
| MCP              | Jira operations performed through MCP            |
| Create           | Can create Jira                                  |
| Update           | Can update Jira                                  |
| Search           | Can search Jira by category                      |
| STM              | Current run state maintained                     |
| Working memory   | Cleared between steps                            |
| LTM              | Persists across sessions                         |
| Deduplication    | Duplicate action prevented                       |
| Fresh vs known   | Clearly distinguished                            |
| Missing data     | Explicitly reported                              |
| Hallucination    | No fabricated result                             |
| Evidence         | Jira action backed by evidence                   |
| Traceability     | Plan and execution trace visible                 |
| Failure handling | MCP failures not falsely reported as successes   |

---

# 31. Tool registry mapped to tasks

Here is the implementation mapping I would use:

| Task              | Tools                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Ticket retrieval  | `ticket_get`, `ticket_search`                                         |
| Semantic matching | `semantic_ticket_search`, `similar_ticket_search`                     |
| Customer history  | `customer_ticket_search`                                              |
| Issue analysis    | `issue_category_search`                                               |
| Churn             | `churn_status_lookup`, `churn_date_lookup`                            |
| Short-term memory | `stm_get`, `stm_update`                                               |
| Working memory    | `working_memory_get`, `working_memory_update`, `working_memory_clear` |
| Long-term memory  | `ltm_search`, `ltm_store`, `ltm_update`                               |
| Jira discovery    | `jira.search_tickets`, `jira.search_tickets_by_category`              |
| Jira retrieval    | `jira.get_ticket`                                                     |
| Jira creation     | `jira.create_ticket`                                                  |
| Jira update       | `jira.update_ticket`                                                  |

---

# 32. Agent/tool mapping

| Agent            | Tools                                                  |
| ---------------- | ------------------------------------------------------ |
| **Atlas**        | Tool registry read, memory read                        |
| **Scout**        | Ticket/search/churn tools + STM + Working Memory + LTM |
| **JiraOps**      | LTM lookup + all Jira MCP tools                        |
| **Orchestrator** | Agent invocation + memory lifecycle + action gate      |

Notice an important point:

**The Orchestrator owns lifecycle. Agents own decisions.**

That is a much cleaner architecture than letting every agent manipulate everything.

---

# 33. Recommended folder architecture

Building on your previous Problem 16 structure, I would use:

```text
Problem_18_Ticket_Intelligence/
│
├── config/
│   ├── model_config.yaml
│   ├── app_config.yaml
│   └── jira_config.yaml
│
├── agents/
│   ├── atlas_planner.py
│   ├── scout_executor.py
│   └── jiraops_agent.py
│
├── orchestration/
│   └── orchestrator.py
│
├── mcp/
│   ├── jira_mcp_server.py
│   ├── jira_mcp_client.py
│   └── tool_registry.py
│
├── memory/
│   ├── short_term.py
│   ├── working_memory.py
│   ├── long_term.py
│   └── deduplication.py
│
├── tools/
│   ├── ticket_tools.py
│   ├── customer_tools.py
│   ├── churn_tools.py
│   └── retrieval_tools.py
│
├── prompts/
│   ├── atlas_prompt.txt
│   ├── scout_prompt.txt
│   └── jiraops_prompt.txt
│
├── data/
│   └── tickets.xlsx
│
├── schemas/
│   ├── plan_schema.py
│   ├── execution_schema.py
│   └── jira_schema.py
│
├── tests/
│   ├── test_new_finding.py
│   ├── test_memory_recall.py
│   ├── test_missing_data.py
│   ├── test_jira_mcp.py
│   └── test_memory_isolation.py
│
├── logs/
│
└── main.py
```

---

# 34. One design rule I strongly recommend

Do **not** make your architecture:

```text
Planner → Executor → Jira Agent → Memory
```

where memory is just something the agents "can access."

Instead make memory part of the **runtime state machine**:

```text
                 Orchestrator
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      Atlas          Scout        JiraOps
        │             │             │
        └─────────────┼─────────────┘
                      │
                  State Manager
             ┌────────┼────────┐
             ▼        ▼        ▼
            STM      WM       LTM
```

This guarantees the three memory semantics rather than merely documenting them.

---

# 35. Final implementation sequence

The cleanest execution order is:

```text
1. Requirements & acceptance criteria
            ↓
2. Architecture
            ↓
3. Config + model routing
            ↓
4. Shared schemas
            ↓
5. Ticket data + retrieval
            ↓
6. Atlas Planner
            ↓
7. Scout Executor
            ↓
8. Short-term + Working Memory
            ↓
9. Long-term Memory
            ↓
10. Deduplication / idempotency
            ↓
11. Jira MCP Server
            ↓
12. Jira MCP Client
            ↓
13. JiraOps Agent
            ↓
14. Action Gate
            ↓
15. Orchestrator integration
            ↓
16. Observability / execution trace
            ↓
17. Test 1 — new finding
            ↓
18. Test 2 — memory recall
            ↓
19. Test 3 — missing data
            ↓
20. Additional resilience tests
            ↓
21. Final demo
```

## The key architectural outcome

At the end, Problem 18 should demonstrate **six independent capabilities**:

```text
Multi-hop reasoning
        +
Multi-agent architecture
        +
Multi-model routing
        +
MCP-based tool/action execution
        +
Three-layer memory
        +
Idempotent evidence-driven actions
```

That is the real scope of the problem. The Jira integration by itself is only one piece; the bigger goal is to prove that the original Planner/Executor RAG system has evolved into a **stateful, action-capable, multi-agent architecture** without making the agents tightly coupled to one model, one memory implementation, or one external system.
