# samu

Repository for the Codex Orchestrator SaaS planning system. Follow **AGENT.md** for authoritative rules, scope, and stop conditions.

## Current Phase
- Phase 0 (Hardening) - sealed. See roadmap/phase0/step-00-bootstrap.md and docs/roadmap/INDEX.md.

## Quick Navigation
- AGENT.md - root authority and navigation map.
- agents/ - sub-agent contracts (backend, frontend, devops, docs).
- docs/ - documentation indexes including roadmap, specs, api, ux, and ops.
- tools/guards/ - PowerShell guards enforcing ASCII, documentation presence, roadmap status, and agent precedence.

## Running Guards
Use `pwsh PS1/guards.ps1` from the repository root to execute all guard scripts. Guards must pass before progressing to further phases.
