# Backend Agent Contract

## Scope
- API design and implementation for the SaaS backend using FastAPI.
- Domain logic, data models, and persistence interactions.
- Backend-specific testing strategy and automation coordination.

## Non-Goals
- Frontend UI or UX implementation.
- Infrastructure provisioning outside backend application needs.
- Documentation governance beyond backend specifications.

## Phase 1 Constraint
- Phase 1 is documentation-only; pause backend code or infrastructure changes unless a roadmap step authorizes them.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage is missing for requested backend work.
- Stop if required INDEX or spec files are absent.
- Block on any non-ASCII output or charset issue in backend scope.
- Pause if changes cross frontend or devops ownership boundaries without coordination.

## File Ownership Boundaries
- Owns backend/ and backend-specific scripts under PS1/ related to backend testing or maintenance.
- Collaborates on shared specs in specs/ and api/ when backend input is required.
- Does not modify frontend/, ux/, or ops/ without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update backend-focused documentation and specs for any behavior or contract change.
- Provide backend automated tests aligned with changes before completion.
- Ensure change logs and roadmap mappings are updated for backend work.
- Validate designs and documentation against architecture principles (docs/specs/04_architecture_principles.md), domain contracts (docs/specs/05_domain_contracts.md), and failure patterns (docs/specs/06_known_failure_patterns.md) before approval.
