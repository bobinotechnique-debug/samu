# Phase 2 Step 15 - Rate Limiting and Abuse Protection

## Purpose
Define enforceable rate limiting and abuse protection rules that respect organization boundaries, align with API conventions, and remain observable across environments without introducing hidden throttling paths.

## Scope
- Applies to API gateway, application services, background job enqueue points, and authentication flows.
- Covers scopes, limit shapes, error responses, headers, and observability expectations. Does not implement middleware or infrastructure.

## Authoritative inputs
- docs/specs/10_api_conventions.md
- docs/specs/11_api_error_model.md
- docs/specs/23_async_jobs.md
- docs/specs/08_rbac_model.md
- docs/specs/09_audit_and_traceability.md
- docs/ops/21_observability_and_logging.md

## Rate limit scopes
- Organization: Primary boundary. Separate buckets per org_id; prevents cross-tenant impact and is mandatory for all authenticated traffic.
- User: Secondary guardrail to mitigate account-level abuse; scoped under org buckets.
- Token/API key: Distinct limits per credential to isolate automation clients; scoped to org and role claims.
- IP: Applied only when authentication is absent or during login flows; used as an anti-abuse signal, not as the primary limiter.
- Endpoint class: Read vs write vs admin endpoints may have differentiated buckets; admin and bulk endpoints carry stricter budgets.

## Default limit shapes (illustrative)
- Use token-bucket or leaky-bucket semantics with burst and sustained components. Example: short bursts allowed for single-page fetches, with lower sustained rates for bulk operations.
- Reads permit higher bursts within org bounds; writes use lower bursts and tighter sustained rates to protect database and audit pipelines.
- Authentication endpoints use separate small bursts with strict sustained ceilings to deter credential stuffing.
- Background job enqueue points use bounded bursts per org with alignment to queue capacity from docs/specs/23_async_jobs.md to avoid overloading workers.

## Burst vs sustained rules
- Bursts MUST be short-lived and capped; sustained limits enforce long-term fairness. Both are enforced per scope (org, user, token).
- Exceeding burst but not sustained budgets SHOULD trigger soft throttling (slight delay) before hard 429 responses, provided the delay is declared and minimal.
- Limits MUST be documented and environment-tunable without code changes; production defaults SHOULD be stricter than local.

## Interaction with authentication and RBAC
- Rate limit evaluation occurs after authentication where possible to attach org_id and role context; anonymous flows rely on IP + endpoint class.
- Privileged roles (org_owner, org_admin) are not exempt; they may receive slightly higher burst ceilings but MUST remain within org-level budgets.
- Service-to-service calls use dedicated credentials and buckets; they MUST NOT reuse end-user quotas.
- Rate limit decisions MUST be auditable with actor_id, org_id, token_id (where applicable), and request_id captured per docs/specs/09_audit_and_traceability.md.

## Error responses and headers
- Throttled requests return HTTP 429 with error.code set to throttling.rate_limit_exceeded per docs/specs/11_api_error_model.md.
- Response headers align with API conventions: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, and `Retry-After` when delays are advised. Values MUST reflect the active scope (org/user/token) and be ASCII.
- Bodies MUST include request_id and timestamp fields and must not suggest client-side retries beyond documented idempotent cases.

## Abuse signals and protections
- Detect anomalies such as sudden burst spikes across multiple tokens in the same org, repeated 401/403 responses, or high error rates for a single IP.
- Suspicious patterns trigger tighter temporary limits or authentication challenges; all actions MUST be logged with correlation identifiers and, when security-relevant, audited.
- Login and token issuance flows SHOULD include incremental delays or captcha-like challenges in the future; these are documented but not implemented here.

## Audit and observability expectations
- Emit structured logs for throttle decisions with org_id, actor_type, actor_id, token_id, request_id, error_code, and applied bucket identifiers.
- Produce metrics such as `rate_limit_exceeded_total{scope,endpoint_class}` and latency histograms when soft throttling is used.
- Maintain dashboards and alerts for sustained 429 rates per org to detect abusive tenants or misconfigured clients.
- All protections must remain transparent: no silent drops, no hidden backpressure that lacks logging or metrics.

## Non-goals and forbidden patterns
- No hardcoded numeric limits inside application code; limits are configuration-driven per environment.
- No shared global bucket across organizations; org boundary is mandatory.
- No silently deferred requests; if delayed, delays are minimal, declared, and observable.
- No client-side exponential retry guidance for throttling; clients should honor Retry-After and documented idempotency rules only.
