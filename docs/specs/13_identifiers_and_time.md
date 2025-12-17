# Identifier and Time Conventions

## Purpose
Standardize identifier formats and time handling to enforce consistency, prevent information leakage, and guarantee reliable ordering and traceability.

## Scope
- Applies to all identifiers and timestamps exposed or consumed by APIs under /api/v1/.
- Covers ID format decisions, generation rules, timezone constraints, and serialization formats.
- Binding for backend persistence, API responses, and frontend consumption in future phases.

## Assumptions
- Organization is the security boundary and project is the planning boundary; identifiers MUST encode neither.
- Server-side components control authoritative identifiers; clients may provide correlation identifiers only for idempotency.
- Phase 1 remains documentation-only; implementation will enforce these rules later.

## Exclusions
- Database primary key implementation details beyond format and opacity requirements.
- Client-side display formatting preferences (e.g., relative time rendering) beyond the mandated source format.
- Clock synchronization mechanisms; only conventions are defined here.

## Identifier Rules
- Resource identifiers MUST be opaque, non-semantic strings; no embedded meaning, timestamps, or counters are allowed.
- UUIDv4 (lowercase, canonical 8-4-4-4-12 hex) MUST be used for public-facing resource identifiers unless a future roadmap step approves an alternative.
- Authoritative identifiers MUST be generated server-side; clients MUST NOT generate canonical resource IDs.
- Identifiers MUST remain stable for the lifetime of the resource and MUST NOT be recycled after deletion.
- Public identifiers MUST NOT expose internal database keys or sequencing patterns.

## Timezone and Timestamp Rules
- All timestamps MUST be recorded and returned in UTC; local timezones are forbidden.
- Timestamps MUST be serialized using ISO 8601 with a trailing Z (e.g., 2025-01-01T00:00:00Z); offsets other than Z MUST NOT be used in API responses.
- Clients MUST treat timestamps as immutable audit data and MUST NOT reinterpret them into different timezones before validation.
- Server clocks MUST be synchronized to UTC; skew handling rules MUST be documented in future implementation steps if required.

## Forbidden Patterns
- Client-generated authoritative identifiers for persistent resources are forbidden.
- Sequential or guessable identifiers (including database autoincrement values) MUST NOT be exposed publicly.
- Local time fields, timezone-less timestamps, or ambiguous date formats (e.g., MM/DD/YYYY) are forbidden in API contracts.
- Embedding semantic meaning (organization ids, project ids, roles, or timestamps) inside opaque identifiers is forbidden.
