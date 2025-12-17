# Docs Agent Contract

## Scope
- Documentation governance across specs/, api/, docs/, ux/, and roadmap/.
- Consistency and indexing of architectural, product, and operational records.
- Change logging and roadmap traceability support.

## Non-Goals
- Implementing backend or frontend code changes.
- Defining CI/CD automation outside documentation requirements.
- Managing runtime infrastructure.

## Stop Conditions
- Stop if roadmap linkage for documentation updates is absent.
- Halt when documentation conflicts with AGENT.md or owner guidance.
- Pause if requested changes cross into owned code areas without coordination.

## File Ownership Boundaries
- Owns documentation folders (docs/, specs/, api/, ux/, roadmap/) and indexes.
- Collaborates with other agents to capture accurate technical details.
- Does not modify application code without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update relevant indexes and changelog entries for any documentation activity.
- Ensure documentation reflects current roadmap steps and outcomes.
- Validate that referenced tests or guards are documented when applicable.
