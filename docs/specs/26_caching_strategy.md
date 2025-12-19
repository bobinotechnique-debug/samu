# Phase 2 Step 19 - Caching Strategy

## Goals
- Define an explicit, opt-in caching strategy for the FastAPI backend with predictable behavior and observability hooks aligned to docs/roadmap/phase2/step-14-observability-and-logging.md.
- Enforce multi-tenancy safety by design through organization-scoped keys, explicit TTLs, and deterministic invalidation rules consistent with docs/specs/03_multi_tenancy_and_security.md and docs/specs/24_security_model.md.
- Ensure cache usage does not bypass rate limiting (Phase 2 Step 17) or resilience controls (Phase 2 Step 18) and degrades safely when Redis or local caches are unavailable.

## Non-Goals
- No cache middleware or library selection; this document is specification-only.
- No implicit caching of responses, queries, or computed data; every cache entry must be declared with a resource-specific TTL and invalidation rule.
- No product-tier differentiation or per-tenant policy negotiation beyond the organization security boundary.

## Cache Layers
| Layer | Scope | Allowed Data | TTL Rule | Isolation | Observability |
| --- | --- | --- | --- | --- | --- |
| Local in-process cache | Single worker/process memory | Safe-to-recompute read models, feature-flag resolutions, and static lookup tables; no secrets or PII beyond identifiers required for authorization | Hard TTL per entry; default max 120s and never infinite | Process-local; no sharing across workers; cleared on deploy/roll | Structured logs and metrics for hits/misses/evictions; trace span annotates cache layer = `local` |
| Redis | Shared across workers and services | Idempotent GET responses, read-only projections, feature-flag documents, and rate-limit neutral metadata; no session tokens or credential material | Explicit TTL per resource; defaults documented in TTL table below; no eternal keys | Organization-scoped keys; org_id is mandatory; separate DB or prefix per environment | Metrics for latency, hit ratio, error rate; logs include org_id, cache_key, result; traces mark Redis calls and circuit breaker state |

## Cache Key Format
- Template (ASCII only): `cache:{env}:{service}:{org_id}:{resource}:{variant}:{identifier}`.
- Segment rules:
  - `{env}`: deployment environment (dev|staging|prod); required to prevent cross-environment bleed.
  - `{service}`: backend service name (`api` for FastAPI backend) to isolate multi-service usage.
  - `{org_id}`: required organization identifier; `anon` allowed only for pre-auth public resources.
  - `{resource}`: stable noun describing the cached item (e.g., `project_read_model`, `feature_flag_bundle`).
  - `{variant}`: optional scope such as locale, role set hash, or parameter signature; must not include PII.
  - `{identifier}`: stable resource identifier (UUID) or deterministic hash of request parameters; hashes must be salted per service and non-reversible.
- Versioning: include `v{n}` in `{resource}` or `{variant}` when schema or serialization changes; older versions must expire naturally through TTLs.

## TTL Rules (Explicit)
| Resource Family | Example Resources | TTL | Rationale |
| --- | --- | --- | --- |
| Feature flags/config toggles | Feature flag bundle per org | 60s | Fast convergence while limiting Redis churn; aligns with docs/specs/26_feature_flags.md polling guidance |
| Read-only projections | Project read model, mission summary, dashboard aggregates | 120s | Limits staleness while avoiding repeated expensive reads; safe because mutations trigger explicit invalidation |
| Reference data | Countries, roles, static lookup tables | 6h | Rarely change; long TTL reduces load; invalidation on publish/deploy |
| Auth-adjacent metadata | Public JWKS, well-known config | 300s | Moderate TTL to balance freshness and availability without storing credentials |
| Negative cache entries | Known-missing IDs for read paths only | 30s | Short TTL to avoid masking new data; never used for write flows |

## Invalidation Strategy
- Principles: cache entries must be invalidated deterministically; no hidden timers beyond TTLs.
- Event-driven invalidation (preferred):
  - Domain mutations (create/update/delete) emit cache purge events keyed by `org_id` and affected resource identifiers.
  - Deployment hooks clear local caches and publish version bump to Redis prefix to force miss until repopulation.
- Manual/operational invalidation: admin-only endpoint or ops script triggers targeted Redis key deletion by prefix; actions are audited with org_id and request_id.
- Local cache invalidation: per-entry TTL plus immediate purge on process restart or deploy; circuit breaker open for Redis triggers local cache TTL halving to reduce staleness.
- No write-through or write-back caching; only read-through and explicit populate patterns are permitted.

## Failure Modes and Fallbacks
| Scenario | Expected Behavior |
| --- | --- |
| Redis unavailable (transient) | Circuit breaker (Phase 2 Step 18) opens after bounded failures; requests proceed without Redis cache, relying on local cache when safe; log `cache.degraded.redis_unavailable` and emit alert. |
| Redis unavailable (prolonged) | Redis calls bypassed; critical paths may return HTTP 503 if data freshness cannot be ensured; org-level audit records capture duration and impacted resources. |
| Local cache poisoning or stale data detected | Immediately drop local cache entry, bypass until next successful populate; emit security signal and metric `cache.local.poisoned_total`. |
| Invalidation event failure | Retry with backoff (respecting circuit breaker budgets); if retries exhausted, force expire impacted prefixes with minimal TTL and log `cache.invalidate_failed`. |
| Serialization errors | Do not cache; return upstream response; log error with request_id, org_id, resource, and do not retry. |

## Observability and Audit Alignment (Phase 2 Step 14)
- Metrics: `cache_hits_total{layer,resource}`, `cache_misses_total{layer,resource}`, `cache_errors_total{layer,resource,reason}`, `cache_latency_ms_bucket{layer}`.
- Logs: structured log per cache decision with fields `layer`, `resource`, `org_id`, `cache_key`, `result` (hit|miss|bypass|error), `ttl_seconds`, `request_id`, `breaker_state` (closed|open|half_open).
- Traces: span attributes include cache layer, key hash (not the full key), TTL, and breaker state; Redis spans nest under request trace with clear error tags.
- Audit: admin-triggered invalidations and bypass toggles are audited with actor_id, org_id, request_id, and reason.

## Security and Multi-Tenancy Constraints
- Org boundary is mandatory: caches must never combine or share data across `org_id` values; `org_id` segment is required except for explicitly public resources (which use `anon`).
- No caching of credentials, session tokens, or personally identifiable information; cached payloads must be minimized and redact sensitive fields.
- Data classification: only `public` or `internal` classification items may be cached; `restricted` data requires explicit approval and encryption-at-rest in Redis, with TTL <= 60s.
- Hash inputs used in keys must be salted per service, non-reversible, and avoid embedding PII or secrets.
- Access controls: cache warmers and invalidators require authenticated service identity with audit trail; no unauthenticated cache control endpoints.

## Usage Rules (Opt-In Only)
- Each cached resource declares: key template, TTL, invalidation triggers, and layer selection before implementation.
- Cache usage is forbidden for write operations, RBAC decisions, or rate limiting decisions; rate limit counters (Phase 2 Step 17) live separately and are not mixed with response caches.
- Populate on read only after RBAC and authorization checks; cache misses must not alter authorization flows.
- Circuit breaker alignment (Phase 2 Step 18): Redis access respects timeout budgets, contributes to breaker metrics, and never retries indefinitely; breakers reset independently per `service+org_id` shard to avoid cross-tenant coupling.
