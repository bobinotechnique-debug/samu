# Phase 2 Spec 33 - Assignment Engagement States

## 1. Purpose and Scope
- Freeze the canonical assignment engagement state machine for Phase 2 so implementation teams can align async workflows, notifications, and contracts without diverging semantics.
- Applies to all assignments under one organization and project; no cross-organization or cross-project state propagation.
- Builds on Phase 1 contracts (ownership, RBAC, audit, idempotency) without introducing runtime code changes.

## 2. State Definitions
- **PROPOSED**: assignment offer created and communicated; awaiting collaborator decision.
- **ACCEPTED**: collaborator explicitly accepts; legal acknowledgement but not yet ready for execution.
- **CONFIRMED**: manager/production validates prerequisites (documents, budget, schedule) and locks execution intent.
- **EXECUTED**: work delivered; execution evidence available or time window elapsed with validation hooks.
- **CANCELED**: assignment withdrawn before or after acceptance; includes collaborator decline as a reasoned cancellation.

## 3. Invariants
- Project-scoped only; every assignment carries org_id and project_id with authorization enforced per docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md.
- No planning exists outside projects; mission_id and project_id required on every assignment mutation.
- Assignment is the atomic unit of cost; cost estimates and contracts bind to assignment_id, not aggregated missions.
- Every transition writes an audit event with correlation_id/trace_id and actor metadata per docs/specs/09_audit_and_traceability.md.
- State transitions must be idempotent; replays with the same correlation_id do not create duplicate timeline entries.

## 4. Allowed Transitions
| From       | To         | Actor (RBAC)                | Preconditions                                                                 | Audit Event |
|------------|------------|-----------------------------|-------------------------------------------------------------------------------|-------------|
| PROPOSED   | ACCEPTED   | collaborator on assignment; project_manager/production may record acceptance on behalf with justification | Valid org/project membership; assignment not expired; notification delivered or retried; acceptance intent captured (actor_id, comment optional). | assignment.accepted |
| PROPOSED   | CANCELED   | collaborator (decline) or production/manager | Decline reason provided; no confirmed contract issued; cancellation reason stored. | assignment.canceled |
| ACCEPTED   | CONFIRMED  | project_manager or production | Budget owner sign-off recorded; required documents checklist satisfied or waived; no conflicting schedule blocks. | assignment.confirmed |
| ACCEPTED   | CANCELED   | project_manager or production; collaborator (withdraw) | Acceptance exists; cancellation reason (withdrawn_by_collaborator, replaced, budget_removed) stored; downstream notifications queued. | assignment.canceled |
| CONFIRMED  | EXECUTED   | system (auto) or production | Execution window reached with attendance or time entry; or production validates completion; contract (if any) locked. | assignment.executed |
| CONFIRMED  | CANCELED   | project_manager or production (exception) | Exception reason captured; no invoice issued; contract, if generated, flagged for amendment/void. | assignment.canceled |
| EXECUTED   | CANCELED   | project_manager (rare) | Post-execution void with legal review; requires finance/legal approval flag; invoice/payment not emitted. | assignment.canceled |

## 5. Edge Cases and Rules
- **Collaborator decline**: represented as CANCELED with reason=declined_by_collaborator; assignment can be re-proposed by moving to PROPOSED with a new audit event assignment.reproposed.
- **Manager override**: project_manager/production may move ACCEPTED -> CONFIRMED even if optional documents pending, but must set override_reason and expected_resolution_at; audit event assignment.confirmed_override recorded.
- **Execution auto-transition**: system may move CONFIRMED -> EXECUTED when execution_end_at has passed and attendance/time entry exists; idempotent check prevents duplicate EXECUTED entries.
- **Re-proposal after cancellation**: only allowed from CANCELED -> PROPOSED by production with explicit link to prior assignment_id and correlation_id for traceability.
- **Expiration**: if proposal_expires_at passes without acceptance, PROPOSED transitions to CANCELED (reason=expired) before re-proposal; reminders and notifications follow docs/specs/34_notifications_and_acceptance.md.

## 6. Backward Compatibility
- Existing assignment statuses (planned, proposed, accepted, confirmed, executed, canceled) map to new machine as follows:
  - planned -> PROPOSED (draft proposals continue to publish as PROPOSED when sent).
  - proposed -> PROPOSED.
  - accepted -> ACCEPTED.
  - confirmed -> CONFIRMED.
  - executed -> EXECUTED.
  - canceled -> CANCELED (includes declines and expirations).
- Any prior DECLINED status is migrated to CANCELED with reason=declined_by_collaborator; reporting uses reason codes for clarity.
- Mission-level states remain unaffected; mission timelines aggregate assignment events without altering mission state machine.

## 7. Audit Rules
- Each transition emits assignment.<state_change> event with fields: org_id, project_id, mission_id, assignment_id, actor_id or system, from_state, to_state, occurred_at, correlation_id/trace_id, reason/metadata.
- Audit events are append-only and immutable; corrections require amendment events referencing original correlation_id.
- Audit visibility: collaborator sees own assignment events; production/management sees project scope; finance/legal sees cancellation and override reasons only if permitted by RBAC.

## 8. Preconditions and Validation
- org_id and project_id must match authenticated context; cross-organization access forbidden.
- Assignment payload includes role, rate, dates; CONFIRMED locks these fields for downstream contract generation.
- Conflicting transitions (e.g., ACCEPTED -> PROPOSED without cancellation) return 409 conflict and emit audit event assignment.transition_rejected with rationale.

## 9. Out-of-Scope / Forbidden Patterns
- No automatic contract generation on PROPOSED; contracts only after ACCEPTED events via async pipeline (see docs/specs/35_contract_generation_pipeline.md).
- Frontend cannot bypass RBAC or write state transitions directly; transitions go through backend/domain services with audit hooks.
- No silent auto-acceptance on timeout; explicit acceptance/decline required.

## 10. Roadmap Linkage
- Phase 2 Step 21 (docs/roadmap/phase2/step-21-engagement-states.md) registers this spec under the Phase 2 documentation-first scope.
