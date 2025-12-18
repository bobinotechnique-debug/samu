# Security and Trust Model

## Dependencies
- docs/specs/03_multi_tenancy_and_security.md
- docs/specs/07_data_ownership.md
- docs/specs/08_rbac_model.md
- docs/specs/09_audit_and_traceability.md
- docs/specs/11_api_error_model.md

## 1. Goals and Non-Goals
### 1.1 Goals
- Guarantee organization-level isolation (hard multi-tenancy boundary).
- Provide a concrete authentication model usable by FastAPI services.
- Define token contents, scopes, and enforcement hooks.
- Define how RBAC is enforced at API boundaries and inside services.
- Define how security events are logged and correlated with audit traces.
- Ensure security design is compatible with async jobs and idempotent retries.

### 1.2 Non-Goals
- Selecting a specific IdP vendor (Auth0, Cognito, Keycloak, etc.).
- Implementing cryptography primitives or custom auth protocols.
- Implementing a full SSO enterprise suite (SAML federation, SCIM) in Phase 2.
- Defining the full incident response runbook (belongs to ops).

## 2. Trust Boundaries
### 2.1 Boundaries
- Tenant boundary: Organization (org_id) is the security boundary. No cross-org reads/writes.
- Functional boundary: Project is a functional boundary, not a security boundary. Access is still org-scoped.
- Service boundary: API gateway / router layer enforces authn/authz consistently for all endpoints.

### 2.2 Assumptions
- All API calls are authenticated, except explicitly declared public endpoints (e.g., health).
- Each request resolves to an AuthContext containing:
  - subject_id (user id)
  - org_id
  - roles / permissions
  - token_id / session_id
  - auth_level (optional)
- All domain queries must be filtered by org_id by default.

## 3. Authentication Model
### 3.1 Supported Authentication Modes
Phase 2 supports two primary modes:
1. User Authentication (interactive)
   - Browser/mobile obtains a short-lived access token.
   - Optional refresh token held by frontend in a secure store.
2. Service-to-Service Authentication (non-interactive)
   - Internal jobs or services call APIs using a service token.
   - Service token is scoped to an org_id where applicable.

### 3.2 Token Types
- Access Token (JWT or opaque): short-lived (e.g., 5-15 minutes).
- Refresh Token (opaque recommended): longer-lived (e.g., 7-30 days).
- Service Token: short-lived, rotated automatically.

### 3.3 Session Model
- Sessions are represented by a server-side record (recommended) keyed by session_id.
- Access tokens map to a session via token_id or session_id.
- Session invalidation is supported (logout, password reset, suspected compromise).

## 4. Token Contents and Claims
### 4.1 Required Claims (Access Token)
- iss: issuer
- aud: audience (api)
- sub: subject identifier (user_id or service_id)
- exp / iat
- jti: token id
- org_id: current organization
- scopes: list of scopes (strings)
- roles: optional (role keys)
- ver: token schema version

### 4.2 Optional Claims
- project_id: only when endpoint is strictly project-scoped (avoid default).
- auth_level: e.g., mfa, password, sso.
- impersonated_by: admin id when using support impersonation.

### 4.3 Claim Rules
- org_id is mandatory for all non-public endpoints.
- org_id must be enforced server-side; never trust client-provided org_id headers.
- role/scope resolution rules must be consistent with docs/specs/08_rbac_model.md.

## 5. Authorization Model (RBAC + Scopes)
### 5.1 Concepts
- RBAC: roles grant permissions within an org.
- Scopes: token-level capability bounding what this token can do.

### 5.2 Precedence Rule
- Effective permission = intersection(role_permissions, token_scopes).
- If either denies, the request is denied.

### 5.3 Scope Naming Convention
- resource:action format.
  Examples:
  - org:read
  - project:read
  - project:write
  - mission:read
  - mission:write
  - assignment:write
  - planning:publish
  - audit:read
  - admin:impersonate

### 5.4 Common Roles (examples)
- org_owner
- org_admin
- project_manager
- planner
- collaborator
- viewer

(Exact role-permission mapping remains defined in docs/specs/08_rbac_model.md; this document defines enforcement mechanics.)

## 6. Enforcement Hooks
### 6.1 FastAPI Request Pipeline
Required enforcement layers:
1. Authentication dependency
   - Validates token.
   - Loads session (if used).
   - Creates AuthContext.
2. Authorization dependency
   - Validates required scope(s).
   - Validates required permission(s).
3. Tenant enforcement
   - Inject org_id into the request context.
   - Ensure all db queries include org_id filters.

### 6.2 Service Layer
- Service methods accept AuthContext (or derived OrgContext) explicitly.
- No service method may accept org_id from request payload without verifying it matches AuthContext.org_id.

### 6.3 Persistence Layer
- All tables include org_id (or a derived tenant key) where applicable.
- Queries must enforce org_id in WHERE clause.
- Unique indexes are composite with org_id to avoid cross-tenant collisions.

### 6.4 Background Jobs
- Job payload must include org_id and actor_id (or service actor).
- Job runner must validate org_id exists and is allowed.
- Jobs must write audit events with correlation_id.

## 7. Data Isolation Guarantees
### 7.1 Isolation Invariants
- Invariant T1: A request scoped to org_id MUST never read/write records belonging to another org.
- Invariant T2: All identifiers returned to clients must be org-scoped.
- Invariant T3: Access to resources must always re-check org_id at read time (no cached assumptions).

### 7.2 DB-Level Protections (Recommended)
- Schema design: all tenant data rows include org_id.
- Optional: PostgreSQL Row Level Security (RLS) can be introduced later; Phase 2 uses app-enforced isolation.
- Optional: separate schemas per tenant is out of scope.

### 7.3 Cross-Tenant Reference Prevention
- Foreign keys must include org_id alignment.
- Services must validate that referenced entities share same org_id.

## 8. Sensitive Operations
### 8.1 Impersonation (Support/Admin)
- Must be explicitly enabled per org and audited.
- Access token includes impersonated_by claim.
- Audit event type: security.impersonation.start / stop.

### 8.2 Token Revocation
- Refresh tokens revocable per session.
- Access tokens revoked by session invalidation (token blacklist optional).

### 8.3 Rate Limiting and Abuse
- Apply per-org and per-user rate limits at API entry.
- Reject abusive clients with standard API error model.

## 9. Audit and Traceability Integration
### 9.1 Required Security Events
- auth.login.success / auth.login.failure
- auth.token.issued / auth.token.refresh
- auth.logout
- auth.session.revoked
- security.permission.denied
- security.impersonation.start / stop

### 9.2 Correlation
- Each request has request_id.
- Each chain of operations shares correlation_id.
- Audit events include: org_id, actor_id, request_id, correlation_id.

### 9.3 Error Mapping
- Use docs/specs/11_api_error_model.md.
- Unauthorized -> 401 with error code auth.unauthorized
- Forbidden -> 403 with error code auth.forbidden
- Tenant mismatch -> 404 or 403 depending on leakage policy (default: 404 to avoid enumeration).

## 10. API Surface Rules
### 10.1 Headers
- Authorization: Bearer <token>
- X-Request-Id: optional client-provided, else generated.
- X-Correlation-Id: optional, propagated to jobs.

### 10.2 Public Endpoints
- /health, /metrics (metrics may be restricted).
- Any other public endpoint must be explicitly documented and justified.

## 11. Testing and Acceptance Criteria
### 11.1 Acceptance Criteria
- All endpoints have an authn/authz dependency chain defined.
- All service methods accept AuthContext (or OrgContext) and enforce org_id.
- All db queries are org-filtered.
- Audit events are emitted for security-sensitive operations.

### 11.2 Test Matrix (Phase 2)
- Unit: RBAC evaluation and scope intersection.
- Integration: cross-org access attempts always denied.
- Integration: tenant mismatch returns 404 by default.
- Integration: revocation invalidates refresh token.
- Integration: background job runner enforces org_id and writes audit events.

## 12. Implementation Notes (Non-Normative)
- Prefer opaque refresh tokens stored server-side with rotation.
- Keep access tokens short-lived to reduce blast radius.
- Avoid embedding large permission sets in tokens; resolve roles server-side when possible.
