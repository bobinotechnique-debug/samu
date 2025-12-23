# Bootstrap Implementation Plan

## Purpose
Concrete execution plan for Phase 2 Step 10 (Implementation Bootstrap) to deliver runnable backend/frontend skeletons without domain logic.

## Scope
- Backend: FastAPI app factory, routing composition, settings/deps, DB session wiring, health endpoints only, smoke tests.
- Frontend: React app shell with router/layout, shared API client wrapper, placeholder pages, smoke tests.
- CI/guards: Ensure guards + lint + tests run for backend and frontend; add minimal workflow wiring only if missing.

## Files to touch (expected)
- docs/audits/implementation_readiness.md
- docs/audits/bootstrap_implementation_plan.md (this file)
- docs/audits/bootstrap_implementation_report.md
- backend/app/main.py, backend/app/api/* (health, deps, errors), backend/app/core/config.py, backend/app/core/db/session.py (if needed), backend/tests/*
- frontend/src/app/*, frontend/src/pages/*, frontend/src/shared/api/*, frontend/src/test/*
- .github/workflows/* or scripts/PS1/* only if CI gaps found.

## Tasks
1) Backend bootstrap
- Align app factory with docs/api/20_api_architecture.md (single api prefix, non-versioned /health/live and /health/ready, optional /api/v1/health alias).
- Ensure Settings + get_settings dependency, DB session dependency (yield pattern), testing-safe defaults.
- Add/confirm health response model with timestamp and checks placeholders only.
- Smoke tests: app starts, /health/live 200, /health/ready shape + status, compatibility alias (if present).

2) Frontend bootstrap
- App shell + router scaffold with placeholder routes (no business logic).
- Shared API client wrapper using env base URL and error mapping skeleton to docs/specs/11_api_error_model.md.
- Placeholder pages rendering headings only.
- Smoke tests: app renders root route, router navigates, API client instantiation without network.

3) CI/guards
- Validate guards command and lint/test commands for backend/frontend.
- Add workflow updates only if existing CI misses guards + lint + tests.

## CI expectations
- Guards: tools/guards/run_guards.py (or PS1 equivalent) is green locally and in CI.
- Backend: lint/test commands succeed (ruff/pytest per repo tooling).
- Frontend: lint/test commands succeed (eslint/prettier/vitest per repo tooling).

## Stop conditions
- Any failing guard/lint/test that requires business logic to fix.
- Ambiguity on health endpoint contract or routing prefix.
- Non-ASCII content introduction.
- Missing roadmap linkage to docs/roadmap/phase2/step-10-implementation-bootstrap.md.

## Next step
- Implement bootstrap wiring in backend and frontend per above, then record results in docs/audits/bootstrap_implementation_report.md with executed commands.
