# API Architecture and Routing (Phase 2)

Status: Starting
Owner: Codex (docs)
Last updated: 2025-12-17
Scope: Phase 2 Step 04 (API wiring and routing scaffolds)

This document defines how FastAPI is wired in practice: route groups, versioning, shared dependencies, error mapping, and pagination rules.
It MUST match Phase 1 API contracts and baselines:
- docs/specs/10_api_conventions.md
- docs/specs/11_api_error_model.md
- docs/specs/12_api_versioning.md
- docs/specs/20_architecture_HLD.md

No business logic is defined here. Only routing, composition, and cross-cutting conventions.

---

## 1. Goals

- Provide a stable, explicit routing tree with route groups aligned to service boundaries (HLD).
- Enforce versioning rules in the actual router layout (no ad-hoc prefixes).
- Centralize error mapping so domain/service exceptions become the Phase 1 error model.
- Standardize pagination (request params + response envelope) consistently across endpoints.
- Ensure organization and project isolation is enforceable via dependencies.

Non-goals:
- Implementing endpoints behavior.
- Implementing DB persistence.
- Implementing auth providers (only stubs/contracts).

---

## 2. FastAPI composition

### 2.1 App entrypoint

Recommended structure (illustrative):

- backend/app/main.py
- backend/app/api/__init__.py
- backend/app/api/v1/router.py
- backend/app/api/v1/routes/*.py
- backend/app/api/deps.py
- backend/app/api/errors.py
- backend/app/api/pagination.py

App wiring responsibilities:
- Create FastAPI app
- Attach middleware (request id, auth context, logging)
- Register exception handlers (Phase 1 error model)
- Include the versioned API router

Pseudo-layout:

- app = FastAPI(...)
- app.include_router(api_v1_router, prefix="/api/v1")
- register_exception_handlers(app)

Important:
- Only one place defines "/api/v1" prefix.
- Internal routers MUST NOT hardcode "/api/v1" again.

### 2.2 Router pattern

- One top-level version router per API version.
- Route groups as sub-routers included in the version router.
- Each route file owns exactly one APIRouter and is included once.

Naming:
- router module: backend/app/api/v1/routes/<group>.py
- router variable: router

Tags:
- Each router sets tags=[...] for OpenAPI grouping.
- Tags MUST match route group name.

---

## 3. Route groups (aligned to HLD boundaries)

This is the Phase 2 scaffolding target. Exact endpoint lists remain defined in Phase 1 API docs.
Groups below are logical boundaries and should map to HLD services/modules.

### 3.1 Core platform

Prefix: /api/v1

- /health
- /meta
- /auth (if any API-level auth endpoints exist)
- /orgs
- /projects

### 3.2 Planning domain

- /planning
  - /planning/templates
  - /planning/instances
  - /planning/assignments
  - /planning/conflicts
  - /planning/publications

### 3.3 People and resources

- /collaborators
- /roles
- /skills
- /sites

### 3.4 Audit and ops

- /audit
- /admin (only if Phase 1 defines it, keep guarded)

Notes:
- Keep groups coarse. Do not fragment routes by tiny sub-domains.
- Each group should have a single "routes/<group>.py" router entry.

---

## 4. Versioning approach (in practice)

Baseline authority: docs/specs/12_api_versioning.md

Rules:
- All public endpoints live under /api/v{N}/...
- No unversioned endpoints, except /health if explicitly allowed by Phase 1.
- Version routers are explicit modules:
  - backend/app/api/v1/router.py
  - (future) backend/app/api/v2/router.py

Deprecation:
- Deprecation is signaled via:
  - OpenAPI metadata (deprecated=True where applicable)
  - Response headers (only if Phase 1 defines a convention)
- Removing endpoints requires a new major version.

---

## 5. Cross-cutting request context dependencies

### 5.1 Request id

Every request MUST have a request id available in logs and error responses.
Source:
- Prefer inbound header "X-Request-Id" if present
- Otherwise generate UUID4

Expose it in:
- response header "X-Request-Id"
- error payload "request_id" (if Phase 1 error model includes it)

### 5.2 Authentication and actor

An "actor context" dependency provides:
- actor_id
- actor_type (user/service)
- org_id (required for tenant isolation)
- roles/scopes (RBAC)

Contract:
- No endpoint with tenant data can run without org_id in context.
- Actor context resolution is done in deps.py and MUST be usable by all routers.

### 5.3 Organization boundary (tenant isolation)

All org-scoped endpoints MUST enforce an org boundary.
Two acceptable patterns (choose one and keep consistent with Phase 1):

Pattern A (path-scoped org):
- /orgs/{org_id}/projects
- deps: require_org_path(org_id) validates membership and sets context

Pattern B (header-scoped org):
- /projects
- require header "X-Org-Id"
- deps: require_org_header() validates and sets context

If Phase 1 already locked this choice, Phase 2 MUST implement that choice only.

### 5.4 Project boundary (functional isolation)

All project-scoped endpoints MUST enforce project belongs to org.
Dependency:
- require_project(project_id) validates:
  - project exists
  - project.org_id == actor.org_id
  - actor has access to project (RBAC)

---

## 6. Error mapping (Phase 1 error model)

Baseline authority: docs/specs/11_api_error_model.md

### 6.1 Principles

- Domain/service code raises typed exceptions.
- API layer catches them and returns the canonical error response.
- No raw tracebacks or unstructured errors leave the API.
- For unexpected exceptions, return a stable INTERNAL error code.

### 6.2 Canonical mapping table (example scaffold)

This table is the wiring contract; the exact codes/fields must match Phase 1.

- ValidationError -> 422 UNPROCESSABLE_ENTITY
  - code: "validation_error"
- NotFoundError -> 404 NOT_FOUND
  - code: "not_found"
- ConflictError -> 409 CONFLICT
  - code: "conflict"
- ForbiddenError -> 403 FORBIDDEN
  - code: "forbidden"
- UnauthorizedError -> 401 UNAUTHORIZED
  - code: "unauthorized"
- RateLimitError -> 429 TOO_MANY_REQUESTS
  - code: "rate_limited"
- DomainInvariantError -> 400 BAD_REQUEST (or 409 if specified)
  - code: "domain_invariant"
- InternalError / Exception -> 500 INTERNAL_SERVER_ERROR
  - code: "internal"

### 6.3 Error response shape

The error response MUST match Phase 1. This doc only requires:
- stable "code"
- stable "message" (safe for display)
- optional "details" (structured)
- request correlation (request_id)

Additionally:
- Include a machine-friendly "error_id" if Phase 1 requires it.
- Never leak secrets, stack traces, SQL, or tokens.

### 6.4 Implementation wiring

- Define exception classes in a shared module (domain or service layer).
- Define FastAPI exception handlers in backend/app/api/errors.py.
- Register handlers in app startup (main.py).

Rule:
- Routers MUST NOT implement per-endpoint try/except for these cases.
- Exception handlers are the single source of mapping.

---

## 7. Pagination rules

Baseline authority: docs/specs/10_api_conventions.md

This section defines how pagination is expressed in request params and response payloads.
Use ONE style consistently per Phase 1 baseline.

### 7.1 Supported pagination styles

Option A: Cursor pagination (preferred for large datasets)
Request:
- limit: int (default and max defined by Phase 1)
- cursor: string (opaque)

Response:
- items: [...]
- page:
  - next_cursor: string | null
  - limit: int
  - has_more: bool

Option B: Offset pagination (only if Phase 1 locked it)
Request:
- limit: int
- offset: int

Response:
- items: [...]
- page:
  - offset: int
  - limit: int
  - total: int (only if Phase 1 requires total, otherwise omit)

### 7.2 Sorting and filtering

If endpoints support sorting/filtering:
- sort: comma-separated fields with optional prefix "-" for desc
- filters are explicit query params (no free-form query language unless Phase 1 defines it)

Rules:
- If sort/filter is not supported, endpoint MUST reject unknown query params only if Phase 1 requires strictness.
- Do not implement "q=" search unless Phase 1 defines it.

### 7.3 Pagination defaults and limits

- Default limit MUST be stable and documented (Phase 1).
- Max limit MUST be enforced (reject or clamp as defined in Phase 1).

---

## 8. Response envelopes and consistency

This document does not redefine schemas; it defines consistency rules.

Rules:
- For list endpoints, use the list envelope defined by Phase 1 (typically items + page).
- For single resources, return the resource schema (no wrapping) unless Phase 1 wraps.
- For create endpoints, return the created resource or a minimal acknowledgement as defined by Phase 1.
- For delete endpoints, return 204 No Content unless Phase 1 specifies otherwise.

---

## 9. OpenAPI and tagging

Rules:
- Each route group MUST set tags=[...] for docs clarity.
- Operation ids should be stable. If Phase 1 defines naming, follow it.
- Deprecations must be expressed using OpenAPI "deprecated" when applicable.
- Examples in OpenAPI must not include secrets.

---

## 10. CORS, security headers, and middleware (scaffold)

Middleware list (scaffold only):
- request id propagation
- auth/actor context extraction (or dependency-only, but keep consistent)
- structured logging
- optional: gzip

Security headers (if Phase 1 or ops docs require):
- strict transport security (when behind TLS)
- x-content-type-options
- x-frame-options / CSP (if relevant)

CORS:
- Disabled by default in production.
- Explicit allowlist for dev front-end origins.

---

## 11. Reference router skeleton (illustrative)

This is a conceptual example to guide implementation and does not lock endpoint lists.

- api/v1/router.py includes:
  - health router
  - orgs router
  - projects router
  - planning router
  - collaborators router
  - audit router

Each route module:
- defines router = APIRouter(prefix="/<group>", tags=["<group>"])
- attaches dependencies at router level when possible:
  - dependencies=[Depends(require_actor), Depends(require_org_context)]

---

## 12. Acceptance checklist (Phase 2 Step 04)

- docs/api/20_api_architecture.md created and registered in docs/api/INDEX.md
- Routing tree and groups aligned with docs/specs/20_architecture_HLD.md
- Versioning approach matches docs/specs/12_api_versioning.md
- Error mapping wiring matches docs/specs/11_api_error_model.md
- Pagination rules match docs/specs/10_api_conventions.md
- Tenant isolation enforcement is described (org + project boundary dependencies)
- ASCII-only content (no accents, no emojis)

---
