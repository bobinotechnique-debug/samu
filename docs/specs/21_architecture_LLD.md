# Phase 2 - Step 02: Low Level Architecture (LLD)

## Purpose and Inputs
- Lock the internal structure for backend services so implementation can proceed without redefining boundaries.
- Roadmap linkage: docs/roadmap/phase2/step-02-low-level-architecture.md.
- Depends on: docs/specs/20_architecture_HLD.md, docs/specs/04_architecture_principles.md, docs/specs/06_known_failure_patterns.md, and Phase 1 contracts (errors, identifiers, time, RBAC, audit).

## Scope and Non-Goals
- **In scope:** package layout per service, dependency direction, layer contracts (api/service/domain/infra), cross-cutting package rules, repository and schema boundaries, async job boundary.
- **Out of scope:** endpoint definitions, database DDL/migrations, queue wiring, vendor selection changes, UI updates, and any business logic implementation.

## Authoritative Backend Layout
```
backend/
  app/
    main.py
    core/
      config.py
      logging.py
      errors.py
      time.py
      ids.py
      security/
        auth.py
        rbac.py
        permissions.py
      audit/
        model.py
        sink.py
        middleware.py
      db/
        session.py
        base.py
        uow.py
      messaging/
        outbox.py
        publisher.py
      observability/
        metrics.py
        tracing.py
    api/
      deps.py
      v1/
        router.py
        health.py
        orgs.py
        projects.py
        collaborators.py
        planning.py
        finance.py
        notifications.py
    modules/
      orgs/
      projects/
      collaborators/
      planning/
      finance/
      notifications/
    tests/
      unit/
      integration/
```
- `core/*` is shared and stable; it cannot import from `api/`, `modules/`, or `infra` inside modules.
- `modules/*` contains bounded contexts; each follows the layering model below.
- `api/*` exposes FastAPI routers and request/response schemas that map to module service handlers only.

## Layering Model and Allowed Imports
- Layers (top to bottom): **api -> service -> domain -> infra**.
- Direction: imports may only point downward; interfaces flow upward.
- Allowed import matrix:
  - `api` may import `service` DTOs/handlers and `core.security`/`core.audit` helpers through `api/deps.py`.
  - `service` may import `domain`, `ports`, `core/*` (ids, time, errors, audit, rbac), and UoW interfaces from `core/db/uow.py`.
  - `domain` may import only `core/ids.py`, `core/time.py`, and `core/errors.py`; it never imports infra or api.
  - `infra` implements `ports` using SQLAlchemy or external SDKs; it may import `domain` types for mapping and `core/db` utilities.
- Forbidden:
  - No `api` -> `infra` imports; data access must pass through service layer and UoW.
  - No `domain` -> `api` or `domain` -> `infra` imports.
  - No cross-module domain imports except typed IDs and shared kernel types.
  - No `datetime.now()` or UUID generation outside `core/time.py` and `core/ids.py`.

## Cross-Cutting Packages
- **core/errors.py**: canonical exceptions; domain and service raise typed errors only. Forbidden to import FastAPI or SQLAlchemy.
- **core/ids.py**: typed identifiers (OrgId, ProjectId, etc.) with constructor validation. Forbidden to import infrastructure packages.
- **core/time.py**: UTC helpers and clock abstraction injected into services/domain. Forbidden to call `datetime.now()` directly in modules.
- **core/security/auth.py**: token parsing and principal extraction for API deps; forbidden in domain.
- **core/security/rbac.py & permissions.py**: permission constants and check helpers used in `api/deps.py` and service handlers; domain trusts pre-authorization.
- **core/audit/**: audit event model, middleware hooks, and sinks. Service emits audit events; infra persists via outbox or sink.
- **core/db/**: SQLAlchemy session factory, declarative base, and UnitOfWork protocol. Only service/infra layers may import.
- **core/messaging/**: outbox record and publisher interface. Service enqueues events; infra publisher reads and dispatches.
- **core/observability/**: metrics and tracing helpers usable by api/service/infra; domain should remain unaware.

## Per-Module Structure and Rules
Each module under `backend/app/modules/<module>/` follows the same internal layout:
```
__init__.py
api/          (optional, module-local routers if not using global api/v1)
  router.py
  schemas.py
service/
  commands.py (input DTOs)
  queries.py  (input DTOs)
  handlers.py (application services: orchestrate UoW, RBAC, audit, ports)
domain/
  entities.py
  value_objects.py
  policies.py
  events.py
  errors.py
ports/
  repositories.py (interfaces used by services)
  external.py     (interfaces to other services/providers)
infra/
  repositories.py (SQLAlchemy implementations)
  orm_models.py
  mappers.py
  adapters.py     (external API adapters, channel clients)
```
Public API surface is restricted to `api/v1/*.py` (or module `api/router.py`) calling into `service/handlers.py` methods.

### Orgs
- **Owned entities:** Organization, OrgSettings, OrgRole, FeatureFlag.
- **Purpose:** tenant boundary and org-scoped feature flags.
- **Public API surface:** `api/v1/orgs.py` delegates to `modules/orgs/service/handlers.py` commands/queries.
- **Ports:** `OrgRepository` for CRUD; optional `FeatureFlagRepository`.
- **Forbidden imports:** org domain must not import projects/planning domains; infra cannot import api.
- **Dependencies allowed:** service may validate org IDs for other modules via ports exposed here.

### Projects
- **Owned entities:** Project, Site, ProjectMember.
- **Public API surface:** `api/v1/projects.py` -> `modules/projects/service/handlers.py`.
- **Ports:** `ProjectRepository`, `SiteRepository`, `ProjectMemberRepository`.
- **Forbidden imports:** no direct planner or collaborator domain usage; use typed IDs only.
- **Notes:** service enforces org and project scoping before delegating to planning or finance ports.

### Collaborators
- **Owned entities:** Collaborator, Skill, AvailabilityWindow, Profile.
- **Public API surface:** `api/v1/collaborators.py` -> `modules/collaborators/service/handlers.py`.
- **Ports:** `CollaboratorRepository`, `AvailabilityRepository`.
- **Forbidden imports:** no project/planning domain imports; validations on membership occur in service via project/org ports.

### Planning
- **Owned entities:** ShiftTemplate, ShiftInstance, Assignment, PlanningRule, Conflict.
- **Public API surface:** `api/v1/planning.py` -> `modules/planning/service/handlers.py`.
- **Ports:** `ShiftTemplateRepository`, `ShiftInstanceRepository`, `AssignmentRepository`, `RuleRepository`; optional `PlanningReadModel` for projections.
- **Forbidden imports:** cannot import collaborator/project domain directly; service requests collaborator or project validation via ports to those modules.
- **Notes:** domain contains conflict detection policies; infra maps to SQLAlchemy tables; async notifications triggered via outbox from service.

### Finance
- **Owned entities:** Budget, CostItem (future), RateCard (future read model).
- **Public API surface:** `api/v1/finance.py` -> `modules/finance/service/handlers.py`.
- **Ports:** `BudgetRepository`; adapters for export generation are defined in `ports/external.py`.
- **Forbidden imports:** cannot depend on planning internals; only typed IDs for org/project references.

### Notifications
- **Owned entities:** NotificationTemplate, DeliveryAttempt, ChannelEndpoint.
- **Public API surface:** `api/v1/notifications.py` -> `modules/notifications/service/handlers.py`.
- **Ports:** `NotificationRepository` (persistence), `ChannelAdapter` (email/sms/etc.), `DeliveryTracker` (status updates).
- **Forbidden imports:** no domain dependencies on planning/finance; adapters encapsulate provider SDKs.
- **Notes:** service consumes outbox events or direct commands; delivery idempotency handled in service using `core/time` and `core/ids`.

## Data Access and Schema Boundaries
- **Request/response schemas:** Pydantic models live in `api/v1/*` (or module `api/schemas.py`) and map to command/query DTOs. They never expose ORM types.
- **Domain models:** Defined in `domain/*.py` with typed IDs and explicit timestamps passed in; no direct DB calls.
- **Repositories:** Ports under `ports/repositories.py` return domain entities or value objects. Infra implementations use SQLAlchemy models in `infra/orm_models.py` and mapping helpers.
- **Unit of Work:** `core/db/uow.py` defines context manager/async protocols. Services open one UoW per request or job, call repositories, and commit or rollback.
- **Transactions:** API layer obtains a UoW via `api/deps.py`; async jobs also create their own scope.

## Async Jobs Boundary
- Service layer is responsible for enqueuing domain events into `core/messaging/outbox.py` records.
- Infra publisher (`core/messaging/publisher.py`) reads outbox and dispatches to providers (e.g., notification channels); domain never publishes directly.
- Job handlers live under `backend/app/worker/` (future) and call service handlers with the same ports and UoW contracts as HTTP paths.
- Idempotency keys stored in Redis or database are managed by service/infra; API does not bypass this layer.

## Inter-Module Communication Rules
- Preferred sync path: service-to-service ports defined in `modules/<module>/ports/external.py` and implemented via adapters in `infra/adapters.py` or API clients.
- Preferred async path: domain events converted to outbox messages consumed by notification or finance jobs.
- No ORM objects cross module boundaries; only typed IDs, primitives, or DTOs defined in ports.
- Any cross-context validation occurs in the calling service using provided ports, never by sharing repositories directly.

## Guardrails and Testability
- Future import guards must enforce layering (api->service->domain->infra) and block SQLAlchemy usage outside `infra/` and `core/db`.
- Domain code must not call `datetime` or UUID constructors directly; rely on `core/time.py` and `core/ids.py` passed from service.
- Public entrypoints for behavior are limited to `api/v1/*.py` and `modules/*/service/handlers.py`; tests target service handlers and domain policies in isolation.
