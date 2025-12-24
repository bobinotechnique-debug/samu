# Phase 2 Step 10 - Smoke Test Contract

## Purpose
Define the minimal smoke tests that validate the bootstrap scaffolding across backend, frontend, and ops surfaces without exercising business logic.

## Scope
- Applies to local and CI pipelines that run after Step 10 bootstrap wiring.
- Targets health endpoints, frontend shell availability, and Docker Compose orchestration.
- Excludes domain workflows, migrations beyond connectivity checks, and performance or load testing.

## Test matrix
- Backend: start API and worker containers; assert `/health/live` and `/health/ready` respond with status and request_id fields; confirm readiness fails when database is offline.
- Frontend: build succeeds; `/health` route renders health stub and surfaces request/correlation identifiers when provided.
- Ops: Docker Compose profile for bootstrap brings up api, worker, db, cache, and frontend; migrations run automatically or via PS1 scripts without manual secrets.

## Acceptance criteria
- All smoke checks run via a single command documented in README or scripts directory with CI-safe defaults.
- Outputs remain ASCII-only and include clear pass/fail markers for automation.
- Logs produced during smoke runs follow docs/ops/21_observability_and_logging.md field requirements.

## Traceability
- Roadmap: docs/roadmap/phase2/step-10-implementation-bootstrap.md
- Related audits: docs/audits/bootstrap_implementation_plan.md, docs/audits/bootstrap_implementation_report.md
