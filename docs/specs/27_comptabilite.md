# Phase 1 Accounting Scope (Comptabilite)

## Purpose
Document accounting and finance-adjacent expectations for Phase 1 in a documentation-only scope. Establish consistent structures for invoices, bills, expenses, budget lines, payments, and attachments without implementing business logic.

## Scope
- Organization-scoped accounting records with mandatory project context; missions inherit project scope.
- Documentation of objects, lifecycles, permissions, audit expectations, exports (CSV/PDF), and minimal reporting.
- Alignment with glossary, domain model, multi-tenancy/security, RBAC, audit, API conventions, and identifiers/time contracts.

## Non-Goals
- Implementing payment processing, ledger posting, or reconciliation logic.
- Advanced accounting exports (no FEC, bank synchronization, URSSAF/GUSO automation, or tax filings).
- Cross-organization visibility or shared ledgers.
- Budget forecasting engines or automated accruals.

## Core Objects
- **Invoice (outgoing)**: Issued by the organization to clients for project or mission deliverables. Fields include organization_id, project_id, optional mission_id, client party, line items, currency, tax breakdown (descriptive only), totals, due dates, payment terms, and delivery references.
- **Bill (incoming)**: Vendor or subcontractor charge to the organization. Fields include organization_id, project_id, optional mission_id, vendor party, line items, currency, tax notes, totals, due dates, and payee instructions.
- **Expense**: Employee or collaborator spend tied to a mission or project. Fields include organization_id, project_id, mission_id, submitter, category, amount, currency, receipt reference, and reimbursement flag.
- **Budget line**: Planned allocation per project and optionally per mission. Fields include organization_id, project_id, optional mission_id, category, allocation amount, currency, effective period, and tags for reporting dimensions.
- **Payment**: Recorded settlement against invoices or bills. Fields include organization_id, project_id, payable/receivable reference, method, amount, currency, paid_on date, and external reference (e.g., transfer id).
- **Attachment**: Supporting documents (quotes, receipts, SOW excerpts). Fields include organization_id, project_id, linked object id/type, filename, content type, checksum, and storage location pointer.

## Status Lifecycle and Allowed Transitions
- **Invoice**: draft -> ready_for_review -> approved -> sent -> partially_paid -> paid -> closed. Cancellations: draft|ready_for_review|approved|sent -> cancelled (cannot revert). Partially_paid -> paid -> closed; closed is terminal.
- **Bill**: draft -> submitted -> approved -> scheduled_for_payment -> paid -> closed. Dispute: submitted|approved -> disputed -> approved|scheduled_for_payment once resolved. Cancel only from draft or submitted.
- **Expense**: draft -> submitted -> approved -> reimbursed -> closed. Rejected path: submitted -> rejected -> draft (resubmission) or closed. Reimbursed is final financial state; closed archives record.
- **Budget line**: planned -> approved -> active -> retired. Adjustments must create new active lines with version references; retired is terminal.
- **Payment**: recorded -> reconciled -> archived. Void path: recorded -> voided (terminal); reconciled cannot be voided.
- **Attachment**: uploaded -> linked -> archived. Deletion is forbidden; archived hides from active lists but preserves audit history.

## Project and Mission Linkage Rules
- Every invoice, bill, expense, budget line, payment, and attachment MUST include organization_id and project_id; mission_id is required when the record is driven by a mission deliverable or expense.
- No record may reference multiple projects; cross-project aggregation occurs only in reporting projections.
- Assignments and missions drive who can submit or approve expenses within their project scope; invoices and bills must cite the project delivery or contract reference.
- Budget lines define the authoritative linkage between planning estimates and mission execution; expenses and bills draw down against the active budget line for the same project/mission/category.

## Exports (CSV/PDF) In Scope
- Export paths are read-only and scoped by organization and project filters (optionally mission, date range, category, status).
- Supported exports: invoice register, bill register, expense submissions, budget line catalog with consumption deltas, payment register with reconciliation markers.
- PDFs must include watermarking and page footers referencing organization, project, mission (if present), generated_at timestamp (UTC), and version hash. CSV exports must include identifiers and version columns.

## Minimal Reporting (KPIs) In Scope
- Accounts receivable aging by project and client (draft and sent excluded from aging buckets).
- Accounts payable aging by project and vendor.
- Budget burn vs allocation per project and mission, including variance percentages.
- Expense reimbursement queue by project/mission and submitter.
- Payment status dashboard (recorded vs reconciled) per project.
- Export summary counts (records per status) to confirm audit completeness.

## Permissions Model (Roles)
- **org_owner/org_admin**: May configure accounting settings, approve invoices, bills, budget lines, and mark payments as reconciled across the organization; may delegate project-level permissions.
- **project_manager**: May create and update invoices, bills, expenses, and budget lines for projects they manage; may approve within project scope; cannot override organization-wide settings.
- **planner**: May draft invoices and bills, create budget lines, and review expenses within assigned projects; requires project_manager or above for approvals.
- **member**: May submit expenses with mission/project linkage; cannot approve or issue invoices/bills.
- **viewer**: Read-only access limited to assigned organization and project contexts.
- All actions enforce default-deny, require organization_id and project_id context, and follow evaluation order from docs/specs/08_rbac_model.md.

## Audit and Trace Expectations
- Creation, updates, approvals, status transitions, exports, and attachment uploads MUST emit audit events capturing actor, organization_id, project_id, mission_id (if present), previous/new status, amounts, and checksum/version metadata.
- Payment records must log source reference, reconciliation timestamp, and correlation ids to invoices/bills.
- Export actions must log filters, record counts, and generated file references; deletion of exports is forbidden.

## Future Extensions (Out of Scope)
- Automated tax calculation, withholdings, or jurisdiction-specific compliance flows.
- Bank, card, or payroll system synchronization.
- Automated dunning, cash application, or multi-currency revaluation logic.
- Regulatory audit packages (FEC or equivalents) and automated submission to authorities.
