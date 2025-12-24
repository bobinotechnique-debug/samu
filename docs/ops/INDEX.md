# Operations Documentation Index

This index governs operational records, including guard behaviors and error logs.

- Status and inventory: docs/STATUS_SUMMARY.md.

## Files
- docs/ops/agent_errors.md - mandatory failure memory log.
- docs/ops/20_deployment_architecture.md - Phase 2 deployment and environment architecture (local, CI, staging, production).
- docs/ops/21_observability.md - Phase 2 Step 09 operations baseline (metrics, tracing, log shipping, health checks, alerting, dashboards, runbooks) with canonical non-versioned /health/live and /health/ready contracts; defers structured logging schema to Step 14.
- docs/ops/21_observability_and_logging.md - Phase 2 Step 14 authoritative structured logging, correlation, and audit hook contract; excludes metrics/tracing/runbooks covered by Step 09.
- docs/ops/22_local_run_flow.md - Phase 2 Step 11 vertical slice run flow with migrations, seed, and service startup commands; referenced by roadmap Step 11 deliverables.
- docker-compose.yml - local/dev service wiring for api, worker, db, cache, and frontend aligned to deployment architecture.

## Rules
- Log every Codex failure once using the required template.
- Keep operational guidance ASCII-only to satisfy guard expectations.
