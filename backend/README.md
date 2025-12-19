# Backend

FastAPI-based backend skeleton aligned with Phase 2 Step 10. It wires configuration, routing, health endpoints, and persistence scaffolding without business logic.

## Structure
- `app/main.py` - FastAPI application factory with middleware, exception handlers, and versioned router registration.
- `app/core` - shared configuration, logging, IDs, time, security hooks, database session helpers, messaging, and observability placeholders.
- `app/api` - dependencies, pagination helpers, request context middleware, and versioned routers under `api/v1`.
- `app/modules` - bounded context placeholders ready for domain/service/infra layering.
- `app/jobs` - queue abstractions and worker entrypoint stub.
- `alembic/` - migration tooling for connectivity checks.
- `tests/` - smoke tests for startup, health checks, and error envelope shape.

## Local usage
1. Copy `.env.example` to `.env` and update values. Optionally add a `.env.local` (ignored) for developer-specific overrides; explicit environment variables take precedence over both files.
2. Install dependencies: `python -m pip install -e ./backend[dev]`.
3. Run tests: `pytest backend/tests`.
4. Start the app: `uvicorn app.main:app --reload` (requires env vars).

Database connectivity defaults to an in-memory SQLite URL for local safety; set `SAMU_DATABASE_URL` (and `SAMU_REDIS_URL`) explicitly for CI, staging, and production. Tests set `SAMU_TESTING=true` with a SQLite URL override to keep pipelines green.

## Operational endpoints
- `GET /health/live` - process up only, no dependency checks.
- `GET /health/ready` - readiness probe (skips dependency checks when `SAMU_TESTING=true`).
- `GET /api/v1/health` - compatibility alias that proxies readiness semantics for legacy callers.

All responses include `X-Request-ID` and `X-Correlation-ID` headers; pass `X-Correlation-ID` on the request to propagate caller-provided correlation values.
