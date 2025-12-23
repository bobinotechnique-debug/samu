# Bootstrap Implementation Plan (Phase 2 Step 10)

## Scope and intent
- Deliver runnable backend and frontend skeletons bound to docs/roadmap/phase2/step-10-implementation-bootstrap.md.
- Health/meta only; no business routers, domain workflows, or UI business logic are enabled in this step.
- Align with API/versioning/error specs (docs/specs/10_api_conventions.md, docs/specs/11_api_error_model.md, docs/specs/12_api_versioning.md) and frontend architecture guardrails (docs/ux/20_frontend_architecture.md).

## Files to touch
- Documentation: docs/audits/implementation_readiness.md (refresh), docs/audits/bootstrap_implementation_plan.md (this plan), docs/audits/bootstrap_implementation_report.md (execution log), docs/audits/INDEX.md (index update).
- Backend: app factory, settings, health router, db session dependency, tests under backend/tests covering app startup and health probes only; remove business router wiring from app/api/v1/router.py.
- Frontend: routing shell in src/app/routes, AppLayout shell, placeholder pages in src/pages/*, API client in src/shared/api/http.ts, supporting tests in src/app and src/shared/api.
- Configuration: .env.example alignment for frontend base URL defaults, package.json scripts for lint/build coverage.
- CI: .github/workflows/ci.yml to ensure guards + backend tests + frontend lint/build/test; avoid reintroducing placeholder workflows beyond minimal scope.

## Tests and checks to add/maintain
- Backend smoke tests: FastAPI app boots; /health/live returns 200 with stable payload; /health/ready and /api/v1/health compatibility alias follow status semantics without requiring real DB in testing mode.
- Frontend smoke tests: AppShell renders planning heading via redirect; router handles mission detail route and unknown routes; API client builds versioned and non-versioned URLs and maps non-2xx responses to typed errors.
- Lint/type/build: backend syntax guard (ruff or equivalent if defined), frontend lint (tsc/ESLint), frontend build (Vite), guards runner.

## CI expectations
- Single matrix job in .github/workflows/ci.yml runs: python tools/guards/run_guards.py; backend lint guard (existing ruff) + pytest; npm ci; npm run lint; npm run build; npm run test.
- PowerShell and POSIX command variants documented in docs/audits/implementation_readiness.md remain the verification contract.

## Explicit constraint
- Health/meta only, no business routers.
