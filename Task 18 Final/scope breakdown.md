Yes. The missing piece is **workability**.

A development plan for an agentic system cannot stop at:

> "Implement Long-Term Memory."

The developer/implementation agent needs to know **what data exists, what schema to create, what tool it can call, what configuration it needs, what it should produce, how failure is represented, and exactly how we decide the subtask is complete.**

So I would strengthen the previous plan without changing the hierarchy:

> **GOAL → TASK → SUBTASK**

and make every subtask an **implementation-ready unit of work**.

---

# Problem 18 — Implementation-Ready Development Plan

## 0. Overall system we are building

Before the WBS, this is the target architecture the subtasks must collectively produce:

```text
                         USER QUERY
                             │
                             ▼
                    ┌─────────────────┐
                    │   ORCHESTRATOR  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ ATLAS PLANNER   │
                    │ Strong Model    │
                    └────────┬────────┘
                             │
                       Structured Plan
                             │
                             ▼
                    ┌─────────────────┐
                    │  PLAN VALIDATOR │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SCOUT EXECUTOR  │
                    │ Smaller Model   │
                    └────────┬────────┘
                             │
              ┌──────────────┼───────────────┐
              ▼              ▼               ▼
         Ticket Tools   Memory Tools    Evidence Tools
              │              │
              │              ├── STM
              │              ├── Working Memory
              │              └── LTM
              │
              ▼
        ACTION GATE
              │
       ┌──────┴──────┐
       ▼             ▼
   NO ACTION       ACTION
                     │
                     ▼
              ┌──────────────┐
              │ JIRAOPS      │
              │ Lightweight  │
              │ Model        │
              └──────┬───────┘
                     │
                     ▼
                MCP CLIENT
                     │
                     ▼
                JIRA MCP SERVER
                     │
                     ▼
                    JIRA
```

---

# GOAL G01 — Establish Requirements, Scope and Acceptance Model

**Purpose:** Convert Problem 18 into an implementation contract.

---

## G01-T01 — Normalize requirements

### G01-T01-ST01 — Extract functional requirements

**Objective:** Convert the narrative into individually testable functional requirements.

**Input/Data required:**

* Problem 18 statement
* Existing Problem 16 requirements/architecture
* Existing Planner/Executor implementation, if available

**Prerequisites:**

* Problem 18 requirement approved.

**Dependencies:** None.

**Tools:**

* Requirement document
* Existing project files

**Output:**

```text
FR-001 Multi-hop planning
FR-002 Multi-step execution
FR-003 Jira MCP integration
FR-004 Jira create
FR-005 Jira update
FR-006 Jira search
FR-007 Multi-model routing
FR-008 Short-term memory
FR-009 Working memory
FR-010 Long-term memory
FR-011 Duplicate prevention
FR-012 Missing-data handling
FR-013 Fresh vs recalled findings
FR-014 Execution traceability
```

**Acceptance Criteria:**

* Every functional requirement is uniquely identified.
* Every statement in Problem 18 maps to at least one FR.
* No requirement depends on an implicit assumption.

**Failure condition:**

* Any requirement cannot be traced to implementation or testing.

---

### G01-T01-ST02 — Extract non-functional requirements

**Data required:**

* Problem statement
* Architecture constraints

**Output:**

```text
NFR-001 Model configurability
NFR-002 Agent isolation
NFR-003 Idempotency
NFR-004 Observability
NFR-005 Error handling
NFR-006 Configuration security
NFR-007 Deterministic tool contracts
NFR-008 Memory isolation
```

**Acceptance Criteria:**

* Each NFR has measurable acceptance criteria.
* Model names are not hardcoded.
* Secrets are not stored in source code.

---

### G01-T01-ST03 — Define scope boundaries

**Output:**

* In-scope list
* Out-of-scope list
* Assumptions

**Important assumptions to explicitly record:**

```text
1. Jira can be represented by a real Jira instance or controlled mock.
2. Ticket data is available locally.
3. Churn data is available in a controlled dataset.
4. MCP server exposes Jira functionality.
5. LTM persists between application runs.
6. System must survive process restart.
```

**Acceptance Criteria:**
Every implementation dependency is either provided or explicitly identified as an assumption.

---

# GOAL G02 — Define Target Agent Architecture

## G02-T01 — Define Atlas Planner Agent

### G02-T01-ST01 — Define Atlas responsibility

**Input:**

* FR-001
* Agent architecture

**Output:**
Atlas specification.

**Atlas does:**

* interpret query
* identify entities
* identify required information
* decompose into steps
* assign tools
* assign dependencies
* identify possible actions

**Atlas does NOT:**

* execute arbitrary tools
* directly mutate Jira
* bypass memory policies

**Acceptance Criteria:**
Atlas responsibilities are non-overlapping with Scout and JiraOps.

---

### G02-T01-ST02 — Define Planner input contract

**Input:**

```json
{
  "query": "...",
  "available_tools": [],
  "memory_context": {},
  "system_capabilities": {}
}
```

**Output:**
Validated PlannerRequest schema.

**Acceptance Criteria:**
All information required for planning is represented explicitly.

---

### G02-T01-ST03 — Define Planner output contract

Output must contain:

```text
plan_id
goal
steps[]
dependencies[]
action_conditions[]
required_information[]
```

**Acceptance Criteria:**
Planner output is machine-parseable and schema-validatable.

---

## G02-T02 — Define Scout Executor Agent

### G02-T02-ST01 — Define execution responsibility

Scout handles:

```text
tool invocation
retrieval
relevance evaluation
evidence extraction
completeness evaluation
retry
StepResult generation
```

**Acceptance Criteria:**
Scout never independently decides to create Jira without Action Gate/JiraOps.

---

### G02-T02-ST02 — Define Scout input/output contract

**Input:**

* PlanStep
* STM
* Working Memory

**Output:**
StepResult.

---

## G02-T03 — Define JiraOps Agent

### G02-T03-ST01 — Define JiraOps responsibilities

JiraOps handles:

```text
finding → Jira payload
Jira duplicate search
CREATE
UPDATE
SKIP
MCP invocation
```

**Acceptance Criteria:**
JiraOps only acts on validated actionable findings.

---

# GOAL G03 — Build Development Environment and Configuration

This was under-specified previously and is critical for a **workable condition**.

## G03-T01 — Establish project structure

### G03-T01-ST01 — Define directory structure

Example:

```text
problem18/
│
├── agents/
│   ├── atlas/
│   ├── scout/
│   └── jiraops/
│
├── orchestrator/
│
├── tools/
│   ├── ticket_tools/
│   ├── memory_tools/
│   └── jira/
│
├── mcp/
│   ├── server/
│   └── client/
│
├── memory/
│   ├── short_term/
│   ├── working/
│   └── long_term/
│
├── data/
│   ├── tickets/
│   ├── customers/
│   └── test_fixtures/
│
├── schemas/
│
├── config/
│
├── tests/
│
└── logs/
```

**Acceptance Criteria:**
Every architectural component has a defined location.

---

### G03-T01-ST02 — Define dependency versions

**Data required:**

* Python version
* LLM SDK version
* MCP SDK version
* vector DB version
* persistence DB version
* testing framework

**Acceptance Criteria:**
All dependencies are pinned or version-constrained.

---

## G03-T02 — External configuration

### G03-T02-ST01 — Create model configuration

Example:

```yaml
planner:
  provider: openai
  model: configured-model

executor:
  provider: openai
  model: configured-model

jiraops:
  provider: openai
  model: configured-model
```

**Acceptance Criteria:**
Changing a model requires configuration change only.

---

### G03-T02-ST02 — Configure secrets

`.env`:

```text
LLM_API_KEY=
JIRA_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=
```

**Acceptance Criteria:**

* `.env` excluded from Git.
* No secret hardcoded.
* Missing secret causes clear startup failure.

---

### G03-T02-ST03 — Define runtime configuration

Include:

```text
similarity_threshold
confidence_threshold
max_retries
memory expiration
Jira project key
Jira issue type
```

**Acceptance Criteria:**
Operational behavior is configurable without source modification.

---

# GOAL G04 — Define Shared Data Contracts

## G04-T01 — Plan schema

### G04-T01-ST01 — Define Plan schema

**Required data:**

```json
{
  "plan_id": "",
  "query": "",
  "goal": "",
  "steps": [],
  "dependencies": [],
  "action_conditions": []
}
```

**Acceptance Criteria:**
Schema validates valid plans and rejects malformed plans.

---

### G04-T01-ST02 — Define PlanStep schema

Mandatory:

```text
step_id
summary
objective
assigned_agent
input
input_source
prerequisites
depends_on
tools
expected_output
memory_read
memory_write
side_effect
success_condition
failure_condition
```

**Acceptance Criteria:**
No executable step can exist without these mandatory attributes.

---

## G04-T02 — Define execution schemas

### G04-T02-ST01 — Define StepResult

Must support:

```text
status
output
evidence
confidence
missing_information
error
retry_count
```

### G04-T02-ST02 — Define Finding

Must support:

```text
finding_id
customer_id
ticket_ids
issue_category
finding_type
evidence
confidence
first_seen
source_type
```

---

## G04-T03 — Define error schema

This is important for agent reliability.

```json
{
  "error_code": "DATA_NOT_FOUND",
  "message": "",
  "recoverable": false,
  "retryable": false,
  "source": ""
}
```

**Acceptance Criteria:**
Missing data, tool failure, validation failure and model failure are distinguishable.

---

# GOAL G05 — Prepare Ticket and Customer Data

## G05-T01 — Establish canonical dataset

### G05-T01-ST01 — Validate 100 ticket dataset

**Required fields:**

```text
ticket_id
customer_id
created_at
issue_category
issue_description
resolution
resolution_status
churn_status
churn_date
jira_key
```

**Acceptance Criteria:**

* Exactly 100 tickets.
* Unique ticket IDs.
* Customer IDs valid.
* Issue categories populated.
* Churn status explicitly represented.
* Some records intentionally contain missing information for negative testing.
* At least one deterministic dataset supports the 4021 scenario.

---

### G05-T01-ST02 — Establish customer dataset

This is a missing dependency from the earlier plan.

**Required fields:**

```text
customer_id
customer_name
account_status
churn_status
churn_date
```

**Acceptance Criteria:**
Every ticket references a valid customer.

---

### G05-T01-ST03 — Establish deterministic test fixtures

Create dedicated records for:

```text
TC01_NEW_FINDING
TC02_EXISTING_FINDING
TC03_MISSING_DATA
```

**Acceptance Criteria:**
The three acceptance scenarios do not depend on random data.

---

# GOAL G06 — Build Retrieval Layer

## G06-T01 — Ticket retrieval

### G06-T01-ST01 — Implement `ticket_get`

**Input:**

```text
ticket_id
```

**Output:**
Canonical ticket.

**Acceptance Criteria:**

* Existing ID → one record.
* Unknown ID → `DATA_NOT_FOUND`.
* Duplicate IDs → dataset validation failure.

---

### G06-T01-ST02 — Implement `ticket_search`

Inputs:

```text
query
issue_category
customer_id
status
limit
```

**Acceptance Criteria:**
Filters work independently and in combination.

---

## G06-T02 — Customer retrieval

### G06-T02-ST01 — Implement customer history

**Input:**
`customer_id`

**Output:**
Customer's tickets.

### G06-T02-ST02 — Implement churn lookup

**Input:**
`customer_id`

**Output:**

```json
{
  "churned": true,
  "churn_date": "..."
}
```

**Acceptance Criteria:**
Missing churn information returns explicit missing state rather than `false`.

This distinction is critical:

```text
churned = false
```

is NOT equivalent to:

```text
churn_status = UNKNOWN
```

---

# GOAL G07 — Build Semantic Retrieval

## G07-T01 — Index ticket data

### G07-T01-ST01 — Create ticket documents

**Input:**
Ticket dataset.

**Data transformation:**

```text
Ticket ID
+
Issue Category
+
Issue Description
+
Resolution
```

**Output:**
Search documents.

---

### G07-T01-ST02 — Generate embeddings

**Input:**
Normalized ticket documents.

**Output:**
Embedding vectors.

**Acceptance Criteria:**
All indexable tickets have embeddings.

---

### G07-T01-ST03 — Store vector metadata

Metadata:

```text
ticket_id
customer_id
issue_category
resolution_status
```

---

## G07-T02 — Implement semantic search

### G07-T02-ST01 — Implement `semantic_ticket_search`

**Input:**

```text
query
top_k
similarity_threshold
```

**Output:**

```text
ticket_id
customer_id
similarity
metadata
```

**Acceptance Criteria:**
Search can identify semantically similar login issues even when wording differs.

---

# GOAL G08 — Build Atlas Planner

## G08-T01 — Planner prompt engineering

### G08-T01-ST01 — Define planning system prompt

Prompt must contain:

* role
* responsibilities
* task registry
* tool registry
* planning rules
* dependency rules
* memory rules
* action constraints
* missing-data rules
* output schema

**Acceptance Criteria:**
Prompt explicitly prevents direct Jira execution.

---

### G08-T01-ST02 — Define few-shot planning examples

Examples should include:

```text
simple query
compound query
missing-data query
query requiring memory
query requiring Jira action
```

**Acceptance Criteria:**
Examples demonstrate correct decomposition.

---

## G08-T02 — Implement Planner

### G08-T02-ST01 — Invoke configured Planner model

**Acceptance Criteria:**
Model is loaded dynamically.

### G08-T02-ST02 — Validate Planner output

**Checks:**

```text
schema
task existence
tool existence
dependencies
cycles
agent permissions
```

---

### G08-T02-ST03 — Implement plan repair

**Input:**
Invalid plan.

**Output:**
Corrected plan or terminal planning failure.

**Acceptance Criteria:**
Planner cannot proceed with an invalid plan.

---

# GOAL G09 — Build Scout Executor

## G09-T01 — Tool execution

### G09-T01-ST01 — Resolve inputs

Input sources:

```text
USER_QUERY
PLAN
PREVIOUS_STEP
STM
WORKING_MEMORY
LTM
CONFIG
```

**Acceptance Criteria:**
References resolve deterministically.

---

### G09-T01-ST02 — Execute tool

**Acceptance Criteria:**

* Tool exists in registry.
* Agent has permission.
* Parameters match schema.
* Result is captured.

---

## G09-T02 — Relevance and evidence

### G09-T02-ST01 — Grade retrieval relevance

**Input:**
Retrieved records.

**Output:**

```text
relevant
confidence
reason
```

### G09-T02-ST02 — Extract evidence

**Acceptance Criteria:**
Every finding references source records.

---

### G09-T02-ST03 — Determine completeness

Must distinguish:

```text
COMPLETE
PARTIAL
MISSING
```

---

## G09-T03 — Retry

### G09-T03-ST01 — Implement bounded retry

Configuration:

```text
MAX_RETRIES
RETRYABLE_ERRORS
BACKOFF
```

**Acceptance Criteria:**

* No infinite loops.
* Retry attempts logged.
* Non-retryable errors aren't retried.

---

# GOAL G10 — Implement Short-Term Memory

## G10-T01 — Run memory

### G10-T01-ST01 — Create run record

Fields:

```text
run_id
query
plan_id
started_at
status
```

### G10-T01-ST02 — Store validated StepResults

### G10-T01-ST03 — Retrieve previous step results

### G10-T01-ST04 — Finalize run

**Acceptance Criteria:**
STM contains everything required for the current run but is not used as persistent cross-session memory.

---

# GOAL G11 — Implement Working Memory

## G11-T01 — Step-local state

### G11-T01-ST01 — Create step memory

Key:

```text
run_id + step_id
```

### G11-T01-ST02 — Store attempts

Store:

```text
attempt_number
tool
input
result
error
timestamp
```

### G11-T01-ST03 — Store partial evidence

### G11-T01-ST04 — Clear memory after step

**Critical Acceptance Criteria:**

```text
Given STEP-001 completed,
when STEP-002 begins,
STEP-002 cannot access STEP-001's temporary Working Memory.
```

Only promoted data in STM may cross the boundary.

---

# GOAL G12 — Implement Long-Term Memory

## G12-T01 — Define LTM data model

### G12-T01-ST01 — Finding memory

Fields:

```text
finding_id
customer_id
issue_category
finding_type
source_tickets
evidence_hash
confidence
first_seen
last_seen
```

### G12-T01-ST02 — Jira relationship memory

Fields:

```text
finding_id
jira_key
action
created_at
updated_at
```

### G12-T01-ST03 — Memory provenance

Store:

```text
source
run_id
agent
timestamp
```

**Acceptance Criteria:**
Every persistent memory record can be traced to evidence.

---

## G12-T02 — LTM operations

### G12-T02-ST01 — Search LTM

### G12-T02-ST02 — Insert finding

### G12-T02-ST03 — Update finding

### G12-T02-ST04 — Store Jira relationship

### G12-T02-ST05 — Retrieve related historical findings

**Acceptance Criteria:**
Memory survives application restart and is available in a later session.

---

# GOAL G13 — Build Finding Identity and Deduplication

## G13-T01 — Finding identity

### G13-T01-ST01 — Define deterministic identity

Example:

```text
customer_id
+
issue_category
+
finding_type
```

Potential hash:

```text
SHA256(customer_id|issue_category|finding_type)
```

**Acceptance Criteria:**
Same business finding generates the same identity across sessions.

---

## G13-T02 — Duplicate detection

### G13-T02-ST01 — Search LTM

### G13-T02-ST02 — Search Jira

### G13-T02-ST03 — Compare evidence

### G13-T02-ST04 — Produce decision

```text
NEW
KNOWN
UPDATED
```

**Acceptance Criteria:**
The same finding cannot accidentally create duplicate Jira tickets because the wording of the user query changed.

---

# GOAL G14 — Build Jira MCP Server

## G14-T01 — MCP architecture

### G14-T01-ST01 — Define Jira MCP server

**Output:**
MCP server exposing Jira capabilities.

### G14-T01-ST02 — Define tool schemas

Required:

```text
jira.create_ticket
jira.update_ticket
jira.search_tickets
jira.search_tickets_by_category
jira.get_ticket
```

**Acceptance Criteria:**
All tools follow MCP tool contract.

---

## G14-T02 — Jira implementation

### G14-T02-ST01 — Implement CREATE

Input:

```text
project
issue_type
summary
description
labels
customer_id
issue_category
```

### G14-T02-ST02 — Implement UPDATE

### G14-T02-ST03 — Implement SEARCH

### G14-T02-ST04 — Implement CATEGORY SEARCH

### G14-T02-ST05 — Implement GET

**Acceptance Criteria for Jira tools:**

* Valid request → successful result.
* Invalid request → structured error.
* Jira key is returned for mutations.
* Tool never falsely reports success.

---

# GOAL G15 — Build Jira MCP Client and JiraOps

## G15-T01 — MCP client

### G15-T01-ST01 — Connect MCP client

### G15-T01-ST02 — Discover tools

### G15-T01-ST03 — Validate tool schemas

### G15-T01-ST04 — Invoke MCP tools

**Acceptance Criteria:**
No direct Jira REST/API call exists inside Scout or JiraOps.

---

## G15-T02 — JiraOps Agent

### G15-T02-ST01 — Convert Finding to Jira payload

**Input:**
Validated Finding.

**Output:**
JiraActionRequest.

### G15-T02-ST02 — Validate payload

### G15-T02-ST03 — Search existing Jira

### G15-T02-ST04 — Execute CREATE

### G15-T02-ST05 — Execute UPDATE

### G15-T02-ST06 — Execute SKIP

**Acceptance Criteria:**
JiraOps follows:

```text
Finding
 ↓
Evidence validation
 ↓
LTM check
 ↓
Jira search
 ↓
Decision
 ├── CREATE
 ├── UPDATE
 └── SKIP
```

---

# GOAL G16 — Implement Action Governance

## G16-T01 — Build Action Gate

### G16-T01-ST01 — Validate required information

**Input:**
Finding.

**Acceptance Criteria:**
Required business attributes exist.

---

### G16-T01-ST02 — Validate evidence

**Acceptance Criteria:**
Finding has at least one authoritative source.

---

### G16-T01-ST03 — Validate confidence

**Acceptance Criteria:**
Confidence meets configured threshold.

---

### G16-T01-ST04 — Check duplicate

**Acceptance Criteria:**
Existing finding/Jira relationship is considered before CREATE.

---

### G16-T01-ST05 — Produce action decision

```json
{
  "allowed": true,
  "decision": "CREATE",
  "reason": "..."
}
```

---

# GOAL G17 — Build Orchestrator

## G17-T01 — Runtime lifecycle

### G17-T01-ST01 — Initialize execution

### G17-T01-ST02 — Invoke Atlas

### G17-T01-ST03 — Validate plan

### G17-T01-ST04 — Resolve dependencies

### G17-T01-ST05 — Invoke Scout

### G17-T01-ST06 — Process StepResult

### G17-T01-ST07 — Invoke Action Gate

### G17-T01-ST08 — Invoke JiraOps

### G17-T01-ST09 — Persist final state

### G17-T01-ST10 — Generate final response

**Acceptance Criteria:**
A complete query can move from:

```text
QUERY
→ PLAN
→ EXECUTION
→ FINDING
→ ACTION
→ MEMORY
→ RESPONSE
```

without manual intervention.

---

# GOAL G18 — Observability, Audit and Traceability

This goal should be significantly stronger than the original plan.

## G18-T01 — Execution logging

### G18-T01-ST01 — Log run

Capture:

```text
run_id
query
timestamp
```

### G18-T01-ST02 — Log Planner

Capture:

```text
model
plan
prompt/version
latency
```

### G18-T01-ST03 — Log Executor

Capture:

```text
task
agent
tool
input
output
retry
confidence
```

### G18-T01-ST04 — Log Jira

Capture:

```text
MCP tool
action
jira_key
result
```

---

## G18-T02 — Memory audit

### G18-T02-ST01 — Log LTM recall

Mark:

```text
source_type = RECALLED
```

### G18-T02-ST02 — Log fresh retrieval

Mark:

```text
source_type = FRESH
```

### G18-T02-ST03 — Log memory promotion

Record why information moved:

```text
Working Memory
→ STM
→ LTM
```

**Acceptance Criteria:**
For any final answer, we can determine whether a statement came from:

* current retrieval
* previous step
* LTM
* Jira.

---

# GOAL G19 — End-to-End Testing and Acceptance

## G19-T01 — Test new actionable finding

### G19-T01-ST01 — Prepare deterministic test data

**Data required:**

```text
Reference ticket 4021
Similar customer tickets
Known churned customer
No existing Jira
No LTM finding
```

**Acceptance Criteria:**
Test fixture guarantees a new actionable finding.

---

### G19-T01-ST02 — Execute compound query

Example:

> Which customers had the same login issue as ticket 4021, and did any of them churn afterward?

**Acceptance Criteria:**
Planner generates multi-hop plan.

---

### G19-T01-ST03 — Validate execution trace

**Acceptance Criteria:**
Trace shows:

```text
STEP 1
STEP 2
STEP 3
...
```

with inputs, outputs and dependencies.

---

### G19-T01-ST04 — Validate Jira creation

**Acceptance Criteria:**

* Action Gate allows action.
* JiraOps is invoked.
* Jira CREATE happens through MCP.
* Correct Jira fields are populated.
* Jira key is returned.
* Jira relationship is stored in LTM.

---

# G19-T02 — Test memory and duplicate prevention

## G19-T02-ST01 — Execute first session

**Expected:**

```text
Finding = NEW
Jira = CREATE
LTM = STORE
```

---

## G19-T02-ST02 — Restart application

**Acceptance Criteria:**
LTM remains available after process restart.

This is important and was missing previously.

---

## G19-T02-ST03 — Execute related query

Example:

> What happened with the customer who had the login issue and churned?

**Acceptance Criteria:**
System retrieves previous finding from LTM.

---

## G19-T02-ST04 — Validate duplicate prevention

**Acceptance Criteria:**

```text
Existing finding = TRUE
Existing Jira = TRUE
New Jira CREATE = FALSE
```

---

## G19-T02-ST05 — Validate fresh vs recalled

Final response must distinguish:

```text
RECALLED:
Customer CUST-XXXX was previously identified...

FRESH:
No new matching customer was found...
```

---

# G19-T03 — Test missing information

## G19-T03-ST01 — Prepare incomplete fixture

Example:

```text
Customer exists
Login issue exists
Churn record unavailable
```

**Acceptance Criteria:**
Missing state is genuinely represented in source data.

---

## G19-T03-ST02 — Execute query

**Acceptance Criteria:**
Agent explicitly states information could not be found.

---

## G19-T03-ST03 — Validate no fabrication

**Acceptance Criteria:**
No unsupported churn status/date is generated.

---

## G19-T03-ST04 — Validate Jira action prevention

**Acceptance Criteria:**

```text
Evidence incomplete
       ↓
Action Gate BLOCKED
       ↓
JiraOps CREATE not called
       ↓
No Jira ticket
```

---

# G19-T04 — Failure testing

## G19-T04-ST01 — Retrieval failure

**Acceptance Criteria:**
Retry occurs only according to policy.

## G19-T04-ST02 — MCP unavailable

**Acceptance Criteria:**
System reports Jira action failure rather than success.

## G19-T04-ST03 — Invalid Planner output

**Acceptance Criteria:**
Invalid plan is rejected.

## G19-T04-ST04 — Model unavailable

**Acceptance Criteria:**
Model failure is explicit and does not result in fabricated output.

## G19-T04-ST05 — Memory unavailable

**Acceptance Criteria:**
System does not silently assume that no historical finding exists merely because LTM is unavailable.

This is particularly important for duplicate prevention.

---

# GOAL G20 — Documentation and Delivery

I would actually add this final goal to the project.

## G20-T01 — Technical documentation

### G20-T01-ST01 — Document architecture

### G20-T01-ST02 — Document agents

### G20-T01-ST03 — Document tools

### G20-T01-ST04 — Document MCP

### G20-T01-ST05 — Document memory architecture

**Acceptance Criteria:**
A developer unfamiliar with the project can understand and run the system.

---

## G20-T02 — Operational documentation

### G20-T02-ST01 — Setup instructions

Must include:

```text
Python version
dependencies
.env setup
model configuration
data setup
MCP startup
application startup
```

### G20-T02-ST02 — Troubleshooting guide

Include:

```text
model failure
MCP failure
Jira authentication failure
memory failure
embedding failure
dataset failure
```

---

# The Missing Data Layer

The most important addition I would make to the original plan is to explicitly treat **data as a first-class development dependency**.

Your agents cannot work merely because we have Python code and prompts.

We need:

```text
                    DATA
                     │
        ┌────────────┼─────────────┐
        ▼            ▼             ▼
     Tickets     Customers       Jira
        │            │             │
        ▼            ▼             ▼
 Semantic Index   Churn Data   Jira State
        │
        └──────────────┐
                       ▼
                    Agents
```

## Required datasets

### 1. Ticket dataset

At least:

```text
100 tickets
```

Fields:

| Field             | Required    |
| ----------------- | ----------- |
| ticket_id         | Yes         |
| customer_id       | Yes         |
| issue_category    | Yes         |
| issue_description | Yes         |
| resolution        | Yes         |
| resolution_status | Yes         |
| created_at        | Yes         |
| churn_status      | Yes/Unknown |
| churn_date        | Optional    |
| jira_key          | Optional    |

---

### 2. Customer dataset

```text
customer_id
customer_name
account_status
churn_status
churn_date
```

---

### 3. Jira test state

You need controlled Jira records for:

```text
NEW customer finding
EXISTING customer finding
EXISTING Jira ticket
UPDATED Jira ticket
```

---

### 4. Missing-data fixtures

At minimum:

```text
customer exists + issue exists + churn missing
customer exists + issue missing
ticket ID doesn't exist
customer ID doesn't exist
```

---

### 5. Semantic-search fixtures

You need paraphrases such as:

```text
"Unable to login"
"Cannot sign in"
"Authentication failing"
"Credentials rejected"
"User cannot access account"
```

These should map to the same conceptual issue category.

---

# Final Tool Registry

The development plan should ultimately produce this registry.

| Tool                              | Owner   | Purpose             | Side Effect   |
| --------------------------------- | ------- | ------------------- | ------------- |
| `ticket_get`                      | Scout   | Retrieve ticket     | No            |
| `ticket_search`                   | Scout   | Search tickets      | No            |
| `semantic_ticket_search`          | Scout   | Semantic matching   | No            |
| `customer_ticket_search`          | Scout   | Customer history    | No            |
| `churn_status_lookup`             | Scout   | Churn lookup        | No            |
| `churn_date_lookup`               | Scout   | Churn date          | No            |
| `ltm_search`                      | Memory  | Historical findings | No            |
| `ltm_store`                       | Memory  | Persist finding     | Yes, internal |
| `ltm_update`                      | Memory  | Update finding      | Yes, internal |
| `jira.get_ticket`                 | JiraOps | Get Jira            | No            |
| `jira.search_tickets`             | JiraOps | Search Jira         | No            |
| `jira.search_tickets_by_category` | JiraOps | Duplicate detection | No            |
| `jira.create_ticket`              | JiraOps | Create issue        | **Yes**       |
| `jira.update_ticket`              | JiraOps | Update issue        | **Yes**       |

---

# Agent-to-Tool Permission Matrix

This should also be an actual project artifact.

| Capability       |   Atlas |   Scout | JiraOps | Orchestrator |
| ---------------- | ------: | ------: | ------: | -----------: |
| Ticket retrieval |       ❌ |       ✅ |       ❌ |            ❌ |
| Semantic search  |       ❌ |       ✅ |       ❌ |            ❌ |
| Churn lookup     |       ❌ |       ✅ |       ❌ |            ❌ |
| STM read         | Limited |       ✅ | Limited |            ✅ |
| Working Memory   |       ❌ |       ✅ | Limited |            ✅ |
| LTM search       | Limited |       ✅ |       ✅ |            ✅ |
| LTM write        |       ❌ | Limited | Limited |            ✅ |
| Jira search      |       ❌ |       ❌ |       ✅ |            ❌ |
| Jira create      |       ❌ |       ❌ |       ✅ |            ❌ |
| Jira update      |       ❌ |       ❌ |       ✅ |            ❌ |
| Generate plan    |       ✅ |       ❌ |       ❌ |            ❌ |
| Execute plan     |       ❌ |       ✅ |       ❌ |            ✅ |

This permission matrix prevents one of the biggest agentic-system problems: **an LLM having more capability than its role requires.**

---

# Final Development Traceability

The entire Problem 18 should therefore trace like this:

```text
PROBLEM 18
│
├── G01 Requirements & Scope
│   ├── T01 Normalize requirements
│   │   ├── ST01 Functional requirements
│   │   ├── ST02 Non-functional requirements
│   │   └── ST03 Scope boundaries
│   └── T02 Acceptance model
│
├── G02 Agent Architecture
│   ├── T01 Atlas
│   ├── T02 Scout
│   ├── T03 JiraOps
│   └── T04 Orchestrator
│
├── G03 Environment & Configuration
│   ├── T01 Project structure
│   ├── T02 Dependencies
│   ├── T03 Model configuration
│   └── T04 Secrets/configuration
│
├── G04 Data Contracts
│   ├── T01 Plan schemas
│   ├── T02 Execution schemas
│   └── T03 Error schemas
│
├── G05 Ticket & Customer Data
│   ├── T01 Ticket dataset
│   ├── T02 Customer dataset
│   └── T03 Test fixtures
│
├── G06 Retrieval
│   ├── T01 Ticket tools
│   └── T02 Customer/churn tools
│
├── G07 Semantic Retrieval
│   ├── T01 Indexing
│   └── T02 Semantic search
│
├── G08 Atlas Planner
│   ├── T01 Prompt
│   └── T02 Implementation
│
├── G09 Scout Executor
│   ├── T01 Tool execution
│   ├── T02 Evidence evaluation
│   └── T03 Retry
│
├── G10 Short-Term Memory
│
├── G11 Working Memory
│
├── G12 Long-Term Memory
│
├── G13 Deduplication
│
├── G14 Jira MCP Server
│
├── G15 Jira MCP Client + JiraOps
│
├── G16 Action Governance
│
├── G17 Orchestrator
│
├── G18 Observability & Audit
│
├── G19 End-to-End Testing
│   ├── T01 New finding
│   ├── T02 Memory/dedup
│   ├── T03 Missing information
│   └── T04 Failure handling
│
└── G20 Documentation & Delivery
```

## One more important architectural distinction

I would now maintain **three separate registries** in the actual project:

### 1. Development WBS

```text
Goal → Task → Subtask → Acceptance Criteria
```

This is what we have defined above.

### 2. Runtime Task Registry

```text
TASK-RET-001
TASK-RET-002
TASK-MEM-001
TASK-JIRA-001
...
```

These are the **atomic capabilities Atlas can select at runtime**.

### 3. Runtime Tool Registry

```text
ticket_get
semantic_ticket_search
ltm_search
jira.create_ticket
...
```

The relationship becomes:

```text
Development Subtask
       │
       │ implements
       ▼
Runtime Task
       │
       │ uses
       ▼
Tool
```

For example:

```text
G06-T01-ST01
"Implement ticket_get"
        │
        ▼
Runtime Task: RET-001
"Retrieve ticket by ID"
        │
        ▼
Tool: ticket_get
```

And:

```text
G15-T02-ST04
"Execute CREATE"
        │
        ▼
Runtime Task: JIRA-CREATE-001
"Create Jira issue"
        │
        ▼
Tool: jira.create_ticket
        │
        ▼
MCP Server
        │
        ▼
Jira
```

**That three-level traceability is what I would use for the actual implementation.** It lets you answer, for any runtime Jira ticket created by the system:

> **Which business requirement → which development goal → which task/subtask → which runtime task → which tool → which MCP operation → which evidence caused this action?**

That is the level of traceability and operational detail I would expect for a genuinely workable **Problem 18 agentic system**, rather than just a conceptual multi-agent demo.
