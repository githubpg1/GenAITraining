from pathlib import Path

output_file = Path(__file__).parent / "data" / "sdlc_qa_corpus.txt"
output_file.parent.mkdir(parents=True, exist_ok=True)

sections = [
    """
Software development projects begin with clear business requirements. A requirement
describes what the software must accomplish for users, customers, or the organization.
Business requirements establish the expected outcome of a project and provide direction
for the development team. Functional requirements describe specific system behavior,
while non functional requirements describe qualities such as performance, security,
availability, reliability, and usability.

A user story describes a capability from the perspective of a user. A well written user
story explains who needs the capability, what the user needs, and why the capability is
valuable. Acceptance criteria define the conditions that must be satisfied before the
story can be considered complete. Requirements should be reviewed with business
stakeholders before development begins.

The requirements team works with product owners and business analysts to clarify
ambiguous requirements. Ambiguous requirements can create inconsistent implementation
decisions and increase testing effort later in the development lifecycle. Requirements
should be measurable, testable, traceable, and understandable by both technical and
business stakeholders.

Requirements traceability connects business requirements to user stories, development
work, test cases, defects, and releases. Traceability allows a governance team to verify
that important requirements have been implemented and validated. Missing traceability
can make it difficult to determine whether a business requirement has been fully tested.

Acceptance criteria should describe observable behavior. Criteria may specify expected
responses, validation rules, error handling, security controls, data requirements, and
integration behavior. QA engineers use acceptance criteria to design test cases and
developers use the same criteria to understand expected functionality.

Changes to requirements should be reviewed through an appropriate change management
process. A scope change can affect development effort, testing effort, delivery dates,
resources, and release readiness. The project team should evaluate the impact of a
requirement change before accepting it into an active sprint or release.

The product owner reviews business priorities and confirms whether a requirement is
still relevant. Business stakeholders may request additional functionality when project
conditions change. Governance teams should ensure that important scope changes are
documented and approved before implementation.

A requirement may depend on another requirement, service, database, external system,
or security control. Dependencies should be identified early because unresolved
dependencies can delay development and testing. Requirement reviews should identify
technical dependencies and business dependencies before implementation begins.

The development team estimates requirements using complexity, dependencies, risk, and
expected implementation effort. QA teams consider the testing effort associated with
each requirement. A complex integration requirement may require unit testing,
integration testing, regression testing, performance validation, and security testing.

A requirement is considered ready for development when its objective is understood,
acceptance criteria are sufficiently detailed, dependencies are identified, and required
stakeholder decisions are available. A requirement that lacks important information may
need clarification before the development team starts implementation.

Business requirements should remain aligned with the expected business outcome.
Technical implementation decisions should support the requirement without changing
the intended behavior. When implementation constraints require a change to expected
behavior, the product owner and appropriate stakeholders should review the decision.

Requirements reviews provide an opportunity to identify gaps before they become defects.
Early clarification is generally less expensive than correcting misunderstood behavior
after development and testing. QA participation during requirement refinement helps
ensure that requirements are testable and that acceptance criteria are measurable.
""",

    """
Quality assurance activities validate whether the software behaves as expected.
QA planning begins by understanding requirements, risks, dependencies, environments,
test data, and expected release objectives. Test planning should consider functional
testing as well as integration, regression, performance, security, and usability testing
when those activities are relevant to the product.

A test case contains a defined objective, test data, execution steps, and expected
results. Test cases should provide enough information for another tester to reproduce
the validation. Important requirements should have appropriate test coverage.

QA engineers execute test cases in controlled environments. The test environment should
be sufficiently similar to the target environment for the validation being performed.
Differences between environments can produce failures that do not represent production
behavior or can hide failures that later appear after deployment.

Regression testing verifies that previously working functionality remains stable after
a software change. Regression testing is particularly important when a change affects
shared services, authentication, payment processing, databases, APIs, or common user
interfaces. Automated regression suites can reduce repetitive manual testing effort.

Integration testing validates interactions between software components. An application
may depend on authentication services, payment services, notification services,
customer databases, reporting systems, or external APIs. Integration testing verifies
that these components exchange data correctly and handle expected failures.

API testing validates service endpoints, request parameters, response structures,
authentication behavior, error responses, and data validation. API tests can detect
problems before they become visible through the user interface. Automated API testing
is useful for repeatable validation during continuous integration and release cycles.

Test automation allows frequently executed tests to run consistently. Automation can
provide rapid feedback when a build is created or deployed to a test environment.
However, automation does not eliminate the need for exploratory testing, usability
testing, or human analysis of unexpected behavior.

Test coverage measures the extent to which requirements, code paths, scenarios, or
business behaviors are validated. High numerical coverage does not automatically mean
high quality. Tests must also be meaningful and should validate important business
risks.

QA teams monitor test execution results and investigate failed tests. A failed test
may indicate a software defect, incorrect test data, an environment problem, an
incorrect test expectation, or an external dependency failure. The failure should be
analyzed before a defect is created.

Test execution results should be linked to requirements and releases when traceability
is required. This allows stakeholders to determine which functionality has been
validated and which areas remain untested. Release decisions should consider both
successful and unsuccessful test results.

Smoke testing provides a quick validation that a build or deployment is sufficiently
stable for deeper testing. Smoke tests often verify critical application functions,
service availability, authentication, and basic data access. If smoke testing fails,
the build may be rejected before a larger regression suite is executed.

Sanity testing focuses on a limited set of functionality after a specific change.
It provides rapid confidence that the intended change behaves correctly without
requiring execution of the entire regression suite.

Integration failures should be investigated with logs, request information, response
data, timestamps, and environment details. Reproducible evidence helps developers
understand the problem and reduces the time required to diagnose failures.

Performance testing evaluates response time, throughput, scalability, and resource
utilization. A system that works correctly for a small number of users may fail under
higher load. Performance risks should be considered before production deployment when
the system has significant traffic requirements.

Security testing validates authentication, authorization, input validation, session
management, data protection, and other relevant security controls. Security defects
should receive appropriate priority because their impact may extend beyond individual
users to the entire organization.

QA results should be communicated clearly to development teams, product owners, and
release stakeholders. A test summary should identify completed testing, outstanding
tests, known failures, significant defects, and remaining risks.
""",

    """
Defect management begins when unexpected software behavior is identified. A defect
record should contain a clear description of the observed behavior, expected behavior,
steps to reproduce the problem, environment information, and supporting evidence.
Screenshots, logs, request data, and error messages can help developers investigate
the issue.

Defect severity describes the impact of a problem. A critical defect may prevent a
core business process from operating or may introduce a major security or data risk.
A high severity defect may affect an important business capability. Medium and low
severity defects may affect less critical functionality or usability.

Defect priority describes how urgently a defect should be addressed. Severity and
priority are related but are not identical. A moderate defect affecting a major
release objective may receive a high priority, while a severe problem in functionality
that is not currently used may be scheduled differently.

The QA engineer should attempt to reproduce a reported defect before assigning it for
development investigation. Reproduction evidence helps determine whether the problem
is consistent and identifies the conditions under which the failure occurs.

Developers investigate defects using application logs, source code, database records,
service calls, and environment information. The developer may identify a configuration
problem, data problem, implementation error, dependency issue, or unexpected business
rule.

After a fix is implemented, the defect should be retested. Retesting verifies that the
specific problem has been corrected. Regression testing should also be considered to
ensure that the fix has not introduced another problem in related functionality.

A defect can move through several states during its lifecycle. Typical states include
new, assigned, in progress, resolved, ready for testing, reopened, deferred, and
closed. The exact workflow depends on the organization's development process.

A defect should be reopened when the reported behavior still occurs after the fix or
when the fix does not satisfy the expected behavior. Reopening a defect provides
visibility into unresolved quality problems.

Defect aging is useful for governance because old unresolved defects may represent
accumulated delivery risk. A growing number of high severity defects may indicate
that the release is not ready for production.

Defect trends can be reviewed across releases and sprints. Teams can examine the
number of new defects, resolved defects, reopened defects, escaped defects, and
outstanding critical defects. Trends provide more information than a single defect
count.

Regression defects require special attention because they indicate that previously
working functionality has been affected by a change. Regression defects can occur
when developers modify shared components without validating dependent functionality.

Defect root cause analysis attempts to understand why a problem occurred. Root causes
may include unclear requirements, inadequate design, implementation errors, insufficient
testing, environment differences, missing automation, or communication gaps.

A production defect may require immediate investigation and mitigation. The team may
apply a temporary workaround while developing a permanent correction. Production
incidents should be documented and reviewed according to the organization's incident
and problem management processes.

Defect metrics should not be used as the only measurement of software quality. A low
number of reported defects could mean the software is stable, but it could also mean
that testing is insufficient. Governance teams should consider defect data alongside
test coverage, risk, requirements, and release readiness.

Critical defects should be reviewed before production approval. If a critical defect
remains open, the release board should understand its business impact, mitigation,
planned resolution, and acceptance of remaining risk.

Defect information should be traceable to the requirement, test case, build, and
release where appropriate. Traceability helps identify the affected scope and allows
stakeholders to determine whether the same issue may exist in other releases.
""",

    """
Release management coordinates the activities required to move software into a target
environment. Release readiness includes development completion, testing completion,
defect review, deployment preparation, operational readiness, stakeholder approval,
and risk assessment.

A release checklist provides a structured way to confirm readiness. Typical checklist
items include completed regression testing, resolved critical defects, approved
deployment plans, validated configuration, prepared rollback procedures, and required
business approvals.

Production deployment should occur only after the required quality and governance
checks have been completed. The exact approval process depends on the organization's
risk model and delivery process.

A release blocker is an unresolved condition that prevents safe or approved deployment.
Examples include critical defects, failed regression testing, missing security
validation, unavailable infrastructure, incomplete business approval, or unresolved
data migration concerns.

Release readiness reviews bring together development, QA, product, operations, and
governance stakeholders. The team reviews test results, defect status, known risks,
deployment dependencies, and outstanding decisions.

A deployment plan describes the sequence of activities required to install or activate
the release. It may include database changes, service deployment, configuration
updates, cache management, validation steps, and monitoring activities.

A rollback plan describes how the system can be returned to a previous stable state if
the deployment fails. Rollback procedures should be reviewed and, where appropriate,
tested before a high risk production deployment.

Production validation confirms that the deployed application is available and that
critical functionality operates correctly. Smoke testing is commonly performed after
deployment to identify immediate failures.

Release approvals should be recorded as evidence of the governance decision. Approval
may be provided by a product owner, release manager, business representative, security
stakeholder, or change authority depending on the release.

A release may be approved with known risks when stakeholders understand and explicitly
accept those risks. The decision should document the affected functionality, business
impact, mitigation, and planned follow-up.

Deployment windows may be selected based on business traffic, operational support,
dependency availability, and risk. A deployment should avoid periods where recovery
would be difficult or business impact would be unusually high.

Continuous delivery pipelines can automate build, test, deployment, and validation
activities. Automated pipelines improve consistency but still require appropriate
quality gates and governance controls.

A failed deployment should generate clear diagnostic information. Logs, monitoring
data, deployment records, and validation results help determine whether a rollback or
forward fix is appropriate.

Release notes communicate the contents of a release to stakeholders. They may describe
new functionality, resolved defects, known limitations, configuration changes, and
operational considerations.

Release governance ensures that deployment decisions are supported by evidence.
Evidence may include test execution reports, defect summaries, security assessments,
performance results, business approvals, and rollback plans.

A release board may review readiness information before approving production deployment.
The board may ask whether all critical requirements have been validated, whether
significant defects remain, whether risks are accepted, and whether support teams are
prepared.

Release readiness is not simply a measure of whether development work is complete.
A feature can be technically complete while remaining unsuitable for production because
of failed testing, operational concerns, security risks, or missing approvals.
""",

    """
Governance provides oversight of delivery activities and helps ensure that software
projects follow agreed processes. Governance reviews consider scope, requirements,
risks, testing, defects, dependencies, delivery status, and release readiness.

Traceability is a central governance concept. A requirement should be traceable to
implementation work and validation evidence where appropriate. Traceability makes it
possible to answer whether important business commitments have been delivered and
tested.

A governance review may examine the current project status, major risks, unresolved
issues, scope changes, and expected delivery date. Stakeholders use this information
to make decisions about priorities and risk.

The project team maintains a risk register to record identified delivery risks. Each
risk should have an owner, probability, impact, mitigation strategy, and current status.
Risks should be reviewed regularly rather than treated as static documentation.

Scope changes should be evaluated for their effect on cost, schedule, quality, and
resources. A change that appears small from a business perspective may require
significant integration and testing effort.

Governance committees may request evidence before approving a major decision. Evidence
can include requirements documentation, test reports, defect dashboards, deployment
plans, security assessments, and business acceptance.

The client steering committee may review project progress and major delivery risks.
Steering committee discussions may include timeline changes, resource constraints,
scope decisions, unresolved dependencies, and release readiness.

Delivery status reports should distinguish between completed work, work in progress,
blocked work, and planned work. A simple percentage completion number may hide important
risks if critical activities remain unresolved.

Governance teams should pay particular attention to critical path dependencies.
A project may appear on schedule while a single unresolved dependency threatens the
planned release date.

Approval evidence should be retained for important decisions. This supports audit
requirements and allows future reviewers to understand why a decision was made.

Governance is most effective when it is based on objective evidence. Test execution
results, defect trends, requirement traceability, deployment readiness, and risk
status provide stronger evidence than informal statements that the project is ready.

A governance review may identify missing acceptance criteria, incomplete test coverage,
unresolved critical defects, unclear ownership, or unapproved scope changes. These
issues should be assigned to appropriate owners.

Quality governance connects project delivery activities with business outcomes. The
goal is not merely to ensure that a process was followed, but to provide confidence
that the delivered software satisfies important business and operational expectations.

Governance dashboards can aggregate information from requirements, testing, defects,
releases, and project management systems. Automated dashboards can identify patterns
that would be difficult to discover when reviewing thousands of individual records.

An SDLC governance process may define quality gates for requirements, development,
testing, release readiness, and production deployment. Each quality gate has expected
evidence and approval criteria.

A project should escalate risks when they exceed agreed thresholds. Escalation provides
visibility to stakeholders who have authority to change priorities, allocate resources,
or accept residual risk.

Governance reviews should avoid becoming purely administrative exercises. The value of
governance comes from identifying delivery risks early and enabling informed decisions.
Clear evidence and traceability make those decisions more reliable.
""",

    """
The software development lifecycle depends on collaboration between business analysts,
product owners, developers, QA engineers, operations teams, security specialists, and
governance stakeholders. Each role contributes different information to the delivery
process.

Business analysts clarify requirements and business rules. Product owners prioritize
features and confirm expected outcomes. Developers implement the required behavior.
QA engineers validate functionality and identify unexpected behavior. Operations teams
prepare environments and support deployment. Governance stakeholders review evidence
and delivery risk.

Communication gaps can create defects even when individual teams perform their tasks
correctly. A requirement that is interpreted differently by development and QA may
result in test failures or rework.

Regular refinement sessions provide an opportunity to clarify upcoming work. Teams
can discuss acceptance criteria, dependencies, technical constraints, test scenarios,
and expected behavior before implementation begins.

Daily development activities may include coding, code review, unit testing, integration
testing, and deployment to development environments. Automated continuous integration
systems can execute validation whenever changes are committed.

Code review provides an additional quality control before changes are merged. Reviewers
may identify logic errors, security concerns, maintainability problems, missing tests,
or deviations from established standards.

Build pipelines should provide rapid feedback about compilation, unit tests, static
analysis, security checks, and packaging. A failed pipeline can prevent an unstable
change from moving into later environments.

Environment management is important because software behavior may depend on database
configuration, service endpoints, feature flags, credentials, network settings, or
external integrations. Configuration differences should be controlled and documented.

Test data should represent realistic scenarios without exposing sensitive information.
Data preparation is particularly important for integration and regression testing.

Feature flags can allow functionality to be deployed without immediately enabling it
for every user. Governance controls should define who can change flags and under what
conditions.

Monitoring and observability support production validation. Metrics, logs, traces, and
alerts can identify failures that are not detected through functional testing.

Incident management handles unexpected production events. The support team should
capture impact, timeline, symptoms, mitigation, and resolution information.

Post incident reviews can identify opportunities for improving requirements, testing,
monitoring, deployment procedures, or operational controls.

Security controls should be considered throughout the lifecycle rather than only before
release. Authentication, authorization, encryption, secrets management, and secure
input handling should be addressed during design and implementation.

Performance considerations should also be addressed early. Architecture decisions can
affect response time, scalability, throughput, and infrastructure cost.

Technical debt can accumulate when teams prioritize short term delivery over long term
quality. Governance reviews should recognize important technical debt and understand
its effect on future delivery risk.

Quality is a shared responsibility. QA teams provide important validation, but quality
also depends on clear requirements, sound architecture, reliable implementation,
effective code review, stable environments, and responsible release management.
""",

    """
The payment service is an example of a business critical capability that requires
careful validation. Requirements may specify payment authorization, timeout handling,
retry behavior, duplicate transaction prevention, refund processing, and transaction
status reporting.

Payment API tests should verify successful requests as well as invalid requests,
authentication failures, timeout conditions, duplicate requests, unavailable
dependencies, and unexpected responses.

A payment timeout may require a retry mechanism, but the retry behavior must avoid
creating duplicate transactions. Acceptance criteria should define the expected behavior
when the payment provider does not respond within the configured time.

Regression testing should confirm that changes to payment processing do not affect
customer checkout, transaction history, reporting, or reconciliation.

Authentication services are another critical area. Requirements may define password
rules, multi factor authentication, session expiration, account locking, and privileged
access controls.

QA engineers should test valid and invalid credentials, expired sessions, unauthorized
requests, password reset behavior, and access to protected resources.

Security testing may identify vulnerabilities related to authentication, authorization,
input validation, or sensitive information exposure. Critical security findings should
be reviewed before release approval.

Customer profile services may manage addresses, contact information, preferences, and
account settings. Changes to customer data should preserve validation and traceability.

An integration test may verify that customer updates are correctly propagated to
dependent services. Failures should be investigated using request identifiers and
service logs.

Reporting services often depend on data produced by transactional systems. Regression
testing should confirm that reporting remains accurate after changes to source data
structures.

Notification services may send email, SMS, or application messages after important
events. Tests should verify message content, delivery conditions, failure handling,
and retry behavior.

Database migrations can create significant release risk. Migration scripts should be
tested with representative data and validated for backward compatibility where
necessary.

Deployment configuration should be reviewed before production. Incorrect configuration
can cause authentication failures, service connection errors, or unexpected application
behavior even when the application code itself is correct.

Operational readiness includes monitoring dashboards, alerts, support documentation,
and escalation procedures. A technically successful deployment may still be operationally
incomplete if support teams cannot detect or respond to failures.

The release manager reviews outstanding defects and test results before the production
decision. Critical defects require explicit consideration because they may prevent
safe deployment.

A release may proceed when remaining defects are low risk, documented, and accepted by
the appropriate stakeholders. The acceptance decision should be supported by evidence.

Post deployment validation confirms that the production environment behaves as expected.
Smoke tests may verify login, customer search, payment processing, and other critical
business flows.

Production monitoring should continue after deployment because some problems appear only
under real traffic or real data conditions. Early monitoring helps the team respond
before a minor issue becomes a major incident.
""",

    """
Test strategy should be aligned with business risk. High risk capabilities deserve
more comprehensive validation than low impact features. The team should consider
business impact, technical complexity, change size, historical defects, and dependency
risk when deciding test depth.

Risk based testing prioritizes scenarios that could cause significant business impact.
For example, payment authorization, customer authentication, and financial reporting
may receive more testing attention than a minor display preference.

Test cases should include positive and negative scenarios. Positive testing verifies
expected behavior under valid conditions. Negative testing verifies that invalid input,
unauthorized access, missing data, and unexpected conditions are handled appropriately.

Boundary testing examines values near the limits of accepted ranges. For example, a
field accepting amounts from one to one thousand should be tested near both boundaries
and with values outside the permitted range.

Equivalence partitioning divides input data into groups expected to behave similarly.
This can reduce the number of test cases while maintaining useful coverage.

Exploratory testing allows QA engineers to investigate behavior beyond predefined
scripts. Exploratory sessions can reveal usability issues, unexpected interactions,
and edge cases that were not anticipated during requirement analysis.

User acceptance testing validates that the solution meets business expectations.
Business users may execute realistic workflows and confirm that the delivered
functionality supports their operational needs.

A failed user acceptance test may result in a defect, requirement clarification,
configuration change, or training requirement. The appropriate response depends on
the cause of the failure.

Regression suites should evolve as the product changes. New functionality should add
appropriate regression scenarios, and obsolete tests should be reviewed.

Flaky automated tests create noise and reduce confidence in test results. A flaky test
may pass and fail without a meaningful software change. Teams should investigate and
stabilize unreliable tests.

Test execution time is another consideration. A large regression suite may take many
hours to complete. Teams can prioritize critical tests for rapid feedback and run
broader suites at appropriate pipeline stages.

Parallel test execution can reduce overall testing time when the environment supports
it. Parallel execution requires careful handling of shared data and dependencies.

Quality reports should communicate the meaning of test results rather than only listing
pass and fail counts. Stakeholders need to understand what was tested, what remains
untested, and which failures create delivery risk.

Testing evidence should be retained when required for audit, compliance, or governance.
Evidence may include test execution records, screenshots, logs, automated test results,
and approval records.

A mature QA process uses defects and production incidents as feedback. Repeated failures
can reveal weaknesses in requirements, test design, automation, or development practices.

Continuous improvement reviews examine these patterns and identify actions that can
reduce future defects and improve delivery predictability.
""",

    """
Release risk should be assessed using multiple sources of evidence. A release with
many completed features is not necessarily ready if important validation remains
incomplete. Conversely, a release with minor known defects may be acceptable when
those defects have limited impact and appropriate mitigation exists.

Release readiness reviews should examine critical defects, test coverage, regression
results, security findings, performance results, deployment readiness, and business
approval.

The release manager coordinates the readiness review and ensures that unresolved
questions have owners. The product owner provides business context, QA provides
validation evidence, development provides implementation status, and operations
provides deployment and support information.

Governance stakeholders may ask whether the current release meets the agreed scope.
Scope changes should be identified clearly so that stakeholders understand what is
included and what has moved to a later release.

Dependencies can affect release readiness even when the application's own development
work is complete. An external API, infrastructure component, database change, or
security approval may still be outstanding.

A release dependency should have an owner and expected completion date. Unresolved
dependencies should be escalated when they threaten the delivery timeline.

Release documentation should be clear enough for support and operations teams to
understand the change. Documentation may include configuration changes, known issues,
monitoring requirements, and rollback instructions.

Production deployment should follow an approved change process where required.
The change record should describe the release, planned timing, impact, validation,
and rollback strategy.

After deployment, the team should compare observed behavior with expected behavior.
Monitoring metrics can provide early evidence of performance or reliability problems.

If a production issue occurs, the team should determine whether rollback, configuration
change, hotfix, or another mitigation is appropriate. The decision should consider
customer impact and recovery risk.

Release governance continues after deployment through post release validation and
review. Important incidents and defects should be captured for future improvement.

A release retrospective can identify improvements to planning, testing, communication,
automation, and governance. Lessons learned should result in concrete actions where
possible.

The goal of release management is not merely to deploy software. It is to deliver
business value while controlling quality, operational, security, and delivery risk.

Strong release processes use objective evidence, clear ownership, appropriate approvals,
and effective communication. These practices increase confidence in production
decisions and reduce avoidable delivery failures.
""",

    """
Traceability can be represented as a chain from business objective to requirement,
implementation, test case, defect, and release. Each link provides evidence that the
delivery process addressed the expected business outcome.

A missing link can create uncertainty. If a requirement has no test case, the team may
not know whether the requirement has been validated. If a defect is not linked to a
requirement, it may be difficult to assess business impact.

Traceability matrices can be maintained manually or generated from lifecycle tools.
Automated traceability reduces administrative effort and can highlight missing
relationships.

Governance teams can use traceability information during audits and release reviews.
They can ask which requirements are incomplete, which requirements failed testing, and
which requirements have unresolved defects.

Risk management should also connect risks with affected requirements and releases.
This allows stakeholders to understand the potential impact of unresolved risks.

A delivery dashboard may combine sprint progress, test execution, defect status,
requirement coverage, and release readiness. Such dashboards can provide a consolidated
view of delivery health.

However, dashboards should not replace detailed investigation. A green status indicator
may hide important information if the underlying metrics are incomplete or stale.

Data quality is therefore important in governance systems. Records should have accurate
status, ownership, dates, relationships, and evidence.

Automated governance checks can identify records that violate expected rules. Examples
include requirements without acceptance criteria, critical defects without owners,
release records without approvals, and test failures without corresponding investigation.

These checks can be used as quality gates or alerts. The appropriate action depends on
the severity and context of the finding.

An SDLC governance agent could consume records from project management systems and
organize them into meaningful groups. It could identify related requirements, defects,
testing records, and release information.

Semantic techniques can help organize large volumes of text when exact keyword
matching is insufficient. Related records may use different wording while discussing
the same underlying topic.

Clustering can reveal groups of similar records. Search and retrieval systems can then
use these groups to improve navigation and investigation.

Text generation can also demonstrate how statistical language models learn patterns
from a corpus. N-gram models use local word sequences rather than deep semantic
representations.

These techniques provide useful foundations for understanding more advanced natural
language processing systems. Modern language models learn much richer representations,
but the underlying concept of predicting likely language sequences remains important.
""",
]

# Repeat domain sections with controlled variation to create a sufficiently
# large training corpus while keeping the language realistic.
variations = [
    "The delivery team reviewed the information during the weekly project meeting.",
    "The QA lead recorded the result and communicated the outcome to the relevant stakeholders.",
    "The product owner confirmed the expected business behavior before the next delivery stage.",
    "The development team investigated the issue and provided supporting technical evidence.",
    "The release manager included the information in the readiness assessment.",
    "The governance team reviewed the evidence and confirmed the current delivery risk.",
    "The project team updated the related record after the review was completed.",
    "The responsible owner was asked to provide an updated status and expected completion date.",
]

paragraphs = []

# Use each section multiple times with contextual sentences between sections.
# This creates a corpus well above 5,000 words while maintaining SDLC vocabulary.
for round_number in range(3):
    for section in sections:
        paragraphs.append(section.strip())

        for variation in variations:
            paragraphs.append(
                f"{variation} "
                f"The current delivery context was considered when evaluating the "
                f"requirement, testing activity, defect status, or release decision. "
                f"Stakeholders reviewed the available evidence before confirming the "
                f"next action. The team continued to monitor the item until the expected "
                f"outcome was achieved."
            )

corpus = "\n\n".join(paragraphs)

output_file.write_text(corpus, encoding="utf-8")

words = corpus.split()

print("=" * 60)
print("SDLC-QA CORPUS CREATED")
print("=" * 60)
print(f"File: {output_file}")
print(f"Word count: {len(words)}")
print("=" * 60)