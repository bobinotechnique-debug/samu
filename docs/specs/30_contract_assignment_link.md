# Phase 1 Extension - Contract and Assignment Link (Spec 30)

## Purpose
- Preserve coherence between planning assignments and contracts without altering Phase 1 locked artifacts.
- Ensure contracts consistently reflect the assignments they cover across dates, roles, and missions.
- Provide documentation-only guidance with no business logic, persistence change, or legal enforceability.

## Contract to Assignment Rule
- A contract may reference one or multiple assignments within the same project and organization.
- Assignments remain project-scoped; cross-project references are forbidden.
- The contract inherits and locks assignment fields for dates, role, and mission to prevent drift after signature.

## Assignment Fields Referenced by Contracts
- **Dates**: planned start/end or individual scheduled windows the assignment covers.
- **Role**: assignment role as declared in planning; immutable once the contract is signed.
- **Mission**: mission identifier within the project; contracts cannot span missions across projects.

## Lifecycle
- **draft** -> **signed** -> **archived**
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
