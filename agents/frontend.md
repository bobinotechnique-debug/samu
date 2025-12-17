# Frontend Agent Contract

## Scope
- UI composition, views, and UX flows implemented with React + Vite + TailwindCSS.
- Frontend state management and interaction patterns.
- Frontend-focused testing and accessibility alignment.

## Non-Goals
- Backend domain or API logic.
- Infrastructure or CI/CD pipeline ownership beyond frontend build needs.
- Authoring backend or devops documentation without coordination.

## Phase 1 Constraint
- Phase 1 is documentation-only; frontend code or build changes require a roadmap step beyond Phase 1 scope.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage is missing for requested frontend work.
- Stop if required INDEX or spec files are absent.
- Block on any non-ASCII output or charset issue in frontend scope.
- Pause if changes cross backend or devops ownership boundaries without coordination.

## File Ownership Boundaries
- Owns frontend/ and frontend-related assets captured in ux/ references.
- Collaborates with Docs Agent on UX documentation in ux/ and docs/ux.
- Does not modify backend/ or ops/ without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update UX or frontend documentation when behaviors change.
- Provide frontend automated tests aligned with changes before completion.
- Ensure change logs and roadmap mappings are updated for frontend work.
