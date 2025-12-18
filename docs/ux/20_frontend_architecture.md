# Frontend Architecture (Phase 2 Step 07)

## Purpose
Define the frontend technical architecture so that the UI stays free of business logic while consuming the locked API and UX contracts from Phase 1 (see docs/specs/10_api_conventions.md, docs/specs/12_api_versioning.md, docs/specs/15_ui_component_contracts.md, docs/specs/16_ui_page_contracts.md).

## Non-goals
- Implementing pages, features, or domain rules.
- Replacing backend validation with frontend rules.
- Creating a second source of truth for business logic.
- Introducing mock APIs for production flows.

## Core principles
1) **UI is a rendering layer**: Components render state and dispatch intents; React components must not implement domain decisions.
2) **One-way data flow**: Intent -> client-side service -> API -> normalized state -> UI.
3) **Server state lives in a dedicated cache**: Do not mirror server data into global client state.
4) **URL is a first-class state**: Filters, view ranges, and pagination live in URL/query params when possible.
5) **Strict separation of concerns**: Page = composition + routing + access checks + data orchestration. Feature adapter = input mapping + API calls + response normalization. Shared UI = reusable components that follow contracts.

## Locked stack assumptions
- React + TypeScript (Vite + TailwindCSS baseline).
- Router: React Router (or equivalent) with an explicit route tree.
- Server state: TanStack Query (React Query) or equivalent.
- Forms: React Hook Form (or equivalent).
- Validation at boundaries: Zod (or equivalent) for runtime input shaping.
- UI kit: shadcn/ui + Tailwind (per UI component contracts).
- Date handling: UTC + ISO strings consistent with API time conventions.

## Project structure (enforced layering)
```
src/
  app/
    AppShell.tsx
    routes/
      index.tsx
      planning.routes.tsx
      missions.routes.tsx
      collaborators.routes.tsx
    providers/
      QueryProvider.tsx
      AuthProvider.tsx
      ThemeProvider.tsx
  pages/
    PlanningPage/
      index.tsx
      planning.page.tsx
    MissionPage/
      index.tsx
      mission.page.tsx
  features/
    planning/
      api/
        planning.client.ts
        planning.keys.ts
      hooks/
        usePlanningGrid.ts
      mappers/
        planning.mappers.ts
      types/
        planning.types.ts
    missions/
      ...
  shared/
    api/
      http.ts
      errors.ts
      pagination.ts
      auth.ts
      versioning.ts
      org_context.ts
    components/
      DataTable/
      TimelineBar/
      AvatarStack/
      ConflictBadge/
      FilterBar/
    ui/
      (shadcn primitives wrappers if needed)
    state/
      ui_store.ts
    utils/
      dates.ts
      format.ts
      guards.ts
    constants/
      routes.ts
      query.ts
    test/
      fixtures/
      msw/ (optional, test-only)
```

Rules:
- `pages/` must not call fetch directly; use `features/*` adapters/hooks.
- `features/*` may call `shared/api/*` only.
- `shared/*` must not import from `features/*` or `pages/*`.
- No circular dependencies.

## Layering model and responsibilities
### App layer (`src/app`)
- Bootstraps providers (query client, auth context, error boundaries).
- Defines route tree and lazy loading boundaries.
- Defines global layout (app shell) and navigation scaffolding.
- **Forbidden**: Domain rules or feature-specific UI logic beyond composition.

### Pages layer (`src/pages`)
- Compose UI components per page contracts.
- Bind route params + URL state to feature hooks.
- Handle access constraints at the UI level (display-only RBAC gating).
- Provide "page view model" mapping from feature output to components.
- **Forbidden**: Backend rule re-implementation or complex server data transforms (move to feature mappers).

### Features layer (`src/features/<feature>`)
- Encapsulate API calls for a feature.
- Define query keys, request/response mapping, and normalization.
- Provide hooks to pages (`useXxx`).
- Keep parsing, mapping, and defaulting out of UI components.
- **Forbidden**: Direct DOM decisions or cross-feature imports beyond shared contracts.

### Shared layer (`src/shared`)
- API client core (HTTP wrapper, auth token injection, error mapping).
- Common UI components per UI component contracts.
- Utilities (dates, formatting, pagination helpers).
- Global UI state store (UI concerns only).
- **Forbidden**: Feature-specific logic.

## App shell and routing
### Route groups
Stable routes matching page contracts:
- `/app/planning`
- `/app/projects/:projectId/missions`
- `/app/projects/:projectId/missions/:missionId`
- `/app/collaborators`
- `/app/settings`

Each route maps to a page entry point in `src/pages/*`.

### URL state conventions
Persist to URL whenever it affects the view:
- time range (`from`, `to`)
- zoom level (`15|30|60`)
- selected `projectId` / `missionId` when not in path
- filters (`role`, `status`, `conflictOnly`, `search`)
- pagination (`page`, `pageSize`) for tables

Avoid global state for URL-friendly values.

## Data fetching and API client usage
### API versioning
All API calls target the versioned base path `/api/v1/...`; base URL and version prefix live in `shared/api/versioning.ts`.

### HTTP wrapper requirements (`shared/api/http.ts`)
- Inject auth token (Bearer).
- Inject organization context header when required by backend conventions.
- Set request id header if the API requires it.
- Enforce JSON content type conventions.
- Normalize errors into the API error model mapping (see docs/specs/11_api_error_model.md).

### Error mapping contract
Errors map to typed objects:
- `code`
- `message`
- `details` (optional)
- `trace_id` / `request_id` when present

UI responsibilities: display user-safe messages and provide trace id copy; do not guess business meaning beyond error code.

### Server state cache rules
- Use TanStack Query for all server state (queries and mutations).
- Mutations invalidate/refetch known query keys; avoid manual cache patching unless explicitly defined.
- Normalize lists where needed without building a full client-side domain model.

### Pagination and filtering
- Follow API pagination conventions from docs/specs/10_api_conventions.md.
- Feature adapters provide query keys that include filters and pagination params.
- Maintain stable mapping between URL state and API params.

## State management
### Categories
1) **Server state**: always via query cache.
2) **URL state**: React Router search params (or equivalent).
3) **Ephemeral UI state**: component local state (expanded rows, dialogs).
4) **Global UI state**: cross-cutting UI concerns (theme, toasts, drawer open, last used view mode) in `shared/state/ui_store.ts`.

**Forbidden**: storing server payloads in global state or duplicating query cache into the store.

### Form state
- Use a form library with controlled submission.
- Validate client-side for shape only (required fields, types) using Zod or equivalent.
- Backend remains authoritative for domain validation.

## UI component contracts binding
- Shared components must comply with DataTable, TimelineBar, AvatarStack, ConflictBadge, and FilterBar contracts.
- Pages must not fork these patterns; new variants require updating the component contract first.

## Enforcement hooks (lightweight)
- ESLint or import-boundary rules to prevent `pages/*` importing `shared/api/http` directly.
- No "services" inside `pages`.
- No feature importing from `pages`.
- TypeScript strict mode with `noImplicitAny`.

## Testing architecture (scaffolding only)
- Unit tests: `shared/utils`, feature mappers, error mapping functions.
- Integration tests: page renders with mocked feature hooks (test-only) and optional API contract tests using MSW in test env only.
- Production must not rely on mocks.

## Security considerations (frontend)
- Never store tokens in insecure storage without an explicit security decision.
- Prefer memory storage with refresh flow if defined by backend security model.
- Do not log sensitive data (tokens, PII) to console.
- Always pass org context as required by multi-tenancy rules.
- Backend remains authoritative for security.

## Acceptance checklist (Phase 2 Step 07)
- Document exists at `docs/ux/20_frontend_architecture.md`.
- Defines folder structure and layering rules.
- Covers routing + URL state conventions.
- Describes server state and client state patterns.
- Specifies API client usage and error mapping expectations.
- Binds to UI component and page contracts.
- Avoids business logic inside UI components.
- Aligns with Phase 1 API conventions and versioning specs.
