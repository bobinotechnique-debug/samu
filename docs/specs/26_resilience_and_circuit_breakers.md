# Phase 2 Step 18 - Circuit Breakers and Resilience Policies

## Purpose
Define enforceable resilience mechanisms that prevent cascading failures across internal services and external dependencies by standardizing circuit breakers, retries, backoff, and timeouts while preserving auditability and rate limiting guarantees.

## Scope
- Applies to synchronous APIs, internal service-to-service calls, external provider integrations, and async job workers.
- Documentation only; no runtime configuration, library choice, or code changes are introduced in this step.
- Aligns with Phase 1 failure patterns (docs/specs/06_known_failure_patterns.md) and Phase 2 constraints for audit (docs/specs/09_audit_and_traceability.md), async jobs (docs/specs/23_async_jobs.md), and security (docs/specs/24_security_model.md).

## Design Goals
- Avoid cascading failures by failing fast when dependencies misbehave.
- Preserve org-level isolation and rate limiting boundaries during failure and recovery.
- Ensure predictable latency through explicit timeouts and bounded retries.
- Maintain auditability, observability, and deterministic recovery paths.

## Failure Categories
| Category   | Definition | Examples | Retry stance |
|------------|------------|----------|--------------|
| Transient  | Short-lived issues expected to resolve without code changes. | Network timeout, brief DB failover, external 5xx, rate limit 429 with Retry-After. | Retry allowed when the operation is idempotent and within budget. |
| Persistent | Issues unlikely to clear without operator action or fixes. | Schema mismatch, invalid payload, repeated auth failure, exhaustion of quotas. | No retries; surface error and require remediation. |
| External   | Failures in third-party providers or outbound services. | Payment API outage, messaging provider timeout. | Retries permitted only when idempotent and provider signals transient error. |
| Internal   | Failures within our services or data stores. | Service dependency saturation, deadlocks, cache outage. | Retries bounded; circuit breakers protect upstream callers. |

## Circuit Breaker Model
- **States**
  - Closed: normal flow; record success/failure rates.
  - Open: fail fast with `dependency.circuit_open` error code; reject new calls for a cool-down window.
  - Half-open: allow limited probes (fixed small concurrency) to test recovery; success rate determines close vs reopen.
- **Transition triggers (default, override-per-service allowed but MUST be documented):**
  - Open when failure rate >= 50 percent over the last 20 requests **or** 5 consecutive timeouts/errors for a dependency.
  - Transition to half-open after a cool-down window of 30-60s (documented per dependency).
  - Close when the half-open probe window reaches at least 5 consecutive successes or < 20 percent failure rate across 10 probes.
- **Guardrails**
  - Breakers wrap external providers and non-core internal services; core transactional DB writes rely on timeouts and retries, not breaker-induced fallbacks.
  - Breakers MUST NOT introduce alternate data sources or stale-cache fallbacks; they only fail fast.
  - Breaker configuration (thresholds, cool-downs, probe limits) MUST be declared alongside the owning service spec and validated by CI/guards.

## Retry Rules
| Context | Allowed | Forbidden |
|---------|---------|-----------|
| Synchronous API handlers | Single bounded retry for idempotent operations on transient infrastructure errors (5xx, timeout) before surfacing structured error. | No retries for validation/authz/domain errors, org boundary violations, or rate limit 429 responses. |
| Internal service calls | Bounded retries (max 2) with backoff for idempotent read/write operations when dependency is healthy (breaker closed) and failure is transient. | No retries when breaker is open/half-open unless probing budget is available. |
| External providers | Retries allowed only on explicit transient signals (5xx, 429 with Retry-After) and only for idempotent operations; honor provider backoff hints when present. | No retries on 4xx (except 429), signature/auth failures, or when idempotency is not guaranteed. |
| Async jobs (Step 05) | Follow docs/specs/23_async_jobs.md category defaults; retries remain capped with deadletter on exhaustion. | No retries for validation, authorization, or business rule violations. |

## Backoff Strategy (Documented Only)
- Exponential backoff with full jitter is the standard; deterministic caps must be documented per call type.
- Defaults unless stricter service rules are defined:
  - Base delay: 1s; multiplier: 2x; max delay: 30s for synchronous internal calls.
  - External provider calls: base 2s; max delay 60s; respect Retry-After headers when present but cap at the documented max.
  - Async jobs keep the base/max attempts defined in docs/specs/23_async_jobs.md; jitter remains mandatory.
- No unbounded or immediate tight loops; retries MUST fit within the parent timeout budget.

## Timeout Standards
| Call type | Default budget | Hard cap | Notes |
|-----------|----------------|----------|-------|
| Public/API requests | 2s target, aligned to UX latency budgets; warn at 1.5s. | 5s absolute per request, including retries. | If exceeded, return dependency or server timeout codes with request_id and correlation_id. |
| Internal service-to-service | 1s per hop. | 3s including retries per request chain. | Timeout must be shorter than API budget to avoid cascade. |
| Database (OLTP) | Statement timeout 500-800ms for primary workloads. | 2s; longer queries require explicit approval and async job offload. | Timeouts must be logged with SQL operation metadata (sanitized). |
| Async job execution | 60s per attempt for default jobs; 300s cap for exports/imports with explicit justification. | 300s absolute per attempt. | Attempt timeout must align with job category SLOs and not bypass deadletter rules. |
| External APIs | 2s default; 5s for file or provider-documented long-lived endpoints. | 10s cap with explicit justification. | Never rely on provider defaults; set both connect and read timeouts. |

## Interaction with Rate Limiting (Step 17)
- Rate limit errors (429) are not retried until the documented window resets; respect Retry-After and propagate headers defined in docs/specs/25_rate_limiting_and_quotas.md and docs/specs/26_rate_limiting_and_abuse_protection.md.
- Circuit breakers MUST treat sustained 429 responses as a signal to reduce load; avoid opening breakers for well-behaved throttling but enforce backoff.
- Org-level limits remain authoritative; retries MUST NOT cross org boundaries or bypass per-org quotas.

## Interaction with Async Jobs (Step 05)
- Workers check breaker state before invoking downstream dependencies; if open, emit `job.deferred_due_to_breaker` audit/log entry and reschedule within the remaining attempt budget.
- Retry and timeout limits inherit docs/specs/23_async_jobs.md; this document adds breaker awareness and prohibits silent retries outside that contract.
- Jobs MUST preserve idempotency keys across retries and breaker transitions to avoid duplicate side effects.

## Observability and Audit Requirements
- **Logs:** Structured logs MUST include request_id, correlation_id, org_id, circuit identifier, state transitions, failure category, and timeout metadata. No secrets or PII beyond audit policy.
- **Metrics:** Minimum gauges/counters per breaker: `breaker_state{circuit}`, `breaker_open_total{circuit}`, `breaker_half_open_total{circuit}`, `breaker_reject_total{circuit}`, latency histograms per dependency, and retry counters by error class. Metrics MUST be org-aware when applicable.
- **Traces:** Spans MUST include circuit state and retry attempts; propagate W3C trace context through internal calls and jobs.
- **Audit:** Breaker open/close events affecting org-facing operations MUST generate audit records per docs/specs/09_audit_and_traceability.md, including org_id, request_id, correlation_id, circuit name, reason, and operator if manual override occurred.

## Non-Goals
- No auto-healing scripts or infrastructure failover logic are introduced here.
- No silent retries or fallback to stale data when breakers open.
- No library- or framework-specific configuration snippets.
- No modification to RBAC, ownership boundaries, or API schemas beyond documenting enforcement expectations.
