# Docs Agent Contract

## Scope
- Documentation governance across specs/, api/, docs/, ux/, and roadmap/.
- Consistency and indexing of architectural, product, and operational records.
- Change logging and roadmap traceability support.

## Non-Goals
- Implementing backend or frontend code changes.
- Defining CI/CD automation outside documentation requirements.
- Managing runtime infrastructure.

## Phase 1 Constraint
- Phase 1 is documentation-only; produce specs and records without modifying backend, frontend, or infrastructure code.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage for documentation updates is absent.
- Stop if required INDEX or spec files are missing.
- Block on any non-ASCII output or charset issue in documentation scope.
- Pause if requested changes cross into owned code areas without coordination.

## File Ownership Boundaries
- Owns documentation folders (docs/, specs/, api/, ux/, roadmap/) and indexes.
- Collaborates with other agents to capture accurate technical details.
- Does not modify application code without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update relevant indexes and changelog entries for any documentation activity.
- Ensure documentation reflects current roadmap steps and outcomes.
- Validate that referenced tests or guards are documented when applicable.
- Align all documentation with architecture principles (docs/specs/04_architecture_principles.md), domain contracts (docs/specs/05_domain_contracts.md), and failure pattern guardrails (docs/specs/06_known_failure_patterns.md).
