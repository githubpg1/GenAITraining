Yes. This requirement is substantially more complex than Problem 16 because it is no longer just a **RAG/search system**. It is an **agentic orchestration system with tool use, MCP, multi-model routing, state management, persistent memory, and action governance**.

I would analyze Problem 18 as follows.

## 1. What the requirement is really asking for

At a high level, the existing architecture:

**User → Planner → Executor → Search/RAG → Answer**

needs to evolve into:

**User → Planner Agent → Executor Agent → Retrieval/Data Tools + Jira MCP → Jira Agent → Memory Layers → Final Response**

with **independent model configuration per agent**.

The five major additions are:

1. **Jira MCP integration**
2. **Third Jira Agent**
3. **Independent model routing**
4. **Three-layer memory architecture**
5. **Action-aware execution + duplicate prevention**

The important architectural shift is:

> The Executor is no longer only responsible for retrieving information. It must be capable of taking an action when the execution step produces an actionable finding.

---

# 2. Functional requirements

I would break the requirement into these functional requirements.

### FR-01 — Compound question decomposition

The system shall accept compound support questions and decompose them into ordered executable steps.

Example:

> "Which customers had the same login issue as ticket 4021, and did any of them churn afterward?"

Planner might generate:

```text
Step 1 → Retrieve ticket 4021
Step 2 → Identify its issue category
Step 3 → Find customers with the same issue category
Step 4 → Determine whether those customers subsequently churned
Step 5 → Check long-term memory for previously reported findings/actions
Step 6 → Determine whether a new actionable finding exists
Step 7 → Create/update Jira if required
```

The exact plan should be generated dynamically rather than hardcoded.

---

# 3. Jira MCP requirement

This is one of the most important changes.

The requirement explicitly says:

> "proper MCP connection to Jira, not a one-off API call bolted onto the Executor."

Therefore, **do not implement something like:**

```python
requests.post(jira_url, ...)
```

inside Executor.

Instead the architecture should look like:

```text
Executor Agent
      |
      v
MCP Client
      |
      v
Jira MCP Server
      |
      v
Jira
```

The Jira MCP Server should expose tools such as:

### Required MCP tools

| Tool                 | Purpose                             |
| -------------------- | ----------------------------------- |
| `create_ticket`      | Create a Jira issue                 |
| `update_ticket`      | Update an existing Jira issue       |
| `search_tickets`     | Search existing Jira issues         |
| `get_ticket`         | Retrieve a specific Jira issue      |
| `search_by_category` | Find existing issues for a category |

The requirement explicitly mentions:

* create ticket
* update ticket
* search existing tickets by category

I would still include `get_ticket`, because it is useful for update workflows and verification.

---

# 4. Important distinction: MCP Server vs MCP Client

This should be explicitly documented.

### Jira MCP Server

Responsible for exposing Jira capabilities as MCP tools.

```text
Jira MCP Server
 ├── create_ticket
 ├── update_ticket
 ├── search_tickets
 └── get_ticket
```

### MCP Client

Used by your agent system to discover/invoke those tools.

```text
Executor/Jira Agent
       |
       ↓
    MCP Client
       |
       ↓
 Jira MCP Server
       |
       ↓
     Jira
```

This separation is important because otherwise the implementation could technically work but fail the architectural intent of the requirement.

---

# 5. Third agent — Jira Agent

The requirement specifically says:

> "new Jira Agent handling ticket creation and updates"

So I would **not simply give Jira tools directly to a generic Executor and call that the Jira Agent**.

The architecture should contain three logical agents:

```text
                    ┌─────────────────┐
                    │  Planner Agent  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Executor Agent  │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        Retrieval Tools             Jira Agent
                                          │
                                          ▼
                                      MCP Client
                                          │
                                          ▼
                                    Jira MCP Server
```

### Planner Agent

Responsible for:

* understanding user intent
* decomposition
* ordering steps
* identifying dependencies
* defining expected outputs
* identifying whether an action may be required

### Executor Agent

Responsible for:

* executing individual plan steps
* retrieving data
* evaluating relevance
* retrying failed retrievals
* determining whether sufficient evidence exists
* passing actionable findings to Jira Agent

### Jira Agent

Responsible for:

* interpreting actionable Jira request
* checking whether an existing Jira issue exists
* deciding create vs update
* constructing Jira fields
* invoking Jira MCP tools
* returning Jira action result

---

# 6. Multi-model requirement

This is another critical architectural requirement.

The system must **not** have:

```python
MODEL = "some-model"
```

and then pass that same model to every agent.

Instead:

```text
                    Model Configuration
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Planner          Executor         Jira Agent
       Model             Model             Model
```

For example:

```yaml
planner:
  model: strongest-model

executor:
  model: smaller-model

jira_agent:
  model: lightweight-model
```

The actual model names should be configurable.

### Very important

I recommend **one central configuration file**, but with independent model entries.

For example conceptually:

```text
config/
   model_config.yaml
```

with:

```yaml
planner:
  model: ...

executor:
  model: ...

jira_agent:
  model: ...
```

The model names should **never be hardcoded in the agent Python files**.

This also satisfies your earlier requirement from Problem 16 that the model can be changed without modifying the source code.

---

# 7. Model selection philosophy

The requirement isn't asking merely for three different strings.

It is testing whether the architecture supports **model specialization**.

### Planner

Needs:

* strong reasoning
* planning
* decomposition
* dependency analysis
* structured output

Therefore:

**Strongest available model**

### Executor

Needs:

* classification
* relevance grading
* extraction
* retry decisions
* high-volume execution

Therefore:

**smaller/cheaper model**

### Jira Agent

Needs:

* structured field extraction
* category mapping
* create/update decision
* tool calling

Therefore:

**lightweight model**

The important design principle is:

> Agent capability should be independent of model identity.

You should be able to replace:

```text
Planner → Model A
```

with:

```text
Planner → Model B
```

without changing Planner implementation.

---

# 8. Three-layer memory architecture

This is probably the most important conceptual part of Problem 18.

Do **not** implement a single:

```python
memory = {}
```

The requirement explicitly demands three distinct memory semantics.

---

## Layer 1 — Short-Term Memory

### Scope

Current query/run.

### Contains

```text
User question
Plan
Completed steps
Step results
Current findings
Action candidates
Final response state
```

Example:

```json
{
  "query": "Which customers had the same login issue as ticket 4021?",
  "plan": [...],
  "completed_steps": [...],
  "findings": [...]
}
```

### Lifetime

One query execution.

### When cleared?

After the run completes.

---

# 9. Working Memory

This is different from short-term memory.

Working memory belongs to the **currently executing step**.

Suppose Step 3 is:

> Find customers with the same login issue.

Working memory could contain:

```text
Step ID: 3

retrieval_attempt_1
retrieval_attempt_2

partial_results
candidate_matches
relevance_scores
retry_reason
current_step_state
```

Then:

```text
Step 3 completed
       ↓
Working memory cleared
       ↓
Step 4 begins
       ↓
Fresh working memory
```

This requirement is very explicit:

> "it should never leak into the next step's context."

So this needs to be enforced architecturally, not merely mentioned in documentation.

---

# 10. Long-Term Memory

Long-term memory survives the current execution.

It should remember things such as:

```text
Customer X
Issue category = LOGIN_FAILURE
Finding = churned
Jira issue = SUP-1234
Action = ticket created
Timestamp = ...
```

Then a future query:

> "Did customer X have the login problem before?"

can retrieve the previous knowledge.

More importantly:

> "If the system already flagged a customer as a churn risk and created a Jira ticket for them last week, it must not create another ticket."

Therefore long-term memory needs **action history**, not merely conversational history.

---

# 11. Long-term memory should have structured records

I strongly recommend something conceptually like:

```json
{
  "memory_id": "MEM-001",
  "customer_id": "C123",
  "issue_category": "LOGIN_FAILURE",
  "finding": "Customer churned after login issue",
  "jira_issue_key": "SUP-1234",
  "action": "JIRA_CREATED",
  "created_at": "...",
  "source": "ticket_4021",
  "confidence": 0.94
}
```

This gives you deterministic duplicate detection.

---

# 12. Very important: Memory ≠ duplicate prevention by itself

I would explicitly separate:

### Memory retrieval

"What do we already know?"

from:

### Idempotency / deduplication

"Should I perform this action again?"

For example:

```text
New finding
    ↓
Search long-term memory
    ↓
Existing equivalent finding?
       │
    ┌──┴──┐
   YES    NO
    │      │
    ↓      ↓
No Jira   Create Jira
```

This is much safer than relying on an LLM to "remember" not to create duplicates.

---

# 13. Fresh vs remembered information

The final response should distinguish:

### Fresh finding

Information discovered during the current run.

### Recalled finding

Information retrieved from long-term memory.

For example:

```text
Fresh findings:
- Customer C123 experienced LOGIN_FAILURE.
- Customer C123 subsequently churned.

Previously known:
- Customer C123 was already flagged as a churn risk.
- Jira SUP-1234 was created on 2026-08-20.

Action:
- No duplicate Jira ticket created.
```

This directly satisfies the requirement:

> "show ... the difference between what long-term memory recalled versus what was found fresh"

---

# 14. Action should be evidence-driven

This is a critical safety/business rule.

The system should **never create Jira merely because the LLM thinks something sounds actionable**.

There should be an evidence chain:

```text
Raw data
   ↓
Retrieved evidence
   ↓
Executor validation
   ↓
Finding
   ↓
Required fields complete?
   ↓
Memory duplicate check
   ↓
Jira Agent
   ↓
MCP
   ↓
Jira
```

If required information is missing:

```text
Missing evidence
       ↓
NO Jira action
```

This directly addresses test case 3.

---

# 15. Test Case 1 — New finding

### Input

A compound question that produces a genuinely new actionable finding.

Expected flow:

```text
User
 ↓
Planner
 ↓
Plan generated
 ↓
Executor
 ↓
Retrieve ticket
 ↓
Identify issue category
 ↓
Find similar customers
 ↓
Check churn
 ↓
New churn finding discovered
 ↓
Search long-term memory
 ↓
No matching prior finding
 ↓
Jira Agent
 ↓
MCP Client
 ↓
Jira MCP Server
 ↓
create_ticket
 ↓
Jira issue created
 ↓
Persist finding + Jira ID in long-term memory
```

### Must verify

* Correct plan
* Correct step ordering
* Correct evidence
* Jira Agent invoked
* MCP used
* Correct Jira fields
* Jira issue actually created
* Memory updated

---

# 16. Test Case 2 — Same customer later

This test validates **persistent memory + idempotency**.

First session:

```text
Finding → churn risk
Jira → SUP-1234
Memory → stored
```

Later session:

```text
Related question
      ↓
Planner
      ↓
Executor
      ↓
Fresh retrieval
      +
Long-term memory lookup
      ↓
Existing finding detected
      ↓
Existing Jira SUP-1234 detected
      ↓
NO duplicate creation
```

Expected response should distinguish:

```text
Previously known:
Customer X had already been identified as a churn risk.
Existing Jira: SUP-1234.

Fresh:
No new evidence indicating a different churn event.

Action:
No new Jira ticket created.
```

This is an excellent test because it validates that memory is actually functional rather than just being a storage component that nobody uses.

---

# 17. Test Case 3 — Missing information

Example:

> "Which customers with ticket 4021's issue later churned, and what was their churn date?"

Suppose your data contains:

```text
Customer A → login issue
Customer A → churned
```

but does **not** contain:

```text
churn date
```

The agent must say:

```text
Customer A was identified as having the issue and subsequently churning,
but the available data does not contain a churn date.
```

It must **not** say:

```text
Customer A churned on June 14.
```

And importantly:

```text
No complete actionable evidence
          ↓
No Jira creation
```

This is an **anti-hallucination + action-gating test**.

---

# 18. Proposed architecture

I would recommend the following architecture for Problem 18:

```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Planner Agent   │
                 │ Strong Model      │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  Short-Term       │
                 │  Memory           │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  Executor Agent   │
                 │ Smaller Model     │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
       Retrieval       Working       Long-Term
         Tools          Memory         Memory
             │             │              │
             └─────────────┼──────────────┘
                           │
                           ▼
                  Actionable Finding?
                           │
                     ┌─────┴─────┐
                    NO           YES
                     │             │
                     ▼             ▼
                  Answer     Jira Agent
                              Lightweight
                                 Model
                                  │
                                  ▼
                              MCP Client
                                  │
                                  ▼
                           Jira MCP Server
                                  │
                                  ▼
                                Jira
                                  │
                                  ▼
                          Long-Term Memory
```

---

# 19. Components that should exist

I would expect the implementation to have roughly these logical components:

```text
project/
│
├── agents/
│   ├── planner_agent.py
│   ├── executor_agent.py
│   └── jira_agent.py
│
├── mcp/
│   ├── jira_mcp_server.py
│   └── jira_mcp_client.py
│
├── memory/
│   ├── short_term_memory.py
│   ├── working_memory.py
│   └── long_term_memory.py
│
├── tools/
│   ├── ticket_search.py
│   ├── customer_search.py
│   └── churn_lookup.py
│
├── config/
│   ├── model_config.yaml
│   └── application_config.yaml
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── executor_prompt.txt
│   └── jira_agent_prompt.txt
│
├── tests/
│   ├── test_new_finding.py
│   ├── test_memory_deduplication.py
│   └── test_missing_information.py
│
└── main.py
```

This is conceptual architecture; the exact structure should depend on what you already have from Problem 16.

---

# 20. Planner output should be structured

The Planner should not return free-form prose.

I recommend a schema similar to:

```json
{
  "query": "...",
  "steps": [
    {
      "step_id": 1,
      "description": "Retrieve ticket 4021",
      "tool": "ticket_search",
      "depends_on": []
    },
    {
      "step_id": 2,
      "description": "Identify issue category",
      "tool": "ticket_analysis",
      "depends_on": [1]
    },
    {
      "step_id": 3,
      "description": "Find customers with matching issue",
      "tool": "semantic_search",
      "depends_on": [2]
    },
    {
      "step_id": 4,
      "description": "Check churn status",
      "tool": "customer_churn_lookup",
      "depends_on": [3]
    },
    {
      "step_id": 5,
      "description": "Evaluate actionable findings",
      "tool": "memory_lookup",
      "depends_on": [4]
    },
    {
      "step_id": 6,
      "description": "Create or update Jira if required",
      "tool": "jira_agent",
      "depends_on": [5]
    }
  ]
}
```

This also makes Planner → Executor communication deterministic.

---

# 21. Executor output should also be structured

For each step:

```json
{
  "step_id": 4,
  "status": "completed",
  "evidence": [
    {
      "customer_id": "C123",
      "source": "customer_123.txt"
    }
  ],
  "finding": {
    "issue_category": "LOGIN_FAILURE",
    "churned": true
  },
  "confidence": 0.95,
  "actionable": true
}
```

This makes it possible for Jira Agent to consume **validated structured information**, rather than parsing Executor prose.

---

# 22. Jira Agent should have an action contract

For example:

```json
{
  "action": "CREATE",
  "customer_id": "C123",
  "issue_category": "LOGIN_FAILURE",
  "summary": "Customer C123 churned after login failure",
  "description": "...",
  "labels": [
    "support-followup",
    "churn-risk",
    "login-issue"
  ],
  "evidence": [
    "ticket_4021",
    "customer_C123"
  ]
}
```

Then Jira Agent:

```text
Validate fields
      ↓
Search existing Jira
      ↓
Create OR update
```

---

# 23. What should NOT be allowed

I would explicitly put these into the non-functional/design constraints.

### ❌ No hardcoded model names

```python
model="..."
```

inside agents.

### ❌ No direct Jira REST API from Executor

```python
requests.post(...)
```

### ❌ No single generic memory object

```python
memory = {}
```

### ❌ No Jira creation based purely on LLM inference

There must be evidence.

### ❌ No duplicate Jira creation

Must check long-term memory and/or Jira.

### ❌ No working-memory leakage

Step N's temporary state cannot automatically enter Step N+1.

### ❌ No hallucinated missing data

Missing information must be explicitly reported.

---

# 24. Non-functional requirements

I would add these even though the original requirement doesn't state them explicitly.

### NFR-01 — Configurability

Models must be independently configurable.

### NFR-02 — Observability

Every execution should produce traceable logs:

```text
Query
 → Planner
 → Plan
 → Step 1
 → Step 2
 → Memory lookup
 → Finding
 → Jira Agent
 → MCP tool
 → Jira result
```

### NFR-03 — Auditability

Jira actions should record:

```text
who/what triggered action
finding
evidence
timestamp
action
Jira issue ID
```

### NFR-04 — Idempotency

Repeated queries must not create duplicate issues.

### NFR-05 — Failure handling

If Jira/MCP fails:

```text
Finding discovered
      ↓
Jira action attempted
      ↓
MCP failure
      ↓
Do not pretend ticket was created
      ↓
Report action failure
```

This is particularly important.

---

# 25. What the evaluator is probably looking for

If this is an assignment/capstone, I would assume they are testing **architecture**, not merely whether the final answer is correct.

The evaluator should be able to see:

### 1. Multi-agent architecture

```text
Planner ≠ Executor ≠ Jira Agent
```

### 2. Multi-model architecture

```text
Planner Model ≠ Executor Model ≠ Jira Model
```

### 3. MCP architecture

```text
Agent → MCP Client → Jira MCP Server → Jira
```

### 4. Memory architecture

```text
Short-term
Working
Long-term
```

### 5. Actionability

```text
Finding → validation → Jira action
```

### 6. Persistent memory

```text
Session 1 → memory
Session 2 → recall
```

### 7. Idempotency

```text
Existing finding → don't duplicate
```

### 8. Grounding

```text
Missing data → explicitly say unavailable
```

---

# 26. Traceability matrix I recommend

For implementation, I would convert the requirement into something like this:

| ID    | Requirement                      | Component        | Evidence                       |
| ----- | -------------------------------- | ---------------- | ------------------------------ |
| FR-01 | Compound query planning          | Planner          | Generated plan                 |
| FR-02 | Step execution                   | Executor         | Execution trace                |
| FR-03 | Jira creation                    | Jira Agent + MCP | Jira issue                     |
| FR-04 | Jira update                      | Jira Agent + MCP | Updated issue                  |
| FR-05 | Jira search                      | MCP              | Search result                  |
| FR-06 | Independent models               | Model Config     | Config file                    |
| FR-07 | Short-term memory                | STM              | Run state                      |
| FR-08 | Working memory                   | Working Memory   | Step state                     |
| FR-09 | Long-term memory                 | LTM              | Persisted record               |
| FR-10 | Duplicate prevention             | LTM + Jira       | No duplicate                   |
| FR-11 | Fresh vs recalled                | Memory subsystem | Final trace                    |
| FR-12 | Missing information handling     | Executor         | Explicit missing-data response |
| FR-13 | No action on incomplete evidence | Action gate      | No Jira ticket                 |
| FR-14 | MCP-based Jira operation         | MCP              | MCP execution trace            |

---

# 27. One important ambiguity in the requirement

There is one thing I would **clarify before implementation**:

### What is the source of Jira?

Is the expectation:

**A. Real Jira instance**

```text
Actual Jira Cloud
```

or:

**B. Mock Jira**

```text
Mock Jira database/API
```

or:

**C. Local simulated Jira MCP server**

```text
Local MCP Server → mock Jira data
```

The requirement says "Jira via MCP", so if the environment provides Jira credentials, I would use a real Jira instance. Otherwise, a local/mock MCP server can demonstrate the architecture.

The important thing is that **the application should interact with Jira through MCP regardless of whether Jira itself is real or mocked**.

---

# 28. Another important architectural decision

I would also distinguish:

### Planner decides *what needs to happen*

from

### Executor decides *whether the step succeeded*

from

### Jira Agent decides *how to perform the Jira action*

This gives you clean separation:

```text
Planner
"What steps are needed?"

Executor
"Did we obtain sufficient evidence?"

Jira Agent
"What Jira operation should be performed?"
```

That separation will make the system much easier to explain in an architecture review/interview.

---

# 29. Final interpretation of Problem 18

I would summarize the entire requirement as:

> **Extend the existing Planner–Executor RAG system into a stateful multi-agent system capable of reasoning over multi-hop support data, taking evidence-driven actions through a Jira MCP server, routing different responsibilities to independently configurable models, and maintaining isolated short-term, step-scoped working, and persistent long-term memory with idempotent action handling.**

The core flow becomes:

```text
                USER QUESTION
                      │
                      ▼
               ┌─────────────┐
               │   PLANNER   │
               │ Strong LLM  │
               └──────┬──────┘
                      │
                      ▼
               SHORT-TERM MEMORY
                      │
                      ▼
               ┌─────────────┐
               │  EXECUTOR   │
               │ Smaller LLM │
               └──────┬──────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
       WORKING MEMORY     LONG-TERM MEMORY
              │                │
              └───────┬────────┘
                      │
                      ▼
              ACTIONABLE FINDING?
                      │
                ┌─────┴─────┐
                │           │
               NO          YES
                │           │
                │           ▼
                │     ┌─────────────┐
                │     │ JIRA AGENT  │
                │     │ Light LLM   │
                │     └──────┬──────┘
                │            │
                │            ▼
                │       MCP CLIENT
                │            │
                │            ▼
                │     JIRA MCP SERVER
                │            │
                │            ▼
                │          JIRA
                │            │
                └────────────┴──────►
                           │
                           ▼
                    LONG-TERM MEMORY
                           │
                           ▼
                     FINAL RESPONSE
```

**My recommendation:** don't start coding Problem 18 immediately. First freeze the **architecture + memory data contracts + Planner/Executor/Jira Agent contracts + MCP tool registry + model configuration + test scenarios**. Once those are fixed, the Python implementation becomes much less error-prone and, importantly, you'll be able to demonstrate every requirement individually rather than having one large agent script that happens to work.
