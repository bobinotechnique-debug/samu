# ADR - Assignment-First Contract-Derived Semantics

## Context
- CT-01 and CT-02 exposed conflicting statements about whether contracts are atomic cost units and whether pre-acceptance drafts are allowed.
- Planning, costing, and audit flows are already anchored on assignments; contracts must not redefine those anchors.
- The contract generation pipeline must support safe previews without producing legal artifacts before acceptance.

## Decision
- Assignment remains the atomic unit for planning, costing, and audit. Contract totals are derived per assignment and optionally aggregated in a contract view.
- A contract may reference one or more assignments **within the same organization and project**; cross-org or cross-project links are forbidden.
- An assignment may be linked to at most one contract at a time to avoid double-counting and simplify audit trails.
- Contracts never override assignment-derived fields (dates, role, rate, mission/project scope); discrepancies require assignment updates or new assignments.
- Pre-acceptance contract previews are allowed for review only, produce no legal artifact, and must not trigger irreversible side effects.
- Issued/active contracts (legal artifacts) are generated only after explicit assignment acceptance.

## Definitions
- **Assignment atom**: the smallest unit for planning, costing, and audit events; immutable identifiers are assignment_id with org_id and project_id context.
- **Contract (derived)**: legal or pre-legal document that references one or more assignments and aggregates their derived values without redefining them.

## Cardinality Rules
- Contract -> Assignment: 1..N assignments permitted **only** inside the same project and organization.
- Assignment -> Contract: 0..1 contract linkage; uncontracted assignments remain valid for planning but are flagged for completeness.
- Cross-project or cross-organization linkage is forbidden.

## Invariants
- Contract cannot override assignment fields for dates, role, rate model, mission_id, project_id, or org_id.
- Any totals or schedules shown on a contract are derived from linked assignments; stored values remain projections, not new sources of truth.
- Amendments create new versions that keep assignment links intact or require replacement assignments when scope changes.

## Acceptance Gating and Drafts
- Draft/preview contracts before acceptance are informational only, carry explicit “non-legal preview” status, and emit no legal artifacts, invoices, or payments.
- Issued/active contracts are generated only after explicit assignment acceptance and honor idempotency rules keyed by assignment links.

## Auditability and Idempotency
- Audit events reference assignment_id as the atomic anchor; contract events aggregate over assignment references.
- Idempotent generation keys include org_id, project_id, assignment_id list, and template version to prevent duplicate artifacts.
- Void or amendment flows must preserve references to the original assignment_ids to maintain traceability.

## Non-Goals
- No payroll, taxation, or jurisdiction-specific legal compliance rules.
- No schema changes or automation of signature/payment flows.

## References
- Spec alignment: docs/specs/28_contrats.md, docs/specs/30_contract_assignment_link.md, docs/specs/33_assignment_engagement_states.md, docs/specs/35_contract_generation_pipeline.md.
