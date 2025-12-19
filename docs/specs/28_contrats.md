# Phase 1 Contracts Scope

## Purpose
Define contract documentation for Phase 1 to keep client, vendor, artist, and intermittent (CDDU) agreements consistent with project-centric rules. Establish lifecycle, template, and audit expectations without implementing contract automation.

## Scope
- Organization-scoped contracts with mandatory project linkage; missions and assignments inherit project scope.
- Contract types: intermittent (CDDU), artist, vendor, client.
- Common fields, parties, amounts, schedules, status lifecycle, template usage, storage, versioning, and attachment rules.
- Permissions, audit/traceability, and export expectations aligned to Phase 1 conventions.
- Aligns with ADR docs/specs/adr_assignment_first_contract_derived.md to keep assignments as the atomic cost/audit unit with contracts derived from assignment data.

## Non-Goals
- Automated signature workflows, payment processing, or legal compliance automation.
- Cross-organization contract visibility or shared repositories.
- Advanced legal exports or regulatory submissions.

## Assignment-Derived Semantics
- Assignments remain the atomic unit for planning, costing, and audit; contracts only aggregate derived values from linked assignments.
- Contracts reference one or more assignments inside the same project and organization; no cross-project or cross-organization linkage is allowed.
- Each assignment may be linked to at most one contract to prevent double counting; uncontracted assignments remain valid for planning but can raise completeness warnings.
- Contracts cannot override assignment-derived fields (dates, role, rate model, mission_id, project_id, org_id); totals and schedules remain derived views.

## Contract Types and Core Fields
- **Intermittent (CDDU)**: Organization <-> collaborator for mission-based engagements; fields include organization_id, project_id, mission_id, collaborator identity, engagement dates, role, rate model, total amount, working time windows, and applicable clauses.
- **Artist**: Organization <-> artist for creative delivery; fields include organization_id, project_id, optional mission_id, deliverables, exclusivity windows, royalties/fees, territory, and usage rights.
- **Vendor**: Organization <-> supplier or subcontractor; fields include organization_id, project_id, optional mission_id, scope of work, deliverables, SLAs, rate card, currency, tax notes, and invoicing schedule.
- **Client**: Organization -> client; fields include organization_id, project_id, optional mission_id, deliverables, milestones, acceptance criteria, payment schedule, currency, and change control rules.
- **Common fields**: contract_id, title, parties, contacts, effective date, start/end dates, governing law (descriptive only), termination clauses, renewal terms, attachment references, signatures (metadata), and status.

## Status Lifecycle and Allowed Transitions
- Base lifecycle: draft_preview (non-legal) -> under_review -> approved -> sent -> signed -> active (issued) -> completed -> archived. Termination path: active -> terminated -> archived; rejection path: under_review|sent -> rejected -> draft_preview for redraft.
- Active/issued status is allowed only after explicit assignment acceptance; pre-acceptance drafts and sent/signed previews remain non-legal and must not trigger payments or legal notices.
- Amendments: active|signed -> amendment_draft -> amendment_under_review -> amendment_signed -> active (new version) -> archived (previous version). Only one active version per contract per project/mission.
- Suspension: active -> suspended -> active|terminated. Suspended contracts cannot accrue new assignments or invoices until reactivated.

## Template, Storage, and Versioning
- Templates are referenced by id and version; generation may produce a draft_preview contract with pre-filled fields tied to project/mission/assignment identifiers without creating a legal artifact until acceptance gates are met.
- Storage keeps immutable versions; each revision increments version_number and captures checksum and generated_at timestamps.
- Signed PDFs and attachments are stored as linked artifacts with organization_id, project_id, contract_id, filename, content type, and checksum; deletions are forbidden, only archival is allowed.

## Linkage Rules to Project, Mission, and Assignment
- Every contract requires organization_id and project_id; mission_id is required when the contract covers a specific mission deliverable or assignment.
- Assignments reference the active contract version for the mission; no assignment may reference multiple contracts, and contracts must stay within one project/org.
- Invoices and bills must cite the contract_id and version when derived from contract deliverables.
- No cross-project or cross-organization references; read-only projections may aggregate at the organization level without exposing cross-organization data.

## Upload and Attachment Rules
- Allowed attachments: signed PDF, statements of work, insurance certificates, rate cards, identity documents (where permitted), and compliance attestations.
- Metadata required: uploader, organization_id, project_id, contract_id, file name, content type, size, checksum, created_at, and version linkage.
- Attachments follow lifecycle uploaded -> linked -> archived; removal is forbidden to preserve audit integrity.

## Permissions Model (Roles)
- **org_owner/org_admin**: Create, approve, send, and archive contracts across the organization; manage templates and version retention.
- **project_manager**: Create and update draft contracts, initiate review, send for signature, and mark signed/active within managed projects.
- **planner**: Draft contracts using templates, attach supporting documents, and propose amendments; cannot approve or sign-off.
- **member**: Read-only access to contracts tied to their assignments; may upload required personal documents for CDDU under project scope.
- **viewer**: Read-only access limited to assigned organization and project contexts.
- Default-deny enforcement with organization_id and project_id required on every action; approval and activation require explicit role permissions per docs/specs/08_rbac_model.md.

## Audit and Trace Expectations
- Record all lifecycle transitions with actor, previous/new status, organization_id, project_id, mission_id (if applicable), contract_id, version, timestamps, and correlation ids to assignments or invoices.
- Log template selection, generated draft references, and attachment uploads with checksums.
- Signature capture stores signer identity metadata, signature timestamp, and storage pointer; no embedded signatures are stored in cleartext.

## Future Extensions (Out of Scope)
- E-signature provider integrations, automated reminders, or dunning flows.
- Clause libraries with rule-based assembly or jurisdiction-specific compliance engines.
- Payment escrow, royalties accounting, or automated revenue recognition.
