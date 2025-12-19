# API Documentation Index

This index mirrors api/INDEX.md and tracks API contract records under Docs Agent governance.

- Status and inventory: docs/STATUS_SUMMARY.md.

- Refer to api/INDEX.md for endpoint catalogs and schemas.
- Align updates with roadmap steps and AGENT.md precedence.
- Ensure API docs stay ASCII-only and validated by guards.
- docs/api/20_api_architecture.md - Phase 2 API architecture and routing scaffolds (routing tree, versioning, dependencies, error mapping, pagination, and middleware).
- Canonical health endpoints are non-versioned GET /health/live and GET /health/ready (readiness checks DB and required dependencies); /api/v1/health is an optional compatibility alias only.
- Organizations and memberships vertical slice endpoints registered under /api/v1/orgs (context/me, list, create, memberships list/add) per Phase 2 Step 11.
