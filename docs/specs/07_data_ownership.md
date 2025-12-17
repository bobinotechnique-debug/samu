# Data Ownership Rules

## Purpose
Define authoritative ownership and boundary rules for data across the platform to guarantee isolation, traceability, and enforcement in later phases.

## Scope
- Applies to all documentation and future implementations touching organization, project, mission, assignment, collaborator, and audit data.
- Governs data modeling, API design, and storage constraints without introducing code changes in Phase 1.

## Assumptions
- Organization is the hard security boundary; project is the hard functional boundary as mandated by AGENT.md.
- Phase 1 remains documentation-only while setting enforceable invariants for subsequent phases.

## Exclusions
- Database schema migrations, ORM models, or API implementations.
- UI behaviors or client-side storage rules.

## Ownership Boundaries
- Organization MUST be treated as the non-negotiable security boundary; no data may cross organizations without explicit export protocols defined in future roadmap steps.
- Project MUST be treated as the functional and planning boundary; missions and planning artifacts MUST NOT exist outside a project.
- Organization ownership MUST cascade to all subordinate data; project ownership MUST cascade to missions and assignments within the same organization.

## Ownership Matrix
- Organization owns: organization profile, org-level policy sets, role bindings, and all subordinate projects.
- Project owns: project profile, missions, mission milestones, planning artifacts, and project-level role bindings.
- Mission owns: mission objectives, status, assignments, and mission-scoped audit context.
- Assignment owns: collaborator linkage, schedule block references, and status within the parent mission.
- Collaborator belongs to exactly one organization; participation in projects and missions MUST be validated against the collaborator organization_id.
- Audit records inherit ownership from the entity they describe and MUST include organization_id and project_id when applicable.

## Required Identifiers
- Every record MUST include org_id; it MUST be validated against authenticated context before processing.
- Records under a project MUST include project_id in addition to org_id.
- Mission and assignment records MUST include mission_id, project_id, and org_id to enforce hierarchical integrity.
- Role bindings and permissions MUST carry org_id and, when project-scoped, project_id to prevent leakage.
- Audit records MUST include org_id and project_id (when applicable) alongside entity identifiers to enable traceability.

## Forbidden Patterns
- Cross-organization joins, aggregations, or shared caches MUST NOT occur; any multi-org operation MUST route through explicit export/import processes defined in future steps.
- Global user or collaborator lists without an org_id filter MUST NOT be produced or consumed.
- Missions, assignments, or planning artifacts MUST NOT be created without a project_id and org_id.
- Role or permission checks MUST NOT rely on project_id alone; org_id validation is mandatory.
- Frontend or client-side data merging across organizations MUST NOT be relied upon for any workflow.

## Verification Rules
- Any data flow lacking org_id validation MUST be rejected during design reviews.
- Any artifact that references mission_id or assignment_id without matching project_id and org_id MUST be treated as invalid.
- Any dataset or API that attempts to aggregate across organizations without explicit roadmap authorization MUST be blocked.

## Related Specifications
- API scoping, pagination, and idempotency expectations that enforce these ownership rules are defined in docs/specs/10_api_conventions.md.
- Identifier and timestamp constraints are defined in docs/specs/13_identifiers_and_time.md to avoid leaking ownership context through IDs or time handling.
- Visual representation of ownership cues in UX views is governed by docs/specs/14_visual_language.md and the view specifications in docs/ux/INDEX.md.
