# Phase 2 Step 17 - Rate Limiting and Quotas

## Goals
- Define an organization-first rate limiting and quota strategy that aligns with the multi-tenant security boundary in docs/specs/03_multi_tenancy_and_security.md and docs/specs/24_security_model.md.
- Describe how limits are derived from authenticated context (org_id, roles, scopes, token_id) defined in docs/specs/08_rbac_model.md without changing endpoint behavior.
- Provide observability, audit, and error handling expectations consistent with docs/specs/09_audit_and_traceability.md and docs/specs/11_api_error_model.md.
- Establish enforceable placement and keying guidance for FastAPI/ASGI services using Redis while remaining implementation-neutral.

## Non-Goals
- No concrete limiter implementation, numeric budgets, or product-tier differentiation.
- No new endpoints or behavior changes; this document is specification-only.
- No override of abuse protections already defined in docs/specs/26_rate_limiting_and_abuse_protection.md; this spec refines quota and enforcement layering for Phase 2 Step 17.

## Threat Model and Abuse Patterns
- Cross-tenant exhaustion: malicious clients attempting to exhaust shared resources across organizations; guarded by mandatory org-scoped buckets.
- Token or credential abuse: rapid replay of valid tokens, burst traffic from compromised tokens, or automation keys over-enqueuing jobs.
- Anonymous/IP abuse: credential stuffing, unauthenticated probing, or excessive health/metadata polling prior to authentication.
- Privilege probing: repeated 401/403 responses triggered by scope escalation attempts or lateral movement across orgs.
- Distributed bursts: multiple tokens or IPs within the same org coordinating to bypass per-user limits; mitigated by parent org quotas.

## Rate Limiting Dimensions
- Organization (primary): every request with authenticated context is counted against an org-level bucket; this is the default scope for fairness and isolation.
- User: nested under organization to prevent a single actor from consuming all org capacity.
- Token/API key: nested under organization to isolate automation credentials and support revocation/rotation without impacting users.
- IP (supporting signal): used for unauthenticated flows and early authentication steps; combined with org/token scopes post-auth to detect distributed abuse.
- Endpoint class: read vs write vs admin vs auth flows; class selection influences which bucket family is consulted but does not change functional behavior.

## Quota vs Burst Distinction
- Quotas: fixed budgets over longer windows (e.g., hourly/daily) that cap aggregate consumption per organization and, when configured, per token. Quotas are designed to protect shared capacity and align with billing later without embedding product tiers.
- Burst limits: short windows that absorb brief spikes while preserving deterministic ceilings; enforced per org with optional per-user/token child buckets.
- Computation rules:
  - Always resolve org_id first; unauthenticated flows use IP+endpoint class until org context is available.
  - Burst consumption decrements both the burst bucket and the applicable quota bucket when a quota window is active.
  - RBAC scopes constrain which endpoint classes a token may access; rate limit evaluation never widens RBAC permissions and MUST deny requests lacking required scope before counting usage.

## Redis Key Model (Conceptual)
- Key prefixes are ASCII and deterministic to aid observability: `rl:{org_id}:{bucket}:{window}` for burst limits; `rq:{org_id}:{bucket}:{window}` for quotas.
- Bucket composition examples:
  - `{bucket}` may include `user:{user_id}`, `token:{token_id}`, `ip:{hashed_ip}`, and `class:{read|write|admin|auth}` segments as applicable.
  - Windows are encoded as fixed durations (e.g., `w60s`, `w1h`, `w1d`) with matching TTLs.
- Values store counters and optional metadata (last_update, retry_after) to enable consistent headers.
- Atomic operations (INCR/EXPIRE) are assumed; no multi-key transactions are required for this spec.

## Enforcement Layer Placement
- ASGI middleware placed early in the stack evaluates IP-based buckets for unauthenticated routes and captures request_id for observability.
- FastAPI dependency executed after authentication resolves org_id, user_id, token_id, roles, and scopes, then evaluates org/user/token buckets and applicable quotas.
- Background job enqueue points reuse the same dependency to evaluate org and token quotas before enqueuing; workers rely on upstream enforcement and do not introduce separate limits here.
- Admin and bulk routes use stricter endpoint classes but share the same enforcement surfaces; no hidden gateway-only rules.

## Headers and Error Mapping
- Exceeded limits return HTTP 429 with `error.code` set to `throttling.rate_limit_exceeded` per docs/specs/11_api_error_model.md.
- Headers (ASCII only):
  - `RateLimit-Limit`: active bucket limit and window description.
  - `RateLimit-Remaining`: remaining capacity in the evaluated bucket.
  - `RateLimit-Reset`: UTC epoch seconds when the bucket resets.
  - `Retry-After`: optional seconds when a delay is advised (for burst exhaustion only).
- When multiple buckets apply, headers reflect the most constraining bucket (usually organization); bodies MUST include request_id and timestamp fields.

## Audit, Observability, and Logging
- Structured logs on every throttle decision include: org_id, user_id (when available), token_id, endpoint class, bucket identifiers, request_id, and the applied error code.
- Metrics: counters such as `rate_limit_exceeded_total{scope,endpoint_class}` and gauges for remaining quota per org; align tag names with auth context fields.
- Audit events are emitted for repeated throttling on authenticated actors (e.g., threshold of consecutive 429s) and for IP-based blocking on auth flows; records include org_id, actor_id, token_id, request_id, and correlation_id per docs/specs/09_audit_and_traceability.md.
- Sampling is permitted for informational logs but not for audit events tied to security-relevant throttling.

## Failure Modes and Fallback Behavior
- Redis unavailable (transient): apply a conservative in-process fallback with minimal per-process ceilings for authenticated requests, fail-closed for admin and auth endpoints, fail-soft (small static budget) for idempotent GET health/metadata routes, and emit alerts/metrics indicating degraded enforcement.
- Redis unavailable (prolonged): expose HTTP 503 for endpoints where safety cannot be guaranteed (admin/auth), and 429 with a clear `throttling.enforcement_degraded` detail for others; never silently drop requests.
- Corrupted or missing keys: regenerate bucket state with zeroed counters and log the anomaly; do not reset other buckets.
- Clock skew: rely on monotonic timers in the middleware/dependency; headers and logs note server time as authoritative.

## Out of Scope
- Selecting specific Redis deployment topology, sharding, or TLS settings.
- Client-side retry policies beyond standard 429 handling.
- Product-tier or contractual quotas; future commercial policies will build on the org-scoped quotas defined here.
