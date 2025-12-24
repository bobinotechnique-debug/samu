# Phase 2 Step 11 - First Vertical Slice (Auth + Org Context + RBAC Hooks)

Status: In Progress

## Goal

Deliver the first end-to-end slice with persistent auth, strict organization context enforcement, and RBAC hooks that exercise organizations and memberships over real storage.

## Scope

- Auth baseline using bearer tokens stored in the database with organization context selection.
- Principal context extraction (actor, org, roles, permissions, token id) attached to request tracing.
- RBAC guard for org and membership read/write permissions.
- Minimal CRUD surface: organizations (context and listing) and memberships (listing and invite/add).
- Audit fields (created/updated by + timestamps + request id) stamped on slice entities.

## Deliverables

- FastAPI dependency that enforces authentication, validates organization context, checks organization activity, and resolves memberships.
- Permission check helper aligned to Phase 1 RBAC model for org:read/org:write and membership:read/membership:write.
- API endpoints (v1) for active org context, listing orgs for the actor, creating orgs, listing memberships, and adding members.
- Persistence tables with alembic migration for users, organizations, memberships, and auth tokens.
- Seed script for local/dev tokens, user, orgs, and memberships.
- Frontend thin client to store a token, select org context, list orgs, and list memberships.
- Operational run flow documented at docs/ops/22_local_run_flow.md covering migrations, seed paths, and service startup for the slice.

## Acceptance

- Protected routes reject missing/invalid tokens (401) and missing/invalid org context (400/403).
- RBAC enforcement blocks membership writes for insufficient roles (403).
- Organization and membership queries are scoped to actor memberships.
- Error payloads follow the Phase 1 error model (code/message/details) for 401/403/404.
- Tests cover auth_required, org_context_required, RBAC forbidden, scoped org/membership listing, and error model shapes.
