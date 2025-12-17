# Low Level Architecture (LLD)

## Purpose
Detail per-service internal structure, package layout, and dependency rules that extend the High Level Architecture without introducing business behavior.

## Package Layout (Backend)
- **api/**: FastAPI routers grouped by domain context; imports only application/service layer interfaces.
- **application/**: Use-case coordinators orchestrating domain services, validation, and audit logging; no direct database access.
- **domain/**: Entities, value objects, and domain services enforcing invariants from docs/specs/05_domain_contracts.md.
- **infrastructure/**: Adapters for PostgreSQL repositories (SQLAlchemy), Redis queues, logging, and external integrations; implements interfaces defined in application/domain layers.
- **worker/**: Job handlers consuming queue messages; reuse application and domain services through dependency injection.

## Package Layout (Frontend)
- **app/**: Shell, routing, and layout wrappers aligned to docs/ux/20_frontend_architecture.md.
- **modules/**: Feature slices keyed by domain contexts (project, mission, collaborator) with API clients, state stores, and view models.
- **components/**: Presentational components mapped to Phase 1 UI contracts; no data fetching.
- **services/**: API client wrappers and cross-cutting utilities (telemetry, feature flags) restricted to pure functions.
- **state/**: Centralized state configuration (e.g., query client, store), keeping ownership context (organization_id, project_id) explicit.

## Dependency Rules
- **Layering:** api -> application -> domain -> infrastructure (implementations) with interfaces flowing inward; no reverse imports.
- **Cross-context access:** Modules may read other contexts only through public application interfaces; no direct repository cross-calls to avoid hidden coupling.
- **Shared utilities:** Common helpers live in a dedicated shared/ directory but cannot import application/domain code.
- **Testability:** Interfaces defined in domain/application enable worker and API layers to share behaviors without duplication.

## Layering Guardrails
- No circular dependencies across packages; enforce via import checks and directory layout.
- Infrastructure code must not contain business rules; validation stays in domain/application layers.
- Frontend modules must not embed authorization or ownership shortcuts; they surface errors from the API and rely on tokens.

## Alignment with Phase 1
- Respects architecture principles (docs/specs/04_architecture_principles.md) and failure patterns (docs/specs/06_known_failure_patterns.md).
- Preserves ownership and RBAC enforcement points defined in docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md by keeping authorization in application/domain layers.
- Keeps audit contracts (docs/specs/09_audit_and_traceability.md) centralized in application orchestration rather than UI.
