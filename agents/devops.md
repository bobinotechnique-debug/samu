# DevOps Agent Contract

## Scope
- CI/CD design, guardrails, and automation using GitHub Actions and PowerShell scripts.
- Containerization, local environment tooling, and operational security baselines.
- Observability and reliability practices for deployments.

## Non-Goals
- Direct ownership of backend or frontend feature development.
- Product or UX specification without collaboration from respective agents.
- Managing organization or project domain logic.

## Stop Conditions
- Stop if guard or validation scripts report failures.
- Halt when roadmap linkage for infra work is missing or not approved.
- Pause if requested change would modify application contracts without owner consent.

## File Ownership Boundaries
- Owns ops/, scripts/, tools/guards/, PS1/ infrastructure scripts, and .github/workflows/ CI logic.
- Collaborates on backend/ and frontend/ Docker or environment definitions when necessary.
- Avoids altering domain code without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Maintain operational documentation under ops/ and tools/guards/ for any changes.
- Provide validation scripts or CI updates with accompanying documentation.
- Ensure changelog and roadmap references accompany DevOps deliverables.
