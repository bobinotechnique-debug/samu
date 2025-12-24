# Phase 2 Step 10 - Backend Bootstrap Wiring Contract

## Purpose
Document the required wiring for the backend skeleton so contributors can validate FastAPI startup, health endpoints, dependency injection, persistence connectivity, and logging hooks without implementing domain logic.

## Scope
- Applies to the API service and worker entrypoints delivered in the Step 10 bootstrap.
- Covers routing skeleton, middleware ordering, health probes, configuration loading, and migration hooks only.
- Excludes domain handlers, data models, and any business workflows.

## Deliverables
- Non-versioned `GET /health/live` and `GET /health/ready` endpoints present and returning JSON envelopes with timestamps.
- Middleware stack that injects request_id and correlation_id and returns them on responses.
- Settings loader precedence: environment variables > .env.local > .env > defaults.
- Alembic migrations wired to run on startup with logging that matches docs/ops/21_observability_and_logging.md field requirements.
- Dependency container stub in place for database session, cache client, and message queue handle (placeholder implementations allowed).

## Acceptance checks
- `uvicorn` server can start locally and in CI via Docker Compose using committed example environment files.
- Readiness probe fails when database connectivity is unavailable; liveness probe remains green unless the process is down.
- Logging output during startup and probe calls uses JSON with request_id and trace_id fields.
- No business routes are exposed; only health endpoints and root version metadata are present.

## Traceability
- Roadmap: docs/roadmap/phase2/step-10-implementation-bootstrap.md
- Related audits: docs/audits/bootstrap_implementation_plan.md, docs/audits/bootstrap_implementation_report.md
