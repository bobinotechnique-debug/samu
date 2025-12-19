# Phase 2 Step 09 - Observability and Operations Baseline

## Scope and goals
- Baseline observability contract aligned to Phase 1 audit/ownership rules and Phase 2 async/jobs/deployment decisions.
- Compatible with Windows-first tooling, Docker Compose environments, and GitHub Actions runners.
- No business-logic changes; only operational instrumentation requirements.

## Structured logging
- **Format:** JSON lines with mandatory fields: `timestamp` (UTC ISO8601), `level`, `message`, `service`, `environment`, `org_id`, `project_id` (when available), `request_id` (per inbound HTTP request), `correlation_id` (cross-hop), `span_id` and `trace_id` (when tracing is on), `user_id` (when authenticated), `ip`, `route`, `duration_ms` (for requests/jobs), `outcome` (`success` | `error` | `retry`), and `source` (`api` | `job` | `frontend` | `worker`).
- **Correlation propagation:**
  - Frontend attaches `X-Correlation-Id` on all API calls; API echoes it in responses and injects it into job payloads/enqueued metadata.
  - Background jobs keep both `correlation_id` and upstream `request_id` in the job context; retries preserve these values.
  - Outbound calls (DB, Redis, queue, external HTTP) include the correlation ID in logs to stitch traces.
- **Error logging:**
  - Log exceptions with stack traces under `error.type`, `error.message`, and `error.stack` fields.
  - Map HTTP status to `outcome` and capture validation failures with `org_id` and `route` to satisfy audit rules.
- **Sampling:** Allow log level/sampling to be configured per environment (dev verbose, staging debug, prod info/error) without code edits.

## Metrics
- **Exposure:** Prometheus-compatible `/metrics` endpoint on the API; workers export the same registry over HTTP (configurable port) or push-gateway if pull is blocked.
- **HTTP metrics:** request count, latency histograms, active requests, and error rate by `route`, `method`, and `status`.
- **Job metrics:** enqueued/active/success/failure/retry counters by queue and job type; execution duration histogram; dead-letter count.
- **Database metrics:** connection pool size/usage, wait time, slow query count, and transaction rollback counter.
- **Cache/queue metrics:** Redis availability ping gauge, operation latency, and queue backlog depth.
- **Resource metrics:** process CPU/memory, file descriptors, and thread count for capacity signals on Windows and Linux runners.

## Tracing
- **Choice:** OpenTelemetry-compatible instrumentation with W3C Trace Context headers.
- **Mode:**
  - Off by default for local unless explicitly enabled.
  - Dev/staging: 10-20% sample rate to validate spans and propagation.
  - Prod: adjustable sampler; start with 5-10% and raise on incident.
- **Coverage:** inbound HTTP spans, DB queries, Redis calls, queue publish/consume, and job execution spans stitched via `trace_id`/`span_id`.

## Health checks
- **Canonical endpoints (non-versioned):**
  - `GET /health/live` -> process up only, no dependency checks, fast response.
  - `GET /health/ready` -> readiness for serving traffic; MUST check database connectivity; include cache/queue only when they are required for handling inbound requests.
- **Compatibility alias:** `/api/v1/health` may exist for legacy callers but is non-canonical and should proxy readiness semantics. Do not wire orchestrator probes to the alias.
- **Workers:** worker readiness mirrors API readiness and adds queue subscription/heartbeat capability checks when workers must process traffic.
- **Responses:** JSON only with `status`, `timestamp`, and per-dependency fields under `checks`; no secrets or stack traces. Keep endpoints unauthenticated so platform probes and load balancers can poll directly.

## Alerting (minimal documented baseline)
- Alert when any ready check fails for >2 minutes.
- Alert on sustained HTTP 5xx/error-rate spike (>2% over 5 minutes) or latency SLO breach.
- Alert on job failure/retry surge, dead-letter growth, or backlog age exceeding SLA.
- Alert on DB connection pool exhaustion, migration failures, or Redis unavailability.
- Alert on missing metrics scrape for >5 minutes from API or workers.

## Runbooks (abridged)
- **API down:** check `/health/live` vs `/health/ready`; inspect recent deploys; roll back to last green image; verify DB/Redis connectivity.
- **DB down:** confirm `/health/ready` DB check; failover/restore service; scale connection pool down in config to reduce storm once back.
- **Redis down:** verify ping failure; restart container/service; drain or pause job publishers until cache/broker is stable.
- **Queue backlog:** check backlog depth metric and dead letters; scale workers horizontally; enable tracing sample bump for failing job types; pause noisy producers if needed.
- **Migration fail:** read migration logs; apply fix forward or roll back; re-run migrations with correlation ID noted in audit log; keep app in maintenance until ready passes.

## Implementation notes
- Keep middleware/adapters responsible for inserting `correlation_id`/`request_id` so business logic stays clean.
- Default configurations must run under Docker Compose, Windows (PowerShell scripts), and GitHub Actions runners without external secrets.
- Document any temporary gaps in docs/ops/agent_errors.md if failures occur during adoption.
