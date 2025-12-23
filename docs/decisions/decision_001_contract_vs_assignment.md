# Decision 001 - Contract vs Assignment Authority

Status: SEALED
Date: 2025-12-24

## Source of truth
- Dates: assignments hold planned and actual dates; contract validity windows cannot override assignment timelines and are advisory for compliance only.
- Roles: assignments define operational roles; contracts may restate them but the assignment is authoritative for role naming and load.
- Rates: contracts are the authoritative container for negotiated rates once signed; assignments may include provisional rates for planning but legal and payable rates come from the linked contract.
- Scope: missions and assignments define scope of work; contracts reference that scope without mutating it.

## Cardinalities and rationale
- Contract to assignments: one contract may cover many assignments; a contract may also exist with zero assignments to support frameworks or future linkage. Rationale: legal agreements often bundle work items.
- Assignment to contract: one assignment may reference zero or one active contract at a time. Rationale: planning must remain independent, and a single governing contract avoids conflicting terms.

## Link rules (direction only)
- Assignments may carry an optional reference to a contract identifier; contracts may list related assignments for traceability but do not require them to exist.
- Links never drive planning creation; missing links surface as risk, not blockers.

## Lifecycle ordering
- Assignments can be created, updated, and completed without any contract existing.
- Contracts can be drafted and signed before assignments exist; linkage occurs only when scope and parties match an assignment.
- An assignment linked to an expired or superseded contract remains valid; risk is raised until a new contract is attached.

## Locking rules
- When a contract is signed, its parties, currency, rate tables, and validity window become immutable; amendments require a new contract record.
- When an assignment is linked to a signed contract, the contract reference and the rate source become immutable on that assignment. Schedule or role edits remain governed by planning rules and never inherit constraints from the contract.

## Forbidden states
- Assignments referencing multiple active contracts simultaneously.
- Contracts marked signed without defined parties, currency, rate tables, or validity windows.
- Contracts overwriting assignment timelines, roles, or mission scope.
- Validation flows that prevent assignment creation or updates because no contract exists.
- Cross-project linkage between a contract and assignments from different projects or organizations.

## Decision Status
SEALED - blocking for persistence and API design
