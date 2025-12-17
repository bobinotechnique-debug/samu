# Persistence and Data Model

## Purpose
Describe the database structure that maps Phase 1 entities to PostgreSQL tables, relations, indexes, and deletion policies while preserving organization isolation and auditability.

## Core Tables
- **organizations** (id, name, slug, created_at, updated_at)
- **projects** (id, organization_id, name, code, status, created_at, updated_at)
- **missions** (id, organization_id, project_id, title, status, start_date, end_date, created_at, updated_at)
- **assignments** (id, organization_id, project_id, mission_id, collaborator_id, role, allocation_pct, created_at, updated_at)
- **collaborators** (id, organization_id, name, email, timezone, created_at, updated_at)
- **audit_events** (id, organization_id, project_id, actor_id, entity_type, entity_id, action, correlation_id, metadata, created_at)

## Relationships
- **organizations** 1..N **projects**, **collaborators**.
- **projects** 1..N **missions**, **assignments**.
- **missions** 1..N **assignments**.
- **collaborators** 1..N **assignments** (within the same organization).
- **audit_events** link to any entity via entity_type/entity_id with required organization_id and optional project_id.

## Indexes
- organizations.slug (unique)
- projects.organization_id + code (unique), projects.organization_id (foreign key index)
- missions.project_id, missions.organization_id + status
- assignments.mission_id, assignments.collaborator_id, assignments.organization_id + project_id + mission_id (composite)
- collaborators.organization_id + email (unique)
- audit_events.organization_id + created_at (for retention queries), audit_events.correlation_id (searchable)

## Soft Delete Rules
- Soft delete flags (deleted_at, deleted_by) on projects, missions, assignments, and collaborators; organizations are immutable except for lock state.
- Deleted records remain queryable for audit with filters requiring deleted_at IS NULL by default.
- Cascade rules: deleting a mission marks related assignments as deleted; projects cannot be deleted if missions exist without explicit archival workflow.

## Data Integrity
- All tables require organization_id and, where applicable, project_id to enforce ownership (docs/specs/07_data_ownership.md).
- Foreign keys enforce same-organization relationships; cross-organization references are forbidden.
- Timestamps stored in UTC per docs/specs/13_identifiers_and_time.md.

## Migration and Seeding Principles
- Migrations executed via managed scripts (migrate.ps1) with repeatable idempotent seeding guarded by organization context.
- Schema changes must preserve audit compatibility and avoid breaking Phase 1 identifiers; new tables must register org_id/project_id.
