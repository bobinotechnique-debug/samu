# Phase 2 Step 17 - Rate Limiting, Quotas, and Abuse Protection Alignment

## Status
Starting

## Objective
Document an organization-first rate limiting and quota strategy for the API that aligns with RBAC scopes, audit/observability rules, and the FastAPI + ASGI stack using Redis for conceptual storage, without changing runtime behavior.

## Deliverables
- docs/specs/25_rate_limiting_and_quotas.md capturing goals, non-goals, threat model, limiting dimensions, quota vs burst distinctions, Redis keying strategy, enforcement placement, headers/error mapping, audit/log interactions, and failure/fallback behavior.
- Index updates registering the specification under Phase 2 artifacts.
- Roadmap status reflecting completion of the documentation-first scope for Step 17.

## Dependencies
- Phase 1 security and ownership: docs/specs/03_multi_tenancy_and_security.md, docs/specs/08_rbac_model.md, docs/specs/09_audit_and_traceability.md.
- Phase 2 security model: docs/specs/24_security_model.md.
- API error handling: docs/specs/11_api_error_model.md.
- Prior abuse protection baseline: docs/specs/26_rate_limiting_and_abuse_protection.md.

## Acceptance Criteria
- All limits are organization-scoped by default with clear child scopes (user, token, IP) and no contradictions with existing security specs.
- Documentation separates quotas from burst limits and avoids product-tier business rules.
- Enforcement placement, headers, and deterministic error behavior are defined without altering endpoints or adding runtime logic.
- Redis failure behavior and audit/observability integration are explicitly documented.
- Indexes and this roadmap entry reference the new specification; content remains ASCII with no TODOs.

## Explicit Exclusions
- No implementation of rate limiting middleware, handlers, or concrete numeric budgets.
- No modifications to existing endpoints, contracts, or behavior beyond documentation.
- No business-tier or contractual quota rules; future tiers will build on the documented org-scoped model.
