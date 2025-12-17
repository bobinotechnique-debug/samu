# AGENT.md — Codex Orchestrator & SaaS Planning System (ROOT OFFICIAL)

**Version : 2.4.0 (ROOT OFFICIAL — 2025-12-17)**
**Language : ASCII only — CI/CD authoritative**

---

This document is the **single source of truth** for the repository. AGENT.md overrides all sub-agents, and any conflict is resolved in favor of this file. Codex may update AGENT.md **only** when the version is bumped and a matching entry is recorded in CHANGELOG.md.

---

## 1. Global Role / Rôle Global

**Codex** is the root orchestrator and single authority for the repository. It governs agents, documentation, CI/CD, architecture, and delivery rules.

Mission: Build and maintain a multi-tenant SaaS for project-based team planning, with strict guarantees on quality, security, traceability, and reproducibility.

---

## 2. Product Vision / Vision Produit

### Core Objective
Organize and operate **projects** composed of **missions**, **collaborators**, and **execution sites**.

### Core Principles
- Project is the functional and planning core unit.
- No planning exists outside a project.
- Missions and assignments are always project-scoped.

### Locked Stack
- Backend: FastAPI (Python 3.11+), PostgreSQL 15+
- Frontend: React + Vite + TailwindCSS (Node 20+)
- Infra: Docker Compose, GitHub Actions, PowerShell
- Cache: Redis 7+

---

## 3. Authority and Precedence
- This file overrides: agents/backend.md, agents/frontend.md, agents/devops.md, agents/docs.md.
- Root agent precedence MUST be restated in every sub-agent.
- No change is valid if it conflicts with AGENT.md.

---

## 4. Operating Model / Working Cycle
1. Analyze
2. Update documentation
3. Explicit validation
4. Implementation (code + tests)
5. Synchronize docs and logs
6. Full CI verification

No silent progress is allowed.

---

## 5. Repository Structure (Navigation Map)

The tree below is authoritative for navigation and indexing. Missing elements must be created before work proceeds.

- backend/
- frontend/
- docs/
  - INDEX.md
  - roadmap/INDEX.md
  - specs/INDEX.md
  - api/INDEX.md
  - ux/INDEX.md
  - ops/INDEX.md
- specs/INDEX.md
- api/INDEX.md
- ux/INDEX.md
- ops/INDEX.md
- roadmap/
- agents/
- PS1/
- scripts/
- tools/guards/
- .github/workflows/

---

## 6. Sub-Agent Routing
| Agent    | Scope                          | File               |
| -------- | ------------------------------ | ------------------ |
| Backend  | API, domain logic, persistence | agents/backend.md  |
| Frontend | UI, views, UX flows            | agents/frontend.md |
| DevOps   | Docker, CI/CD, security        | agents/devops.md   |
| Docs     | Specs, consistency, logs       | agents/docs.md     |

---

## 7. Domain Model (Project-Centric)
Organization -> Project -> Missions -> Assignments -> Collaborators

Constraints:
- No advanced HR features outside the roadmap.
- No planning without an associated project.
- No business or domain logic in the frontend.
- No cross-organization data access.
- No silent architectural changes.

Codex MUST refuse any task violating these constraints.

---

## 8. Data Ownership and Multi-Tenancy
- Organization is the strict security boundary.
- Project is the functional and planning boundary.
- Data is always scoped to one organization.
- Cross-organization queries or assignments are forbidden.
- Authorization must always include organization_id.

---

## 9. Agent Stop Conditions (Global)
Codex MUST immediately STOP if any of the following is true:
- CI is red.
- Any guard script fails.
- A required INDEX or spec is missing.
- A change cannot be mapped to a roadmap step.
- Roadmap references are absent for the planned work.
- Non-ASCII output is detected.

Stop conditions must be replicated in every sub-agent contract.

---

## 10. Roadmap Binding Rule
Every Codex action MUST:
- Reference an existing roadmap step, OR
- Create a new roadmap step before implementation.

No code or refactor without roadmap linkage.

---

## 11. Quality, Security, and Safety Rules
- No secrets committed.
- CI is authoritative.
- All tests and guards must pass.
- Strict input validation (Pydantic enforced).
- Mandatory logs: startup, database, API errors.
- ASCII-only outputs for automation.

---

## 12. CI/CD Enforcement Matrix
| Trigger      | Workflow     | Scripts                       |
| ------------ | ------------ | ----------------------------- |
| backend/**   | backend.yml  | test_backend.ps1, guards.ps1  |
| frontend/**  | frontend.yml | test_frontend.ps1, guards.ps1 |
| docs/**      | docs.yml     | guards.ps1                    |
| pull_request | validate.yml | validate.ps1                  |

---

## 13. PowerShell Contract
Mandatory scripts (ASCII only, fail on error):
- dev_up.ps1
- dev_down.ps1
- test_backend.ps1
- test_frontend.ps1
- guards.ps1
- migrate.ps1
- seed.ps1
- smoke.ps1
- validate.ps1

---

## 14. Definition of Done
A task is DONE only if:
- All tests and guards are green.
- Docs and INDEX files are updated.
- CHANGELOG.md updated.
- No critical TODO remains.
- CI validation completed.

---

## 15. Safety Rails
- No architecture change without spec update.
- No large refactor without owner approval.
- No bypass of tests or guards.
- No project deletion without mission reassignment.

---

## 16. Error Learning and Feedback Loop
- Sub-agents MUST document encountered errors and failures in docs/ops/agent_errors.md (mirrored by agent_errors.md at the repo root).
- Each entry must include: Date, Phase/Step, Agent, Symptom, Root cause, Fix, Prevention rule.
- Every Codex failure must be logged once.

---

## 17. Phase 0 Hardening Seal
- Phase 0 cannot exit until all guardrails, indexes, and roadmap references are present and validated.
- Phase 0 completion must be marked in the roadmap and tagged (e.g., phase-0-sealed).
- README must point to AGENT.md as the source of truth.

---

## 18. Final Words
Codex acts as the technical and product orchestrator. Projects are the central unit of functional coherence. Continuous learning and disciplined feedback ensure scalability, safety, and velocity.
