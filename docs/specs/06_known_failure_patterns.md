# Known Failure Patterns

## Purpose
Document recurring errors and architectural drifts with detection and prevention rules to keep CI green and architecture consistent.

## Scope
- Applies to all agents and documentation owners.
- Enforced during reviews, roadmap execution, and guardrail checks.
- Covers agent errors, architectural drifts, forbidden shortcuts, and deceptive "looks OK but is wrong" cases.

## Failure Patterns

### Planning Without Project Anchor
- Description: Missions or plans documented or proposed without an explicit project_id.
- Root Cause: Ignoring the project-centric rule or assuming default project context.
- Detection Method: Review specifications and payloads for missing project_id; block any plan lacking project linkage.
- Prevention Rule: Reject any planning artifact unless it references a valid project_id tied to an organization_id.

### Cross-Organization Data Mixing
- Description: Data flows or reports that combine records from multiple organizations in a single request or view.
- Root Cause: Convenience queries or analytics shortcuts that bypass tenancy boundaries.
- Detection Method: Trace data access patterns for joins or filters missing organization_id; audit API designs for aggregation across tenants.
- Prevention Rule: Enforce organization_id as mandatory in every query, API, and UI filter; block multi-organization aggregation.

### Frontend-Embedded Business Logic
- Description: Business decisions or validations implemented in the frontend instead of the backend.
- Root Cause: Convenience-driven UI logic intended to speed delivery without backend alignment.
- Detection Method: Review UI documentation and code for role checks, policy enforcement, or data shaping not backed by backend APIs.
- Prevention Rule: Require backend-owned APIs to provide validated decisions; keep frontend stateless beyond presentation state.

### Single Source Drift
- Description: Documentation or code diverges from AGENT.md or the active roadmap step.
- Root Cause: Updating artifacts without referencing authoritative sources or missing index updates.
- Detection Method: Cross-check every change for roadmap linkage and AGENT.md alignment; verify index entries are updated.
- Prevention Rule: Block merges without roadmap reference, index updates, and AGENT.md consistency confirmation.

### Hidden Non-Determinism
- Description: Implicit defaults, time-dependent behaviors, or undocumented retries that make outcomes unpredictable.
- Root Cause: Prioritizing convenience over explicit deterministic rules.
- Detection Method: Inspect workflows for implicit randomness, current-time dependencies, or silent retries lacking bounds.
- Prevention Rule: Specify deterministic inputs/outputs; document and bound any randomness or retry strategies with logging hooks.
