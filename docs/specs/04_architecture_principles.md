# Architecture Principles

## Purpose
Establish authoritative architecture rules that constrain design, implementation, and documentation across all agents to prevent ambiguity and drift.

## Scope
- Applies to backend, frontend, docs, and ops activities in all phases.
- Governs planning, domain modeling, and cross-agent collaboration.
- Enforceable during design reviews, code changes, and documentation updates.

## Principles
1. **Single Source of Truth Rule**
   - Rule: AGENT.md and the most recent roadmap step are the only authoritative sources for scope and precedence; any document or code conflicting with them is invalid until reconciled.
   - Test: Every change references the active roadmap step and defers to AGENT.md on conflicts.

2. **Separation of Concerns (Domain, Application, Infra)**
   - Rule: Domain policies live in backend domain modules and specs; application orchestration stays in services; infrastructure concerns remain in ops scripts. Cross-layer leakage is forbidden.
   - Test: No domain rule is implemented or documented in frontend or infra scopes; ops scripts do not embed business rules.

3. **No Planning Without Project**
   - Rule: All planning artifacts, assignments, and missions must reference a project identifier; standalone planning records are invalid.
   - Test: Any plan, mission, or assignment spec lacking a project reference fails review.

4. **No Cross-Organization Data Access**
   - Rule: Data access is scoped to a single organization; cross-organization queries, joins, or UI aggregations are forbidden.
   - Test: All data flows require an organization_id input and validation; multi-organization aggregation attempts are rejected.

5. **Backend Authoritative, Frontend Stateless**
   - Rule: Backend owns business logic, validation, and state; frontend holds transient view state only and may not embed business rules or persistence logic.
   - Test: Business decisions documented or coded in the frontend are blocked; backend exposes validated APIs for all stateful operations.

6. **Deterministic Behavior Over Convenience**
   - Rule: Architectures favor deterministic outcomes; non-deterministic shortcuts (implicit defaults, time-based randomness, hidden retries) are prohibited without explicit specification and logging.
   - Test: Each workflow defines deterministic inputs and outputs; any randomness or retry strategy is specified, logged, and bounded.

## Enforcement
- Violations must be logged as agent errors and blocked until resolved.
- Reviews must check alignment with these principles before accepting documentation or code.
