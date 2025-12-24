# Phase 2 Step 10 - Implementation Bootstrap

## Goal
Create runnable scaffolding for backend, frontend, and ops surfaces without adding business logic. Align with Phase 1 contracts and Phase 2 architecture outputs.

## Scope
- Backend FastAPI skeleton with versioned routing, error model wiring, operational health endpoints, and dependency plumbing.
- Persistence adapters and Alembic initialized for connectivity checks only.
- Auth context extraction and RBAC hook stubs.
- Jobs and Redis placeholders with worker entrypoint stub.
- Frontend React shell, routing skeleton, API client wrapper, and env config.
- Docker Compose baseline for api, worker, db, cache, and frontend.
- Tests for app startup, health probes, and error envelope.

## Deliverables
- docs/specs/36_bootstrap_backend_wiring_contract.md - backend bootstrap wiring contract for health endpoints, middleware, settings precedence, and adapter stubs.
- docs/ux/36_frontend_shell_contract.md - frontend shell wiring contract for routing, API client wrapper, and environment handling.
- docs/specs/37_smoke_test_contract.md - smoke test contract covering backend, frontend, and ops bootstrap surfaces.
- Index updates in docs/specs/INDEX.md and docs/ux/INDEX.md reflecting the new contracts.

## Status
In progress.

## Notes
- No domain workflows implemented.
- Defaults target local/CI usage with SQLite fallback in tests to keep pipelines green.
- Implementation readiness audit recorded at docs/audits/implementation_readiness.md; resolve documented blockers before coding.

## Iteration 2 (V0.001) runtime bootstrap
- Non-versioned `GET /health/live` and `GET /health/ready` are routed outside `/api/v1`, with `/api/v1/health` kept only as a readiness compatibility alias.
- Request and correlation IDs are returned on responses via middleware to support probe traceability.
- Settings loader honors precedence (env vars > .env.local > .env > defaults) with local-safe defaults and a committed `.env.example` for contributors.

## Prerequisites and acceptance alignment
- Canonical operational endpoints are non-versioned GET /health/live (liveness only) and GET /health/ready (readiness with at least database checks; add cache/queue only when required to serve traffic).
- Deployment and CI probes MUST target /health/live and /health/ready; /api/v1/health, if kept, is only a compatibility alias that proxies readiness and is discouraged for probes.
- Routing bootstrap must keep /health/* outside /api/v1 while preserving versioned routers for business APIs.
- Implementation Readiness Audit blocker on conflicting health contracts is removed once this alignment is merged.
