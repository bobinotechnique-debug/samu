# samu

Repository for the Codex Orchestrator SaaS planning system. Follow **AGENT.md** for authoritative rules, scope, and stop conditions.

## Table of Contents
- [Project Overview](#project-overview)
- [Current Phase](#current-phase)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Guards and Compliance](#guards-and-compliance)
- [CI/CD](#cicd)
- [Navigation](#navigation)

## Project Overview
The platform provides project-centric planning capabilities with FastAPI and React foundations. All contributions must respect the root authority outlined in AGENT.md.

## Current Phase
- Phase 0 (Hardening) - sealed. See roadmap/phase0/step-00-bootstrap.md and docs/roadmap/INDEX.md.

## Prerequisites
- Python 3.11+
- Node.js 20+ and npm
- Git
- PowerShell (for existing scripts) or Python 3.11 (for cross-platform guards)

## Getting Started
1. Clone the repository and ensure you are on the correct branch.
2. Install backend dependencies:
   - `cd backend`
   - `python -m venv .venv && source .venv/bin/activate` (or `.venv\\Scripts\\activate` on Windows)
   - `pip install -e .[dev]`
3. Install frontend dependencies:
   - `cd frontend`
   - `npm ci`
4. Start local services (from repository root):
   - Backend: `cd backend && uvicorn app.main:app --reload`
   - Frontend: `cd frontend && npm run dev`

## Running Tests
- Backend: `cd backend && pytest`
- Frontend: `cd frontend && npm run test`
- Cross-cutting sample tests: `pytest tests/backend` and `cd frontend && npm run test -- --dir ../tests/frontend`

## Guards and Compliance
- PowerShell: `pwsh PS1/guards.ps1`
- Cross-platform: `python tools/guards/run_guards.py`
Guards must pass before progressing to further phases.

## CI/CD
- `.github/workflows/ci.yml` runs guards, linting, and backend/frontend tests across Linux, macOS, and Windows.
- `.github/workflows/release.yml` prepares semantic releases and updates the changelog after validation.

## Navigation
- AGENT.md - root authority and navigation map.
- agents/ - sub-agent contracts (backend, frontend, devops, docs).
- docs/ - documentation indexes including roadmap, specs, api, ux, and ops.
- tools/guards/ - Guard scripts for ASCII validation, documentation coverage, roadmap sealing, and agent precedence.
