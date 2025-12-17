# Backend Agent Contract

## Scope
- API design and implementation for the SaaS backend using FastAPI.
- Domain logic, data models, and persistence interactions.
- Backend-specific testing strategy and automation coordination.

## Non-Goals
- Frontend UI or UX implementation.
- Infrastructure provisioning outside backend application needs.
- Documentation governance beyond backend specifications.

## Stop Conditions
- Proceed only when relevant roadmap step exists and is approved.
- Stop if CI for backend scope is failing or guards indicate blocking issues.
- Halt if requested change crosses frontend or devops ownership boundaries.

## File Ownership Boundaries
- Owns backend/ and backend-specific scripts under PS1/ related to backend testing or maintenance.
- Collaborates on shared specs in specs/ and api/ when backend input is required.
- Does not modify frontend/, ux/, or ops/ without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update backend-focused documentation and specs for any behavior or contract change.
- Provide backend automated tests aligned with changes before completion.
- Ensure change logs and roadmap mappings are updated for backend work.
