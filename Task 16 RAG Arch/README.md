# ey-agentic-ai-training-02
ey-agentic-ai-training-02


16. SDLC Delivery Manager Agent for Requirements-to-Release Governance
Build an SDLC governance agent that connects requirements, user stories, design documents, code, commits, test cases, defects, release notes, and change approvals. The agent should identify missing
traceability, summarize delivery status, flag scope creep, detect release-readiness gaps, and prepare
governance reports for sprint reviews, release boards, or client steering committees. Bonus: auto-generate
acceptance criteria and test scenarios from business requirements.
Objective: Improve delivery transparency and release confidence by creating an end-to-end intelligent
governance layer across the SDLC.
Learning takeaways: Requirements traceability, ALM integration, defect analytics, release-readiness scoring,
test coverage mapping, governance reporting, and delivery-risk prediction.


WORKFLOW Capstone

- Create Goal , Success Criteria and Workflow

- then create the above specific for your domain

- create tools for your project to achieve your goal

tool to get business requirment:::: 
boolean connect_to_confluence_tool(api/mcp server details);  : return true or false whether connected to confluence
search_brd_in_confluence(application_name)  :: return json with the requirement documents
format_brd(document) :: return formated req , analysis
boolean add_in_traceability(formatted_req) :: boolean whether added or not , and maintain traceability to be updated later


tool to get design documents:::: 
boolean chec_existing_session(api/mcp server details);  : return true or false whether connected to confluence
search_in_confluence(application_name,requirement_type)  :: return json with the requirement documents
format_doc_for_tracebaility(document, document type) :: return formated req , analysis, json
boolean add_in_traceability(formatted_req) :: boolean whether added or not , and maintain traceability to be updated later, find and map with the parent epic/ stories


- tools to get user stories

boolean connect_to_jira_tool(api/mcp server details);  : return true or false whether connected to jira
gather_user_stories(application_name)  :: return json file with all the user stories
boolean add_in_traceability(formatted_req) :: boolean whether added or not , and maintain traceability to be updated later
map_user_stories_with_requirements :: mark traceability of stories with requirements
give_output_percentage() - whether bus req and stories are mapped and how much percentage

--- tools to get test cases

boolean chec_existing_jira_session(api/mcp server details);  : return true or false whether connected to jira
gather_test_cases()  :: return json file with all the test cases, with the parent user stories
boolean map_in_traceability() :: boolean whether added or not , and maintain traceability to be updated later, map with equirement, user stories, with the test cases and design document constraints
map_user_stories_with_requirements :: mark traceability of stories with requirements
double give_output_percentage() - whether bus req and stories are mapped and how much percentage


---tools to get code, code commit

connect_with_github_tool(mcp server) : 
connect_repo_and_branch_name(repo,branch_name) : return boolean whether connected with branch
get_code_commits_for_connected_repo() : 
trace_code_with_traceability_matrix() : check code level - very hectic , and code commit check - might be flaky if code commit is not as per standard

or

check_existing_jira_connection()
check_code_commit_attached_to_userstory() : if not attached to each task , return back percentage attached


similary tools for defects(from jira) - map to requirement traceability , which defect mapped with what test case/ if defect solution is enhancement to the actual requirement then final traceability will change/ updated,
 release notes(from confluence) - learn how to map it with traceability,
  and change approvals(from confluence) - map new changes with traceability , stories, new tasks added on story level?, whether change approval not mapped to any story/ task epic/ requirement, create another line with empty parents

analyze_defect(defect_json) :: store in json , mapping of defect. defect bucketing, which user stories have highest defects. number of defects per user stories. 



  PHASE 2 (AGENT 2)
  identify_missing_traceability(trace_document) : store  json format of missin traceabiliyt of user stories, cases etc
  show_root_of_missing_traceability():: show the whole level structure from where traceability is missing
  show_scope_creep() : scope not preesent in the original requirement from defect should be shown. if not present in change approval. (whether approved change approval requirement will be considered as scope creep or extent in business requirement)

  add_change_approval_in_bus_requirement() :: if needed

  String summarie_delivery_status(List<Status>) : using percentage of scope creep, percentage of traceability missing(average), code miss average, percentage missing for each - stories to requirement, stories to test cases,  give final summary with all details

  boolean final_release_readines_score() ::  if percentage from above average < 90% , not release ready



PHASE 3(AGENT3)

Tools to prepare governance reports

String prepare_sprint_governance_reports() :: summarie the current status in sprint board, to do , defects, in progress, completed

String prepare_release_status() :: summarize release status mentioning traceability, reason, percentage from all the traces gaps, scope leak

String prepare_client_report_status()  :: summarize client report status final creating raid with date from all the tasks, and final color trend. summarise in 3 lines 


24 august
--- need to crate excel sheet, create planner, these are goals, , success criteria, connect tools with goals and what is the acceptance crtierai. 
breakdown tyour gols in to multiple tasks, what tolls they are going to use, and output expectation
-success factor achieves/ criteria, success factor percentage
- divide each goal in each task like we do in sprint, give weight to the task as well
, tool registry
--task will be in json  , and contract will be same which will be feeded into executor

--ANSWER
## Plan: SDLC Governance Capstone

Build the agent incrementally in sprint-sized goals, beginning with SDLC data modeling and ending with traceability analysis, risk detection, release scoring, and governance reporting.

### Goal 1 — Plan and model the SDLC

**Breakdown**
- Define project personas, workflow, and governance use cases.
- Identify artifact types: requirements, designs, epics, stories, tests, commits, defects, releases, and changes.
- Define common fields, IDs, relationships, evidence, and confidence levels.
- Create the Excel/project planner.

**Tools**
- `README.md`
- Excel or CSV planner
- Pydantic data models

**Success criteria**
- 100% of required artifact types are documented.
- Every task contains an owner, dependency, tool, expected output, acceptance criteria, and completion percentage.

**Output**
- Project plan
- SDLC data dictionary
- Traceability relationship model
- Initial project planner

---

### Goal 2 — Ingest and normalize SDLC data

**Breakdown**
- Load JSON, CSV, TXT, PDF, and DOCX files.
- Normalize all lifecycle artifacts into a common structure.
- Validate missing IDs, duplicate records, invalid types, and broken references.
- Create sample data for each artifact type.

**Tools**
- Document extraction from `Task 11 Document Summarize`
- CSV patterns from `Task 12 Relationship Manager REview`
- Mock Jira, Confluence, and GitHub adapters

**Success criteria**
- At least 95% of valid sample records are ingested successfully.
- 100% of invalid records are reported with a clear error reason.

**Output**
- Normalized SDLC dataset
- Ingestion summary
- Validation and error report

---

### Goal 3 — Build end-to-end traceability

**Breakdown**
- Map requirements to design documents and user stories.
- Map stories to test cases.
- Map code commits and pull requests to stories.
- Map defects, release notes, and changes to affected artifacts.
- Calculate mapping percentages and identify orphan records.
- Generate acceptance criteria and test scenarios from requirements.

**Tools**
- Jira, Confluence, and GitHub connector interfaces
- TF-IDF from `Task 3 TF IDF`
- Embedding and similarity logic from `Task 8 Word Embeddings`
- Classification and entity extraction from `Task 6 Five NLP`

**Success criteria**
- At least 90% requirements-to-story mapping coverage.
- At least 90% story-to-test coverage.
- At least 85% valid commit-to-story linkage.
- 100% of missing mappings are flagged.

**Output**
- Traceability matrix
- Coverage percentage report
- Orphan and missing-link report
- Generated acceptance criteria and test scenarios

---

### Goal 4 — Detect delivery risks and scope creep

**Breakdown**
- Analyze defects by severity, status, component, and affected story.
- Identify stories with unusually high defect counts.
- Find missing traceability and show the root cause.
- Compare changes and defects with the approved requirements baseline.
- Distinguish approved scope extensions from unapproved scope creep.

**Tools**
- Jira defect adapter
- Confluence release-note and change-approval adapter
- Traceability graph traversal
- Fact-validation patterns from `Task 12 Relationship Manager REview`

**Success criteria**
- At least 90% precision on seeded defect, traceability, and scope-creep scenarios.
- Every risk includes evidence, source IDs, reason, owner, and recommended action.

**Output**
- Defect analytics
- Missing-traceability root-cause report
- Scope-creep and change-impact report
- RAID/action items

---

### Goal 5 — Calculate release readiness and create reports

**Breakdown**
- Score requirements-to-story coverage.
- Score story-to-test coverage and test execution results.
- Score code/commit linkage.
- Include critical defects, approved changes, and release-note completeness.
- Generate sprint, release, and client governance reports.

**Tools**
- Deterministic scoring service
- OpenRouter service from `Task 10 Summarize`
- Structured prompts and Pydantic response validation
- Evidence validation from `Task 12`

**Success criteria**
- Release-readiness scoring is 100% deterministic.
- Overall readiness below 90% results in “Not Release Ready.”
- Green: at least 95%; Amber: 90–94%; Red: below 90%.
- 100% of required report sections are present.
- At least 95% of report fields are populated or marked “Not Available.”

**Output**
- Release-readiness scorecard
- Sprint governance report
- Release status report
- Three-line client steering report
- RAID/action log

---

### Goal 6 — Integrate, test, and demonstrate

**Breakdown**
- Connect ingestion, traceability, risk analysis, scoring, and reporting.
- Add mock integrations for environments without live credentials.
- Test valid and invalid mappings, duplicate IDs, missing approvals, critical defects, and scope changes.
- Document setup, assumptions, limitations, and demonstration steps.
- Update planner completion percentages.

**Tools**
- FastAPI or CLI patterns from `Task 10` and `Task 11`
- Automated tests
- Mock Jira, Confluence, and GitHub data
- Local NLP assets from Tasks 6–9

**Success criteria**
- At least 90% of seeded end-to-end scenarios produce the expected result.
- At least 90% of automated tests pass.
- Credentials are never exposed.
- Integration and model failures produce controlled, explainable errors.

**Output**
- Runnable prototype
- Automated test report
- Demo dataset and script
- Setup guide
- Architecture diagram
- Completed Excel/project planner

---

### Overall acceptance criteria

- All SDLC artifacts can be loaded and represented in one normalized model.
- Every traceability relationship includes status, evidence, and confidence.
- Missing links, scope creep, defects, and release gaps are clearly reported.
- Release readiness is reproducible and configurable.
- Reports include metrics, risks, evidence, owners, and recommended actions.
- The complete workflow runs successfully using mock data without live integrations.

### Dependencies

1. Goal 1 must be completed before implementation begins.
2. Goal 2 is required before traceability mapping.
3. Goal 3 is required before risk scoring and governance reports.
4. Goal 4 can run in parallel with the later part of Goal 3.
5. Goal 5 depends on Goals 3 and 4.
6. Goal 6 depends on all previous goals.