# Feature Flags and Configuration Toggles (Phase 2 Step 16)

## Purpose
- Provide an authoritative scaffolding for feature flags and configuration toggles in the FastAPI backend.
- Establish deterministic evaluation rules, naming conventions, and storage strategy before introducing any business logic.
- Align toggle evaluation with observability and security baselines defined in prior steps.

## Non-Goals
- Implement runtime feature gating for business logic.
- Introduce remote flag providers or dashboards.
- Bypass existing RBAC, audit, or data ownership boundaries.

## Definitions
- **Feature flag**: Boolean control used to enable or disable application behavior without deploying code.
- **Configuration toggle**: Boolean configuration switch used to adjust non-functional runtime behavior (e.g., optional connectors) without altering authorization rules.

## Flag Types
- **Env-scoped**: Values provided per environment (local, ci, staging, production) via environment variables.
- **Global**: System-wide defaults applied when no environment or organization override is present.
- **Org-scoped**: Overrides bound to a specific organization identifier.

## Precedence (highest to lowest)
1. Environment override.
2. Organization override.
3. Global default.
4. Hardcoded fallback.

## Naming Conventions
- Flag keys: `lower_snake_case`.
- Group prefixes: `planning_`, `missions_`, `collabs_`, `billing_`, `ops_`.
- Environment variables use the `FEATURE_` prefix with uppercase segments that normalize to the lowercase key (e.g., `FEATURE_PLANNING_TIMELINE_V2` -> `planning_timeline_v2`).

## Evaluation Contract
- Pure, deterministic function with no side effects.
- Inputs: `key`, `org_id` (optional), and `env` string.
- Outputs: boolean decision and source metadata (env override, org override, global default, fallback).
- No mutation of context or storage during evaluation.

## Audit and Logging Guidance
- Emit debug-level logs for evaluations with fields: key, value, source, org_id presence flag, org_id suffix (last 6 chars only), env.
- Do not log secrets or full identifiers; prefer suffix logging when identifiers are needed.
- Align log formatting with Phase 2 Step 14 observability guidance.

## Forbidden Patterns
- Bypassing RBAC or authentication through flags.
- Changing organization ownership boundaries with flags.
- Hiding or altering business rules instead of performing explicit migrations.
- Branching database schemas behind flags.

## Storage Strategy (Phase 2 Scaffold)
- Environment variables with the `FEATURE_` prefix parsed into normalized boolean flags.
- In-memory map for global defaults and hardcoded fallback values.
- Optional organization overrides loaded from a local configuration file (example committed to the repo); no database-backed storage yet.

## Test Strategy
- Unit tests covering precedence ordering, environment parsing, key normalization, and decision source enumeration.
- Tests run without external services (no database or Redis requirement).

## Future Extensions
- Database-backed flag storage with audit history.
- Admin UI for controlled flag changes with RBAC enforcement.
- Remote provider integration guarded by security and privacy constraints (not implemented in this step).
