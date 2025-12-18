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
1. Copy `.env.example` to `.env` and update values.
2. Install dependencies: `python -m pip install -e ./backend[dev]`.
3. Run tests: `pytest backend/tests`.
4. Start the app: `uvicorn app.main:app --reload` (requires env vars).

Database connectivity defaults to PostgreSQL; tests set `SAMU_TESTING=true` with a SQLite URL override to keep pipelines green.
