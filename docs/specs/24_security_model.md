# Security and Trust Model

## Purpose
Define concrete security mechanisms that guarantee organization isolation, enforce RBAC, and preserve auditability for Phase 2 architecture.

## Authentication Flows
- **User login:** OIDC/OAuth2 authorization code with PKCE issuing access and refresh tokens scoped to organization_id and actor_id.
- **Service tokens:** Signed JWTs for internal automation with restricted scopes and explicit organization_id; rotation managed via secrets store.
- **Token refresh:** Refresh tokens stored securely with rotation on use; revoke paths clear active sessions for an organization.

## Token Scopes and Claims
- Required claims: sub (actor_id), organization_id, optional project_id context, roles, scopes, issued_at, expires_at, correlation_id seed.
- Scopes align with Phase 1 RBAC permissions and are evaluated in order: organization -> project -> resource action.
- Tokens must include audience matching API/worker services; workers verify signatures before accepting job payloads.

## Authorization Enforcement
- API middleware extracts organization_id/project_id from tokens and request paths; denies if missing per docs/specs/07_data_ownership.md.
- Application layer checks permissions against docs/specs/08_rbac_model.md before invoking domain services.
- Workers re-validate scopes on job consumption to prevent privilege escalation via queues.

## Data Isolation
- All data access filters by organization_id and, when applicable, project_id; no shared tables without org_id.
- Redis caches and queues namespace keys by organization_id to prevent cross-tenant leakage.
- Audit events include organization_id and project_id to align with docs/specs/09_audit_and_traceability.md.

## Transport and Secrets
- HTTPS enforced for all external endpoints; internal services communicate over mTLS within the compose network.
- Secrets (JWT signing keys, OAuth client secrets, database credentials) stored in environment-specific secret stores and injected via runtime configuration, never in code or images.

## Monitoring and Incident Response
- Security events (failed logins, token revocations, denied authorizations) logged with correlation_id and actor context.
- Alerting thresholds configured per organization to detect brute force or anomalous access patterns.
- Incident runbooks reference docs/ops/20_deployment_architecture.md for rotation and isolation steps.

## Alignment with Phase 1
- Enforces multi-tenancy and security expectations (docs/specs/03_multi_tenancy_and_security.md).
- Applies ownership and RBAC rules from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md.
- Preserves audit guarantees from docs/specs/09_audit_and_traceability.md and error handling from docs/specs/11_api_error_model.md.
