# Backend Testing Strategy (Phase 2 Step 13)

## 1. Purpose and Scope
- Establish the authoritative backend testing strategy and pytest harness without introducing business logic.
- Standardize how backend engineers validate correctness, isolation, and regression coverage using Windows-first execution paths (for example: `.\backend\scripts\test_backend.ps1` and `python -m pytest backend\tests`).
- Keep CI green by preventing flaky or stateful tests and by aligning fixtures with the FastAPI dependency model.

## 2. Test Pyramid Definition
- **Unit (base):** Fastest layer validating pure functions, helpers, and adapters with no network or database I/O. Target >60% of the suite volume.
- **Integration (middle):** Service, repository, and API wiring tests that exercise database interactions, FastAPI dependency overrides, and error handling. Target ~30% of coverage with focused fixtures per feature.
- **Contract (tip):** Stable response and schema assertions for published API surfaces and critical async handlers. Target ~10% to pin compatibility; use snapshot-free, explicit assertions.
- End-to-end/UI tests are owned by frontend scope; backend relies on contract coverage instead of UI automation.

## 3. Test Category Rules
- **Unit tests:**
  - Location: `backend\tests\unit` (create as needed).
  - May import domain helpers, validators, and mappers; must not touch the database or network.
  - Use pure data builders and deterministic inputs; avoid monkeypatching globals outside the test module.
- **Integration tests:**
  - Location: `backend\tests\integration` (create as needed) plus existing top-level API tests.
  - Exercise FastAPI routes via `TestClient`, repository calls via SQLAlchemy sessions, and dependency overrides for side effects.
  - Use fixture-provided sessions with rollback to guarantee per-test isolation; never rely on execution order.
- **Contract tests:**
  - Location: `backend\tests\contract` (create as needed).
  - Pin HTTP status codes, error envelope shape, and schema-critical fields for published routes and async job handlers.
  - Use explicit versioned paths (for example: `/api/v1/health/live`) and stable payloads; avoid snapshot files.

## 4. Database Isolation Strategy
- Default to an in-memory SQLite database with `StaticPool` for local and CI runs; connection string `sqlite+pysqlite:///:memory:` must be set by tests.
- Recreate metadata per test session before fixtures run, then use a rollback fixture to discard state after each test, even when commits occur.
- Alembic migrations remain out of scope for unit tests; integration tests may invoke migrations only when seeding schema changes is required.
- Never share ORM instances across tests; always request a fresh session from the factory fixture. Cross-test data dependencies are forbidden.

## 5. Async and Background Job Testing Rules
- Async route handlers should be exercised through FastAPI’s test client; prefer dependency overrides to fake external queues or email/sms senders.
- Background jobs must run in-process with stub transports (in-memory queue or function callbacks). No external brokers or services are permitted in tests.
- Use deterministic clocks and UUID generators (fixture-provided) to avoid flaky timing; avoid `sleep` and real retries.
- When asserting retries or idempotency, capture emitted audit/error events via in-memory collectors instead of hitting Redis or external sinks.

## 6. Forbidden Patterns
- Real network calls, cloud SDK usage, or reliance on external containers/services during tests.
- Cross-test ordering assumptions, shared mutable globals, or data persisted outside fixture-managed sessions.
- Thread.sleep/time.sleep-based timing, non-deterministic randomness without fixture seeding, or long-running loops.
- Snapshot files for API payloads; assertions must be explicit and aligned to contract specs.
- Bypassing FastAPI dependency overrides to inject credentials or org context; always use the fake auth context fixture instead.
