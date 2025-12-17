# Frontend Architecture

## Purpose
Define the frontend technical architecture for Phase 2, ensuring the UI remains free of business logic while consuming Phase 1 API and UX contracts.

## App Shell
- Single-page application built with React + Vite + TailwindCSS; routing handled by a top-level router with guarded layouts.
- Layout includes organization/project selectors that drive scoped API requests; selection state persisted in client storage with validation against tokens.

## State Management
- Query client (e.g., React Query) for server state with cache keys incorporating organization_id and project_id.
- Lightweight global store for UI preferences (theme, density) and routing parameters; no derived business rules.
- Derived view models computed from API responses in modules, not in shared components.

## Data Fetching
- API client wraps fetch/axios with automatic inclusion of tokens and correlation_id headers.
- Pagination helpers align with docs/api/20_api_architecture.md conventions (cursor-first, `has_more`).
- Error handling maps server envelopes to user-safe messages; unauthorized responses trigger re-auth flows without guessing permissions.

## Module Structure
- Feature modules per domain context (projects, missions, assignments, collaborators) containing hooks, API clients, and view models.
- Components remain stateless, receiving formatted data and callbacks only; no direct API calls inside presentational components.
- Cross-cutting utilities (telemetry, feature flags) live in services/ and cannot import module-specific logic.

## Testing and Tooling
- Story-driven component testing using mock data that honors Phase 1 visual language and component contracts.
- Integration tests stub API responses to validate routing and state wiring without exercising business rules.

## Alignment with Phase 1
- Uses UI component and page contracts from docs/specs/15_ui_component_contracts.md and docs/specs/16_ui_page_contracts.md.
- Follows API conventions and versioning from docs/specs/10_api_conventions.md and docs/specs/12_api_versioning.md.
- Preserves ownership boundaries by requiring organization_id/project_id in all data calls; no cross-tenant caching.
