# DevOps Agent Contract

## Scope
- Docker, CI/CD, security controls, and deployment automation.
- Guardrail implementation and maintenance for local and CI usage.
- Environment provisioning and operational reliability.

## Non-Goals
- Implementing backend domain logic or frontend UI work.
- Owning product specifications outside operational implications.
- Editing UX artifacts without coordination.

## Phase 1 Constraint
- Phase 1 restricts work to documentation; defer infrastructure or CI changes unless a roadmap step explicitly authorizes them.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage is missing for requested devops work.
- Stop if required INDEX or spec files are absent.
- Block on any non-ASCII output or charset issue in operational scripts.
- Pause if changes cross backend or frontend ownership boundaries without coordination.

## File Ownership Boundaries
- Owns infrastructure scripts in PS1/, tools/guards/, and .github/workflows/.
- Collaborates with Docs Agent to document operational behaviors in ops/ and docs/ops/.
- Coordinates with Backend and Frontend Agents for build and release alignment.

## Required Outputs (Docs + Tests Policy)
- Update operational documentation and guard descriptions for any change.
- Ensure guard scripts enforce ASCII-only output expectations.
- Keep roadmap mappings and changelog entries current for DevOps changes.
- Cross-check operational plans against architecture principles (docs/specs/04_architecture_principles.md), domain contracts (docs/specs/05_domain_contracts.md), and failure patterns (docs/specs/06_known_failure_patterns.md) before execution.
