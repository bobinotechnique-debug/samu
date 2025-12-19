# Execution Governance and Invariants

## 1. Purpose and Non-Goals
- Document enforceable execution governance rules and invariants that prevent drift during Phase 3+ implementation.
- Define where each invariant is enforced (API, services, repositories, database, async workers) and how violations surface.
- Align enforcement with Phase 1 contracts (multi-tenancy, RBAC, audit, error model, API conventions, identifiers/time).
- Non-goals: introduce new business logic, change schemas, add dependencies, or implement endpoints.

## 2. Definitions
- **Organization boundary:** Hard security boundary; no data or execution crosses `org_id`.
- **Project boundary:** Functional planning boundary; missions and assignments live inside a project and its `org_id`.
- **Mission:** Execution unit within a project; aggregates assignments and run sheets.
- **Assignment:** Work item belonging to a mission; scoped by `org_id`, `project_id`, and `mission_id`.
- **Actor:** User, system process, or API key performing an action; always resolved with `org_id` context.
- **System:** The SaaS platform components (API, services, workers, storage) operating under the above boundaries.

## 3. Global Invariants (Authoritative)
1. **Org isolation:** No read/write crosses `org_id`; every query and mutation must filter by `org_id`.
2. **Project scoping:** Projects belong to one `org_id`; missions and assignments must include matching `project_id` and `org_id`.
3. **Mission existence:** Missions cannot exist without a parent project; references must validate project presence and `org_id` alignment.
4. **Assignment existence:** Assignments cannot exist without a mission; references must validate mission and project ownership.
5. **Audit coverage:** Every mutating action emits an audit event using the Phase 1 audit envelope (actor, request_id, timestamps, entity refs).
6. **UTC and ordering:** All timestamps stored in UTC; interval fields validate `start_at < end_at` when both present; identifiers remain opaque and stable.
7. **Read purity:** GET/READ operations produce no writes, side effects, or async dispatches.
8. **Idempotent jobs:** Async handlers are idempotent within `org_id` (and `project_id` when present) using stable idempotency keys.
9. **Versioned APIs:** Public routes must declare API version per Phase 1 conventions; breaking changes require new versions.
10. **Error contract:** Errors follow the Phase 1 error model (code/message/details) with stable codes and correlation ids.

## 4. Local Invariants by Area
### Projects, Missions, Assignments
- Projects: unique per `org_id` by name and slug; soft-delete must retain uniqueness constraints within `org_id`.
- Missions: must reference an active project in the same `org_id`; status transitions must be valid per mission lifecycle; scheduling windows must be inside project active window when defined.
- Assignments: must reference an active mission; assignee must belong to the same `org_id`; availability conflicts cannot be auto-resolved without policy approval; quantity/time units must align with mission units.

### Collaborators, Skills, Availability
- Collaborators belong to exactly one `org_id`; cross-org membership is forbidden.
- Skills are namespaced to `org_id`; lookups must filter by `org_id` and normalized name.
- Availability windows must not overlap per collaborator and must validate `start_at < end_at`.

### Files and Documents (Mission Run Sheet attachments)
- Files inherit `org_id` and `project_id`; storage paths and access tokens must be scoped by `org_id`.
- Attachments cannot be linked to missions outside their `project_id` or `org_id`.
- Checksums and content-type metadata are required for mutating file operations.

### Notifications
- Notification templates are scoped by `org_id`; dispatch must validate audience membership in `org_id`.
- Notification jobs must be idempotent per (`org_id`, recipient, template, payload_hash, schedule_bucket`).
- Notification delivery is best-effort unless explicitly marked critical; failures must not mutate domain state.

## 5. Enforcement Matrix
| Invariant | Layer | Mechanism | Error code | Audit requirement | Test type |
| --- | --- | --- | --- | --- | --- |
| Org isolation on all queries | Repository, DB | Required `org_id` filter; DB partial indexes by `org_id` | 403 for cross-org access attempt | Audit attempt with actor and target ids | Unit (repository), integration (API) |
| Project scoping for missions | Service, DB | Service guard validates project ownership; FK `mission.project_id -> project.id` with `org_id` check | 422 when project missing/mismatched | Audit mutation request | Unit (service), migration/DB tests |
| Assignment requires mission | Service, DB | Service guard; FK with `ON DELETE RESTRICT`; mission status check | 409 for status violation; 422 for missing mission | Audit mutation request | Unit (service), integration |
| Audit on mutations | API, Service | Audit dispatcher invoked before commit; retries on failure with dead letter | 500 if audit sink unavailable and operation cannot be confirmed | Audit event stored with request_id | Unit (audit helper), integration (API) |
| UTC and interval ordering | Service, Validation layer | Validation schema enforcing UTC and `start_at < end_at` | 422 | Audit rejection with validation reason | Unit (validators) |
| Read purity | API | Route guards reject writes in GET handlers; workers only for async routes | 500 if violation detected | Audit anomaly event | Static check, integration |
| Idempotent jobs | Async worker | Idempotency key enforcement and dedup store per `org_id` | 409 for duplicate conflicting payload | Audit job attempt and result | Unit (worker), chaos/retry tests |
| Versioned APIs | API routing | Versioned path prefix and backward-compatible schema | 404 for missing version | Audit request | Unit (routing), contract tests |

## 6. Failure Semantics
- **403:** Authorization failure, cross-org access, or forbidden scope escalation.
- **404:** Resource not found within the caller `org_id` and `project_id` scope.
- **409:** Conflict on state transitions, duplicate idempotency key with different payload, or mission/assignment status violations.
- **422:** Validation errors (missing parent references, invalid time ordering, malformed payloads).
- **Degrade vs reject:** Degrade only for non-critical secondary effects (notifications, analytics enrichment). Reject for ownership, audit, idempotency, or scope violations.

## 7. Forbidden Patterns
- Cross-organization queries or joins, including implicit reads without `org_id` filters.
- Service calls that bypass repositories or issue raw SQL without scope guards.
- Business logic in the frontend that bypasses server-side validation or RBAC.
- Implicit writes inside read paths, including cache warming that mutates state without audit.
- Async jobs that mutate domain state without idempotency keys and audit events.

## 8. ADR-lite Rule for Changes
- Any change to invariants requires an ADR-lite entry at `docs/adr/NNN-title.md` with context, decision, consequences, and affected enforcement points.
- ADR-lite must link to the roadmap step driving the change and reference impacted specs.
- No implementation may proceed until the ADR-lite is merged and indexed.

## 9. Codex Stop Conditions (Phase 3+)
- Required spec or ADR-lite for an invariant is missing or outdated -> STOP.
- Invariant cannot be enforced at the declared layer (missing guard, constraint, or test) -> STOP.
- Guard scripts, CI, or enforcement tests fail -> STOP.
- Detected cross-org access, unaudited mutation, or non-idempotent job behavior -> STOP until remediated.
