# Phase 1 Extension - Contract and Assignment Link (Spec 30)

## Purpose
- Preserve coherence between planning assignments and contracts without altering Phase 1 locked artifacts.
- Ensure contracts consistently reflect the assignments they cover across dates, roles, and missions.
- Provide documentation-only guidance with no business logic, persistence change, or legal enforceability.
- Aligns with ADR docs/specs/adr_assignment_first_contract_derived.md so assignment remains the atomic planning and costing unit.

## Contract to Assignment Rule
- A contract may reference one or multiple assignments within the same project and organization.
- Assignment linkage is optional but limited to at most one contract per assignment to avoid double counting; uncontracted assignments remain valid for planning.
- Assignments remain project-scoped; cross-project references are forbidden, and cross-organization links are disallowed.
- The contract inherits and locks assignment fields for dates, role, and mission to prevent drift after signature; contracts never override these fields.

## Assignment Fields Referenced by Contracts
- **Dates**: planned start/end or individual scheduled windows the assignment covers.
- **Role**: assignment role as declared in planning; immutable once the contract is signed.
- **Mission**: mission identifier within the project; contracts cannot span missions across projects.

## Invariants and Derived Values
- Assignment is the atomic unit for planning, costing, and audit; any contract totals are computed per assignment and optionally aggregated for display.
- Contracts must not redefine assignment-derived fields (dates, role, rate model, mission_id, project_id, org_id); any mismatch requires an assignment update or new assignment.
- Totals or schedules shown on a contract are derived from linked assignments; the assignment remains the source of truth for costing and audit.
- Amendments keep the assignment links intact; scope changes require assignment replacement before a new contract version is issued.

## Lifecycle
- **draft_preview (non-legal)** -> **signed/active (post-acceptance)** -> **archived**
- Draft previews may exist before acceptance but cannot emit legal artifacts or payments; signed/active contracts are only issued after explicit assignment acceptance.
- State changes are documented only; no automated signature or payment flow is introduced.

## Completeness and Alerts
- Missions with assignments SHOULD have at least one associated contract covering those assignments.
- If a mission has assignments but no linked contract, a warning is raised; the warning is non-blocking.
- Warnings are displayed in the planning dashboard and project views to surface contract gaps.

## Visibility and RBAC
- Contract-assignment links respect organization as the security boundary and project as the functional boundary.
- Read-only visibility is available to stakeholders with planning access; finance/legal roles can view linkage details.
- No automatic payments, banking sync, or legal exports are triggered by linkage data.

## Non-Goals
- Payroll, invoicing, or accounting-grade validation.
- Cross-organization or cross-project contract linkage.
- Storage of computed totals or payment schedules derived from contracts.
