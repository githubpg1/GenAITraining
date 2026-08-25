from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

ROOT = Path(__file__).parent
styles = getSampleStyleSheet()
body = styles["BodyText"]
heading = ParagraphStyle("PolicyHeading", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6)

POLICIES = [
    ("documents/current/employee_time_off_policy_2026.pdf", "Employee Time Off Policy", "Version 3.0", "January 1, 2026", [
        ("1", "Purpose and Scope", "This policy defines paid annual vacation and personal time for regular full-time employees. It applies to employees working in all company offices unless a local statutory rule or signed employment agreement provides a greater entitlement. Medical leave, parental leave, and public holidays are governed by separate policies."),
        ("2", "Eligibility and Accrual", "Employees begin accruing vacation on their employment start date and may schedule accrued time after completing the 30-day onboarding period. Vacation is credited at the beginning of each calendar year. Employees joining during the year receive a prorated balance based on their start month. Part-time and temporary employees follow the entitlement in their written agreement."),
        ("3.1", "Annual Vacation Entitlement", "Eligible employees receive 20 paid vacation days per calendar year. Vacation is taken in half-day or full-day increments. Employees should check their available balance in the HR portal before submitting a request."),
        ("3.2", "Request and Approval Procedure", "Submit a vacation request in the HR portal at least 10 business days before the planned start date. The line manager must approve the request before travel or other non-refundable arrangements are made. Approval depends on staffing needs and does not guarantee approval during restricted business periods."),
        ("3.3", "Carry Forward and Expiry", "Up to 5 unused vacation days may be carried into the next calendar year and must be used by March 31. Days above 5 expire on December 31 unless HR has approved a written exception because of business-directed deferral or applicable law."),
        ("3.4", "Cancellation and Separation", "A manager may ask an employee to reschedule approved vacation only for a documented business emergency. Employees should cancel changed plans in the HR portal. At separation, unused accrued vacation is handled according to applicable law and payroll procedures."),
        ("4", "Exclusions and Contacts", "This policy does not define medical leave, parental leave, disability accommodation, or benefits eligibility. Contact HR Operations for balance corrections or policy interpretation and contact the line manager for scheduling decisions."),
    ]),
    ("documents/historical/employee_time_off_policy_2025.pdf", "Employee Time Off Policy", "Version 2.0", "January 1, 2025", [
        ("1", "Purpose and Applicability", "This version governed eligible regular full-time employees from January 1, 2025 through December 31, 2025. It is retained for historical questions and does not replace the current Employee Time Off Policy."),
        ("2.1", "Annual Vacation Entitlement", "During the 2025 policy period, eligible employees received 18 paid vacation days per calendar year. Employees joining during the year received a prorated balance. Vacation was taken in half-day or full-day increments."),
        ("2.2", "Request and Approval", "Employees submitted vacation requests through the HR portal at least 10 business days before the planned start date. The line manager had to approve the request before the leave began."),
        ("2.3", "Carry Forward", "Up to 5 unused vacation days could be carried into 2026 and were expected to be used by March 31, 2026. This historical rule was superseded by Version 3.0 effective January 1, 2026."),
        ("3", "Policy Change Record", "Version 3.0 increased the annual entitlement from 18 to 20 days for the 2026 policy period. Questions about 2025 must use this Version 2.0 document."),
    ]),
    ("documents/current/business_travel_expense_policy_2026.pdf", "Business Travel and Expense Policy", "Version 1.0", "January 1, 2026", [
        ("1", "Purpose, Scope, and Authorization", "This policy covers reasonable and necessary expenses incurred during approved business travel. Obtain written manager approval before booking transportation or lodging. Personal travel, commuting, upgrades, fines, and expenses for unapproved guests are not reimbursable."),
        ("2.1", "Transportation", "Book the lowest logical economy airfare or standard rail fare through the approved travel channel. A business-class exception requires director approval before booking. Reasonable local transportation between the airport, hotel, and business location is reimbursable with an itemized receipt."),
        ("2.2", "Hotel Reimbursement", "The standard hotel reimbursement limit is 200 USD per night before applicable taxes. Use the company's preferred hotels when available. A higher rate requires written pre-approval from the department director and must be explained in the expense report."),
        ("2.3", "Meal Reimbursement", "Eligible employees may claim up to 75 USD per travel day for business meals, including applicable taxes and gratuity. Alcohol, personal entertainment, and meals for unapproved guests are not reimbursable. Meals provided by the conference or host must be deducted from the daily claim."),
        ("3.1", "Receipts and Documentation", "Itemized receipts are required for individual expenses of 25 USD or more. Each claim must include the business purpose, dates, location, attendees when applicable, and the related manager approval. A lost receipt requires a signed declaration and finance approval."),
        ("3.2", "Submission Deadline and Reimbursement", "Submit the completed expense report through the finance portal within 30 calendar days after returning from travel. Finance reviews policy compliance and normally processes approved reports in the next payroll cycle. Returned reports must be corrected and resubmitted."),
        ("4", "Exceptions and Fraud Prevention", "Exceptions must be approved in writing before the expense is incurred unless an emergency makes advance approval impossible. Falsified, duplicated, or personal claims may be rejected and referred for disciplinary review."),
    ]),
    ("documents/current/parental_leave_policy_2026.pdf", "Parental Leave Policy", "Version 2.1", "January 1, 2026", [
        ("1", "Purpose and Eligibility", "This policy provides job-protected parental leave for the birth, adoption, or placement of a child. Regular employees who have completed 12 months of continuous service may request leave. Statutory entitlements that are more favorable than this policy continue to apply."),
        ("2.1", "Leave Duration", "Eligible employees may take up to 16 weeks of parental leave for each qualifying event. HR confirms the available entitlement and whether local law requires a different duration or payment treatment."),
        ("2.2", "Request Procedure", "Submit the parental leave request and supporting documentation to HR at least 30 days before the planned leave where reasonably possible. The request should state the proposed start date, expected return date, and whether the leave will be taken continuously or in approved blocks."),
        ("3", "During Leave and Return", "Employees must keep HR informed of changes to the expected return date. HR and the manager will coordinate the return-to-work plan and any legally required accommodations. Employees should not perform regular work while on approved parental leave unless HR has authorized a transition activity."),
        ("4", "Benefits and Contacts", "Benefit continuation, pay, and interaction with vacation or medical leave depend on the applicable plan and local law. HR is the authoritative contact for an individual eligibility determination; managers should not promise an entitlement outside this policy."),
    ]),
    ("documents/current/employee_benefits_policy_2026.pdf", "Employee Benefits Policy", "Version 4.0", "January 1, 2026", [
        ("1", "Eligibility and Enrollment", "Regular full-time employees may enroll in eligible company benefit plans during the annual enrollment period or within 30 days of a qualifying life event. Coverage begins on the date shown in the plan confirmation, not necessarily on the employment start date."),
        ("2.1", "Medical Coverage", "Eligible employees may enroll in the company medical plan and may select available dependent coverage. Premiums, deductibles, covered services, and exclusions are defined in the insurer's plan documents and the benefits portal."),
        ("2.2", "Dental and Vision Coverage", "Eligible employees may enroll in available dental and vision plans during the applicable enrollment window. Claims and coverage questions should be directed to the plan administrator using the contact details in the benefits portal."),
        ("2.3", "Retirement Plan", "Eligible employees may contribute to the company retirement plan according to the plan administrator's enrollment rules. Contribution rates, vesting, and any company contribution are governed by the current plan document rather than this summary."),
        ("3", "Qualifying Life Events", "Marriage, divorce, birth or placement of a child, loss of other coverage, and similar events may create a special enrollment window. Submit supporting documentation through the benefits portal within 30 days of the event unless the plan document states a different deadline."),
        ("4", "Eligibility Changes and Contacts", "Benefits eligibility can change when employment status, work location, or employment ends. Contact HR Benefits for a current plan summary and contact the plan administrator for claim decisions. This policy does not promise benefits not described in the applicable plan documents."),
    ]),
]

for relative, title, version, effective, sections in POLICIES:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.7*inch, leftMargin=0.7*inch)
    story = [Paragraph(title, styles["Title"]), Paragraph(f"{version} | Effective date: {effective}", body), Spacer(1, 12)]
    for number, section, text in sections:
        story += [Paragraph(f"{number} {section}", heading), Paragraph(text, body)]
    doc.build(story)
    print(path)
