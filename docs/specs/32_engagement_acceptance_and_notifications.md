# Phase 1 Spec 32 - Engagement, Acceptance, Reminders, and Audit Timeline

## 1. Purpose
- Lock the engagement ladder and acceptance rules for missions and assignments without introducing business logic or irreversible automation.
- Provide a declarative model for reminders, escalations, and execution documents so production teams can coordinate while respecting organization security boundaries.
- Deliver traceable engagement timelines and audit coverage that align with Phase 1 contracts for multi-tenant safety, planning coherence, and non-regression.

## 2. Definitions
- Mission: execution unit scoped to one project and organization that bundles work, schedule, and collaborators.
- Assignment: atomic planning unit that links a collaborator to a mission with role, dates, and expected workload.
- Engagement: end-to-end coordination flow from proposal to closure for a mission and its assignments.
- Acceptance: explicit human decision (accept or decline) captured for a mission and, optionally, each assignment.
- Reminder: scheduled, non-blocking notice that a required action or document is missing.
- Escalation: declarative reassignment of reminder responsibility (e.g., to production or direction) when pending items remain.
- Execution Document: non-legal artifact (attachment or metadata) linked to mission and assignments to prove execution.
- Engagement Event: any auditable state change or document action recorded on the engagement timeline.

## 3. Engagement Ladder (state machine)
- States: planned, proposed, accepted, confirmed, executed, closed, canceled.
- Allowed transitions:
  - planned -> proposed (production creates proposal with assignments and required documents)
  - proposed -> accepted (explicit acceptance by collaborator or mission owner)
  - accepted -> confirmed (production confirms when all required assignments are accepted or conditionally accepted)
  - accepted -> canceled (proposal withdrawn before confirmation)
  - confirmed -> executed (mission delivered with evidence ready for validation)
  - executed -> closed (documents validated and no pending reminders)
  - proposed/accepted/confirmed -> canceled (mission no longer valid)
- State meaning and actors:
  - planned: draft mission prepared by production; only production edits.
  - proposed: invitations/reminders enabled; production manages updates and reminders.
  - accepted: collaborator or mission owner records explicit accept/decline; production can re-propose after decline.
  - confirmed: production validates readiness (all critical assignments accepted or conditionally accepted) and publishes execution timeline.
  - executed: mission completed; production uploads or requests execution documents.
  - closed: production or direction marks completion after document validation; audit trail finalized.
  - canceled: production or direction cancels; timeline records rationale and timestamp.
- Partial acceptance: mission may be in accepted state while specific assignments remain pending; confirmation requires all required assignments marked accepted or accepted_with_conditions.
- Constraints: no cross-organization transitions; project is the functional boundary; reminders and transitions are declarative with no automatic irreversible effects.

## 4. Acceptance Model
- Explicit acceptance required via user action; no implicit acceptance on timeouts.
- Recorded fields: actor_id, timestamp, decision (accept/decline), optional comment.
- Conditional acceptance: decision accepted_with_conditions plus condition text; visible to production and direction and displayed on mission timeline.
- Expiration: proposal_expires_at stored per mission/assignment; when expired, mission/assignment reverts to planned or stays in proposed with status "expired" until re-proposed.
- Decline flow: decline keeps mission visible; production can re-propose after addressing comments; history preserved in audit journal.
- No legal enforcement: acceptance is an engagement signal only; no contract signature or payroll computation triggered.

## 5. Reminders and Escalations (declarative)
- Reminder types: acceptance_missing, contract_expected, document_missing_post_mission.
- Schedule rules (examples): J-7, J-3, J-1 before execution start; J+1 after execution for missing documents.
- Escalation ladder: assign_to production on first miss; escalate_to direction after repeated misses or post-expiration.
- Behavior: reminders and escalations create warnings and timeline events only; they do not block transitions or trigger payments.
- Delivery channel governance defers to docs/specs/21_notifications_and_messaging_contracts.md; if channels are unavailable, reminders still create audit events.

## 6. Engagement Timeline
- Event catalog: mission_created, assignment_proposed, acceptance_recorded, proposal_expired, mission_updated, mission_canceled, document_expected, document_uploaded, document_validated.
- Views: per mission timeline (ordered by occurred_at, stable ids); per project timeline aggregates mission events without cross-organization leakage.
- Ordering and dedup: events carry correlation_id/trace_id; idempotent insertion rules ignore repeats with same correlation_id.
- Visibility: collaborators see their mission timelines; production and direction see project timelines.

## 7. Execution Documents
- Types (non-legal): signed_contract_pdf (attachment reference), attendance_sheet, mission_report, payslip_reference (metadata only, optional).
- Lifecycle: expected -> uploaded -> validated -> archived; validation is manual or policy-driven but never triggers payments or accounting exports.
- Links: document references include org_id, project_id, mission_id; assignment_id optional for collaborator-specific artifacts.
- Storage rules: store metadata and file reference with versioning; no automatic deletions; redactions recorded as new versions.
- Constraints: no payroll computation, accounting-grade exports, or bank sync; documents remain declarative evidence only.

## 8. Engagement Audit Journal
- Append-only journal scoped by organization and project.
- Minimum fields: org_id, project_id, mission_id, assignment_id (optional), event_type, actor_id or system, occurred_at, correlation_id/trace_id, payload summary.
- Security: production and direction can view mission/project journals; collaborators can view mission events relevant to their assignments.
- Retention: follow existing audit retention policy (docs/specs/09_audit_and_traceability.md) with immutable history; redactions recorded as new events.

## 9. Permissions and RBAC
- Intermittent/collaborator: view proposals, accept/decline own assignments, view own mission timeline.
- Production: propose missions and assignments, resend reminders, manage execution documents, view project timelines and audit entries for their projects.
- Finance/HR (if present): view expected documents and validation status; no payroll or accounting computations.
- Direction/Admin: read all mission and project timelines, escalations, and audit journals within the organization.
- RBAC evaluation follows docs/specs/08_rbac_model.md with organization-scoped checks; no cross-organization access.

## 10. Non-goals
- Electronic signature or legal contract enforcement.
- Payroll calculation or automatic payment triggers.
- Accounting exports or bank synchronization.
- Automated irreversible side effects; all flows remain declarative and traceable.

## 11. Future extensions
- Webhooks for engagement and document events.
- Push notifications aligned to messaging contracts.
- Signature provider integration without altering acceptance semantics.
- External payroll or accounting exports gated by future roadmap steps.

## Roadmap linkage
- Roadmap: docs/roadmap/phase1/step-23-engagement-acceptance-and-notifications.md (documentation-only amendment under Phase 1 lock charter).
