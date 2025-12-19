# Operations Documentation Index

This index governs operational records, including guard behaviors and error logs.

- Status and inventory: docs/STATUS_SUMMARY.md.

## Files
- docs/ops/agent_errors.md - mandatory failure memory log.
- docs/ops/20_deployment_architecture.md - Phase 2 deployment and environment architecture (local, CI, staging, production).
- docs/ops/21_observability.md - Phase 2 observability baseline (logging, metrics, tracing, health checks, alerting, runbooks).
- docs/ops/21_observability_and_logging.md - Phase 2 Step 14 authoritative observability, structured logging, correlation, and audit hook contract.
- docs/ops/22_local_run_flow.md - Local vertical slice run flow with migrations, seed, and service startup commands.
- docker-compose.yml - local/dev service wiring for api, worker, db, cache, and frontend aligned to deployment architecture.

## Rules
- Log every Codex failure once using the required template.
- Keep operational guidance ASCII-only to satisfy guard expectations.
