# Phase 2 Spec 35 - Contract Generation Pipeline

## 1. Purpose
- Define the event-driven, auditable, and idempotent pipeline that turns assignment acceptance into generated contracts and later payslips without automatic payment.
- Scope: documentation-first; no runtime code changes; aligned with Phase 1 multi-tenancy, RBAC, and audit rules.

## 2. Trigger and Flow
- AssignmentAccepted event (from ACCEPTED state) enqueues job GenerateContract.
- Job reads assignment snapshot (org_id, project_id, mission_id, collaborator_id, role, rate, dates) and contract_template_version.
- Contract locks role, rate, start/end dates; changes require new assignment or amendment.

## 3. Idempotency and Safety
- Idempotency key: contract_key = org_id + assignment_id + contract_template_version.
- Job must be idempotent: repeated execution with same contract_key returns existing contract reference without side effects.
- Retry/backoff: exponential backoff with jitter; bounded attempts with dead-letter on exhaustion; retries reuse same idempotency key.
- Observability: trace_id propagates from event to job to storage; each attempt writes audit event contract.generation_attempt with attempt count, success/failure, and error (if any).

## 4. Change Management
- If assignment changes after a contract exists:
  - Create new assignment (preferred) with new assignment_id; previous contract remains linked to original assignment.
  - Or issue amendment (avenant) referencing prior contract_id with audit event contract.amendment_requested and new contract_key that bumps contract_template_version or amendment_sequence.
- Assignment transition ACCEPTED -> CANCELED after contract must emit contract.void_requested with rationale; payments remain blocked until resolved.

## 5. Missing Contract Alert Rule
- Mission with at least one assignment and any assignment state >= ACCEPTED but no contract on that assignment triggers WARNING (non-blocking) with event contract.expected_missing.
- Notifications use CONTRACT_EXPECTED_WARNING; does not block execution but must be visible on mission/project timeline.

## 6. Read Model: Timeline Composition
- Derived read view (not stored) composed as: Assignment -> Acceptance -> Contract -> Execution -> Invoice -> Payment.
- Read model is recomputed from events; no mutable state stored; consumers must tolerate partial data and idempotent merges.

## 7. Audit Rules
- Minimum audit fields: org_id, project_id, mission_id, assignment_id, contract_id (when created), actor_id or system, attempt, outcome, correlation_id/trace_id, payload summary, occurred_at.
- Audit events: contract.generation_attempt, contract.generated, contract.generation_failed, contract.amendment_requested, contract.void_requested, contract.expected_missing.

## 8. Forbidden Patterns
- No contract generation before explicit acceptance; PROPOSED notifications cannot trigger contract jobs.
- No frontend-triggered contract generation; only backend jobs consume events.
- No silent overwrites of contracts on assignment edits; require new assignment or amendment path with audit.

## 9. Dependency Alignment
- Uses async job model from docs/specs/23_async_jobs.md and consistency/idempotency rules from docs/specs/25_consistency_and_idempotency.md.
- Security aligns with docs/specs/24_security_model.md; all storage and events scoped by org_id and project_id with RBAC on reads.

## 10. Roadmap Linkage
- Phase 2 Step 21 (docs/roadmap/phase2/step-21-engagement-states.md) anchors this pipeline specification.
