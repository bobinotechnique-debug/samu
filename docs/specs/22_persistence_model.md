# Persistence and Data Model

## Purpose
Define the PostgreSQL persistence design that maps Phase 1 entities to concrete tables, relationships, indexes, and deletion policies while preserving organization isolation, project scoping, and auditability.

## Authoritative principles
1. Organization is the security boundary; no cross-organization joins in API behavior.
2. Project is the functional boundary; missions, planning, and assignments cannot exist outside a project.
3. Every tenant-scoped row carries `org_id`; every project-scoped row carries both `org_id` and `project_id`.
4. Soft delete is the default for mutable business entities; hard delete is limited to ephemeral/derived data or explicit purge.
5. All writes are attributable (`created_by`, `updated_by`) and timestamped in UTC.
6. Primary keys are UUIDs. Public identifiers may be added later without changing internal UUID keys.

## PostgreSQL conventions
- Schema: `public` (single schema).
- Naming: snake_case table and column names; foreign keys use `<ref>_id`.
- Types: `uuid` primary keys; `timestamptz` for timestamps; `deleted_at timestamptz NULL` for soft delete.
- Soft delete contract: rows are active when `deleted_at IS NULL`; default queries MUST filter accordingly. Uniqueness uses partial indexes scoped to active rows.

## Multi-tenancy and isolation
- **Row-level isolation**: every tenant-scoped table includes `org_id`.
- **Project isolation**: every project-scoped table includes `project_id` and `org_id`.
- **Foreign key safety**: foreign keys for tenant/project scoped tables MUST ensure matching `org_id` and (when applicable) `project_id`, via composite keys or triggers in implementation.

## Entity inventory (Phase 1 mapping)
- Organization
- User and Membership (organization membership)
- Project
- Collaborator
- Mission
- Assignment
- Role / Skill
- Availability / Unavailability
- Tags / Labels
- Audit events
- Notification outbox

## Tables
### 1) organizations
Purpose: tenant boundary.

Columns:
- `id uuid PK`
- `name text NOT NULL`
- `slug text NOT NULL`
- `status text NOT NULL DEFAULT 'active'` (active | suspended | closed)
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_organizations_slug_active`: UNIQUE (`slug`) WHERE `deleted_at IS NULL`.

Deletion: soft delete only; organization delete triggers policy-driven cascade of soft deletes to org-scoped entities.

### 2) users
Purpose: global identity record. Users can belong to many organizations.

Columns:
- `id uuid PK`
- `email text NOT NULL`
- `display_name text NULL`
- `status text NOT NULL DEFAULT 'active'`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_users_email_active`: UNIQUE (`email`) WHERE `deleted_at IS NULL`.

Deletion: soft delete only.

### 3) org_memberships
Purpose: link users to organizations and capture org-level roles.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL` FK -> `organizations(id)`
- `user_id uuid NOT NULL` FK -> `users(id)`
- `role text NOT NULL` (owner | admin | manager | planner | viewer)
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_org_memberships_org_user_active`: UNIQUE (`org_id`, `user_id`) WHERE `deleted_at IS NULL`.
- `ix_org_memberships_org_id_active`: (`org_id`) WHERE `deleted_at IS NULL`.
- `ix_org_memberships_user_id_active`: (`user_id`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 4) projects
Purpose: functional boundary for planning.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL` FK -> `organizations(id)`
- `name text NOT NULL`
- `code text NULL`
- `timezone text NOT NULL DEFAULT 'UTC'`
- `status text NOT NULL DEFAULT 'active'` (active | archived)
- `start_at timestamptz NULL`
- `end_at timestamptz NULL`
- `created_by uuid NULL` FK -> `users(id)`
- `updated_by uuid NULL` FK -> `users(id)`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_projects_org_code_active`: UNIQUE (`org_id`, `code`) WHERE `deleted_at IS NULL` AND `code IS NOT NULL`.
- `ix_projects_org_id_active`: (`org_id`) WHERE `deleted_at IS NULL`.

Deletion: soft delete; project deletion workflow must soft delete all project-scoped entities.

### 5) collaborators
Purpose: person/resource that can be assigned to missions.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL` FK -> `organizations(id)`
- `default_project_id uuid NULL` FK -> `projects(id)`
- `kind text NOT NULL DEFAULT 'person'` (person | team | vendor)
- `first_name text NULL`
- `last_name text NULL`
- `display_name text NOT NULL`
- `email text NULL`
- `phone text NULL`
- `status text NOT NULL DEFAULT 'active'` (active | inactive)
- `created_by uuid NULL` FK -> `users(id)`
- `updated_by uuid NULL` FK -> `users(id)`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_collaborators_org_email_active`: UNIQUE (`org_id`, `email`) WHERE `deleted_at IS NULL` AND `email IS NOT NULL`.
- `ix_collaborators_org_id_active`: (`org_id`) WHERE `deleted_at IS NULL`.
- `ix_collaborators_name_trgm_active`: GIN (`display_name` gin_trgm_ops) WHERE `deleted_at IS NULL` (requires `pg_trgm`).

Deletion: soft delete; assignments referencing deleted collaborators remain for audit and history.

### 6) roles
Purpose: organization-scoped role catalog.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `name text NOT NULL`
- `color text NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_roles_org_name_active`: UNIQUE (`org_id`, `name`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 7) collaborator_roles
Purpose: many-to-many join between collaborators and roles.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `collaborator_id uuid NOT NULL` FK -> `collaborators(id)`
- `role_id uuid NOT NULL` FK -> `roles(id)`
- `created_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_collaborator_roles_active`: UNIQUE (`collaborator_id`, `role_id`) WHERE `deleted_at IS NULL`.
- `ix_collaborator_roles_collaborator_id_active`: (`collaborator_id`) WHERE `deleted_at IS NULL`.
- `ix_collaborator_roles_role_id_active`: (`role_id`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 8) skills
Purpose: organization-scoped skill catalog.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `name text NOT NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_skills_org_name_active`: UNIQUE (`org_id`, `name`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 9) collaborator_skills
Purpose: many-to-many join between collaborators and skills with proficiency metadata.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `collaborator_id uuid NOT NULL`
- `skill_id uuid NOT NULL`
- `level smallint NULL` (0..5)
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_collaborator_skills_active`: UNIQUE (`collaborator_id`, `skill_id`) WHERE `deleted_at IS NULL`.
- `ix_collaborator_skills_collaborator_id_active`: (`collaborator_id`) WHERE `deleted_at IS NULL`.
- `ix_collaborator_skills_skill_id_active`: (`skill_id`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 10) missions
Purpose: work item inside a project with a time window.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `project_id uuid NOT NULL` FK -> `projects(id)`
- `title text NOT NULL`
- `description text NULL`
- `location text NULL`
- `status text NOT NULL DEFAULT 'draft'` (draft | planned | in_progress | done | canceled)
- `start_at timestamptz NOT NULL`
- `end_at timestamptz NOT NULL`
- `created_by uuid NULL`
- `updated_by uuid NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- Validate `end_at > start_at`.
- `ix_missions_project_time_active`: (`project_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL`.
- `ix_missions_org_project_active`: (`org_id`, `project_id`) WHERE `deleted_at IS NULL`.
- `ix_missions_status_active`: (`project_id`, `status`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 11) assignments
Purpose: link collaborators to missions with optional role and sub-time range.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `project_id uuid NOT NULL`
- `mission_id uuid NOT NULL` FK -> `missions(id)`
- `collaborator_id uuid NOT NULL` FK -> `collaborators(id)`
- `role_id uuid NULL` FK -> `roles(id)`
- `status text NOT NULL DEFAULT 'assigned'` (assigned | confirmed | checked_in | completed | canceled)
- `start_at timestamptz NOT NULL`
- `end_at timestamptz NOT NULL`
- `notes text NULL`
- `created_by uuid NULL`
- `updated_by uuid NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- Validate `end_at > start_at`.
- `ix_assignments_project_time_active`: (`project_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL`.
- `ix_assignments_mission_active`: (`mission_id`) WHERE `deleted_at IS NULL`.
- `ix_assignments_collaborator_time_active`: (`collaborator_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL`.
- `ix_assignments_status_active`: (`project_id`, `status`) WHERE `deleted_at IS NULL`.
- Conflict detection support: `ix_assignments_collaborator_start_active`: (`collaborator_id`, `start_at`) WHERE `deleted_at IS NULL`.

Deletion: soft delete; prefer status transitions (e.g., canceled) over deletion for audit fidelity.

### 12) availability_blocks
Purpose: explicit availability or unavailability constraints.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `project_id uuid NULL` (NULL means org-wide availability)
- `collaborator_id uuid NOT NULL`
- `kind text NOT NULL` (available | unavailable)
- `start_at timestamptz NOT NULL`
- `end_at timestamptz NOT NULL`
- `source text NOT NULL DEFAULT 'manual'` (manual | import | sync)
- `reason text NULL`
- `created_by uuid NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- Validate `end_at > start_at`.
- `ix_availability_collaborator_time_active`: (`collaborator_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL`.
- `ix_availability_project_time_active`: (`project_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL` AND `project_id IS NOT NULL`.
- `ix_availability_org_time_active`: (`org_id`, `start_at`, `end_at`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 13) tags
Purpose: reusable org-scoped labels.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `name text NOT NULL`
- `color text NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_tags_org_name_active`: UNIQUE (`org_id`, `name`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

### 14) mission_tags
Purpose: tag missions.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `project_id uuid NOT NULL`
- `mission_id uuid NOT NULL`
- `tag_id uuid NOT NULL`
- `created_at timestamptz NOT NULL`
- `deleted_at timestamptz NULL`

Constraints and indexes:
- `uq_mission_tags_active`: UNIQUE (`mission_id`, `tag_id`) WHERE `deleted_at IS NULL`.
- `ix_mission_tags_mission_active`: (`mission_id`) WHERE `deleted_at IS NULL`.
- `ix_mission_tags_tag_active`: (`tag_id`) WHERE `deleted_at IS NULL`.

Deletion: soft delete.

## Audit and integration tables
### 15) audit_events
Purpose: immutable audit trail for writes and security events.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `actor_user_id uuid NULL`
- `actor_type text NOT NULL DEFAULT 'user'` (user | system | api_key)
- `action text NOT NULL` (create | update | delete | restore | publish | assign | unassign | login | ...)
- `entity_type text NOT NULL`
- `entity_id uuid NULL`
- `project_id uuid NULL`
- `occurred_at timestamptz NOT NULL`
- `request_id text NULL`
- `ip text NULL`
- `user_agent text NULL`
- `before jsonb NULL`
- `after jsonb NULL`

Indexes:
- `ix_audit_org_time`: (`org_id`, `occurred_at`).
- `ix_audit_entity`: (`entity_type`, `entity_id`).
- `ix_audit_project_time`: (`project_id`, `occurred_at`).

Deletion: append-only; no soft delete. Retention is policy-driven (default 2 years).

### 16) outbox_events
Purpose: transactional outbox for async notifications and integrations.

Columns:
- `id uuid PK`
- `org_id uuid NOT NULL`
- `project_id uuid NULL`
- `topic text NOT NULL`
- `payload jsonb NOT NULL`
- `status text NOT NULL DEFAULT 'pending'` (pending | processing | sent | failed | dead)
- `available_at timestamptz NOT NULL`
- `attempts int NOT NULL DEFAULT 0`
- `last_error text NULL`
- `created_at timestamptz NOT NULL`
- `updated_at timestamptz NOT NULL`

Indexes:
- `ix_outbox_pending`: (`status`, `available_at`).
- `ix_outbox_org`: (`org_id`, `created_at`).

Deletion: hard delete allowed after retention window (e.g., 30 days) via maintenance jobs.

## Relationships (logical)
- organizations 1..N projects
- users 1..N org_memberships
- organizations 1..N collaborators
- projects 1..N missions
- missions 1..N assignments
- collaborators 1..N assignments
- collaborators N..N roles (via collaborator_roles)
- collaborators N..N skills (via collaborator_skills)
- missions N..N tags (via mission_tags)
- collaborators 1..N availability_blocks
- organizations 1..N audit_events
- organizations 1..N outbox_events

## Index strategy (summary)
- Planning views by project/time: `missions(project_id, start_at, end_at)`, `assignments(project_id, start_at, end_at)`.
- Conflict detection by collaborator/time: `assignments(collaborator_id, start_at, end_at)`, `availability_blocks(collaborator_id, start_at, end_at)`.
- Fast catalog lookups: org-scoped catalogs using (`org_id`, `name`) unique partial indexes.
- Partial indexes use `WHERE deleted_at IS NULL` to coexist with soft delete.
- Optional search: `collaborators.display_name` GIN trigram index (pg_trgm).

## Soft delete and deletion policies
### Default policy
- Soft delete for: organizations, users, org_memberships, projects, collaborators, roles, skills, missions, assignments, availability_blocks, tags, and join tables.
- Append-only: audit_events.
- Derived/ephemeral cleanup allowed: outbox_events.

### Cascade semantics (policy)
- Deleting a project soft deletes missions, assignments, mission_tags, and project-scoped availability blocks.
- Deleting a collaborator soft deletes the collaborator; assignments remain for audit but collaborator is inactive.
- Deleting a role or skill soft deletes related join table rows; historical assignments retain role references where present.

### Restore semantics
- Restoration allowed only when uniqueness constraints for active rows are preserved.
- All restore operations MUST be audited.

## Data integrity invariants
- Any row with `project_id` references a project with the same `org_id`.
- `missions.project_id` belongs to the same `org_id` on the mission row.
- `assignments.project_id` matches `missions.project_id`.
- `assignments.org_id == missions.org_id == collaborators.org_id`.
- No assignment exists outside a project.

Enforcement is expected via composite foreign keys where possible or via triggers/deferred checks.

## Migration and evolution guidelines
- Favor additive changes (new nullable columns, new tables) to protect backward compatibility.
- Breaking changes require versioned migrations and backward-compatible API behavior.
- Add indexes concurrently on large tables in production environments.

## Open questions (deferred)
- Do we need separate `mission_instances` versus templates, or is `missions` the instance?
- Should recurrence (RRULE) live on missions or in a dedicated table?
- Do equipment/resource planning requirements appear in Phase 2 or later?

## Acceptance criteria
- All Phase 1 entities map to tables with explicit `org_id` and `project_id` rules.
- Core relationships and isolation rules are defined.
- Indexes cover planning reads and conflict detection.
- Soft delete and uniqueness rules rely on partial indexes.
- Audit and outbox persistence skeletons are present.
