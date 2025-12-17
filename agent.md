# AGENT.md — Codex Orchestrator & SaaS Planning System

**Version : 2.3 (ROOT OFFICIAL — 2025-12-17)**  
**Language : Bilingual FR/EN — ASCII only, CI/CD authoritative**

---

This document is the **single source of truth** for the repository.  
Any deviation must be explicitly approved and logged.

Codex is authorized to **update this document progressively** as the system evolves,  
provided that all changes are:
* Explicitly versioned
* Logged in CHANGELOG.md
* Mapped to a roadmap step

---

## 1. Global Role / Role Global

**Codex** is the root orchestrator and single authority for the repository.  
It governs agents, documentation, CI/CD, architecture, and delivery rules.

Mission:  
Build and maintain a multi-tenant SaaS for project-based team planning,  
with strict guarantees on quality, security, traceability, and reproducibility.

---

## 2. Product Vision / Vision Produit

### Core Objective

Organize and operate **projects** composed of **missions**, **collaborators**, and **execution sites**.

### Core Principles

* Project is the functional and planning core unit.
* No planning exists outside a project.
* Missions and assignments are always project-scoped.

### Locked Stack

* Backend: FastAPI (Python 3.11+), PostgreSQL 15+
* Frontend: React + Vite + TailwindCSS (Node 20+)
* Infra: Docker Compose, GitHub Actions, PowerShell
* Cache: Redis 7+

---

## 3. Authority and Precedence

This file overrides:

* agents/backend.md
* agents/frontend.md
* agents/devops.md
* agents/docs.md

If a conflict exists, **AGENT.md always wins**.

---

## 4. Operating Model / Working Cycle

### Macro Phases

| Phase | Scope                                    |
| ----- | ---------------------------------------- |
| 0     | Agent system and orchestration           |
| 1     | Foundational documentation               |
| 2     | Technical bootstrap                      |
| 3     | CI, quality, and security                |
| 4     | MVP (Orgs, Projects, Missions, Planning) |
| 5     | Advanced Planning and Intelligence       |

### Standard Flow

1. Analyze
2. Update documentation
3. Explicit validation
4. Implementation (code + tests)
5. Synchronize docs and logs
6. Full CI verification

No silent progress is allowed.

---

## 5. Repository Structure (Authoritative)

backend/
frontend/
docs/
specs/
roadmap/
api/
ux/
ops/
agents/
PS1/
scripts/
tools/guards/
.github/workflows/

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

---

## 8. Non-Goals (Hard Constraints)

The following are explicitly out of scope unless stated in the roadmap:

* No advanced HR features outside the roadmap.
* No planning without an associated project.
* No business or domain logic in the frontend.
* No cross-organization data access.
* No silent architectural changes.

Codex MUST refuse any task violating these constraints.

---

## 9. Data Ownership and Multi-Tenancy

* Organization is the strict security boundary.
* Project is the functional and planning boundary.
* Data is always scoped to one organization.
* Cross-organization queries or assignments are forbidden.
* Authorization must always include organization_id.

---

## 10. Agent Stop Conditions (Hard Stops)

Codex MUST immediately STOP if:

* CI is red.
* Any guard script fails.
* A required spec or roadmap step is missing.
* A change cannot be mapped to a roadmap step.
* Tests are skipped or bypassed.

Codex must report the blocking reason before proceeding.

---

## 11. Roadmap Binding Rule

Every Codex action MUST:

* Reference an existing roadmap step, OR
* Create a new roadmap step before implementation.

No code or refactor without roadmap linkage.

---

## 12. Quality, Security, and Safety Rules

* No secrets committed.
* CI is authoritative.
* All tests and guards must pass.
* Strict input validation (Pydantic enforced).
* Mandatory logs: startup, database, API errors.

---

## 13. CI/CD Enforcement Matrix

| Trigger      | Workflow     | Scripts                       |
| ------------ | ------------ | ----------------------------- |
| backend/**   | backend.yml  | test_backend.ps1, guards.ps1  |
| frontend/**  | frontend.yml | test_frontend.ps1, guards.ps1 |
| docs/**      | docs.yml     | guards.ps1                    |
| pull_request | validate.yml | validate.ps1                  |

---

## 14. PowerShell Contract

Mandatory scripts (ASCII only, fail on error):

* dev_up.ps1
* dev_down.ps1
* test_backend.ps1
* test_frontend.ps1
* guards.ps1
* migrate.ps1
* seed.ps1
* smoke.ps1
* validate.ps1

---

## 15. Definition of Done

A task is DONE only if:

* All tests and guards are green
* Docs and INDEX files are updated
* CHANGELOG.md updated
* No critical TODO remains
* CI validation completed

---

## 16. Safety Rails

* No architecture change without spec update
* No large refactor without owner approval
* No bypass of tests or guards
* No project deletion without mission reassignment

---

## 17. Error Learning and Feedback Loop

Sub-agents MUST document encountered errors and failures in a dedicated log  
(e.g. docs/ops/agent_errors.md or equivalent), including:

* Context (step, agent, commit)
* Root cause analysis
* Resolution applied
* Preventive rule or guard added

This feedback loop is mandatory and is used to prevent repeated failures  
across agents and future phases.

---

## 18. Final Words

Codex acts as the technical and product orchestrator.  
Projects are the central unit of functional coherence.  
Continuous learning and disciplined feedback ensure scalability, safety, and velocity.

