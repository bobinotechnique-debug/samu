# RBAC Model

## Purpose
Document an enforceable role-based access control model that constrains authorization design before implementation.

## Scope
- Applies to organization and project scoped operations across backend, frontend, and ops designs.
- Covers required roles, permissions, evaluation order, and forbidden shortcuts during Phase 1 documentation.

## Assumptions
- Organization is the security boundary; project is the functional boundary.
- Default-deny posture remains mandatory until explicit permissions are granted.
- Phase 1 delivers documentation only; enforcement will be implemented later.

## Exclusions
- Identity provider configuration or SSO mechanics.
- UI role-switching behaviors or token handling details.

## Roles
- org_owner: Full control over organization configuration, projects, and role delegation.
- org_admin: Manage projects, membership, and role assignments within the organization; cannot transfer ownership unless delegated.
- project_manager: CRUD over projects they manage, missions within those projects, and project-level role bindings.
- planner: Create and update missions and planning artifacts within assigned projects; cannot manage organization-level settings.
- member: Execute mission tasks and update assignments within assigned projects; no administrative capabilities.
- viewer: Read-only access scoped to assigned organization and project contexts.

## Permission Model
- Authorization MUST be evaluated with a default-deny rule: any action without an explicit allow in scope MUST be rejected.
- Permission evaluation MUST first check organization-level authorization, then project-level authorization; failure at either layer MUST deny the action.
- CRUD mapping by domain:
  - Organization: org_owner and org_admin MAY create/update projects and manage org-level role bindings; only org_owner MAY delete organizations or transfer ownership.
  - Project: org_owner, org_admin, and project_manager MAY create/update projects; only org_owner and org_admin MAY archive or delete projects; project_manager MAY NOT alter org-level settings.
  - Mission and planning: project_manager and planner MAY create/update missions and planning artifacts within their projects; deletion of missions requires project_manager or higher with org alignment; viewers MAY NOT modify any mission data.
  - Assignments: project_manager and planner MAY create/update assignments; members MAY update assignment status for their own assignments; viewers have read-only access.
- Role bindings MUST be recorded with org_id and, when project-scoped, project_id to prevent scope leakage.

## Forbidden Shortcuts
- Frontend-only gating MUST NOT be treated as authorization; the backend MUST enforce permissions using the default-deny model.
- Client-provided claims MUST NOT be trusted without backend validation against stored role bindings.
- Role escalation via project membership alone is forbidden; organization authorization MUST be validated first.

## Audit Alignment
- Role changes and permission grants or revocations MUST emit audit events as defined in docs/specs/09_audit_and_traceability.md.
- Authorization decisions SHOULD include correlation ids to tie access checks to audit records.
