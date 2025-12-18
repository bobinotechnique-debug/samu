# Mission Run Sheet (Phase 1)

## Purpose
Document the canonical structure and governance for mission run sheets (operational call sheets) used to coordinate mission execution without implementing APIs or UI changes. This replaces the earlier Phase 1 addendum tied to the mission roadmap and becomes the authoritative reference for operational run sheets.

## Concept and Scope
- **Mission run sheet**: an operational call sheet that consolidates mission-critical details for day-of execution and coordination.
- **Mission-scoped**: every run sheet belongs to exactly one mission and inherits mission identifiers, RBAC, and audit scope.
- **Project-scoped**: missions (and their run sheets) are always nested under a project; project context must be present on every view and export.
- **Org-scoped**: organization is the security boundary; cross-organization access to run sheets is forbidden.
- **Single active run sheet per mission**: at most one run sheet may be in `validated` or `published` status for a mission at any time; drafts can exist but only one may be promoted.

## Status Lifecycle
- **draft**: editable working copy; may be iterated and versioned prior to validation.
- **validated**: internally approved; locked to RBAC and audit rules but still retractable to `draft` for corrections; cannot bypass mission RBAC inheritance.
- **published**: immutable except for new versions; distribution-ready for operational use. Any change requires creating a new version, preserving prior published artifacts.
- **archived**: retired snapshot; remains read-only for audit/history and cannot return to active states.

## Versioning and Immutability
- Each status transition creates an immutable revision identifier; `published` and `archived` revisions must never be edited in place.
- Draft revisions can be superseded, but published revisions require creating a new version derived from the latest validated draft.
- All versions inherit mission audit metadata (created_by, created_at, organization_id, project_id, mission_id) and retain provenance to the source revision.
- Attachments and exports (PDF, images, plans) are version-pinned; replacing an attachment generates a new revision.

## Required Sections
- **Header**: mission identifiers, project identifiers, organization identifiers, mission window (start/end), mission status, and current run sheet version.
- **Personnel assignments**: structured list of personnel with fields `who`, `role`, `start_at`, `end_at`, contact channel, and required certifications if applicable.
- **Schedule slots**: ordered time slots with labels, start/end timestamps, dependencies, and designated owner; collisions with mission schedule must be detectable but not auto-resolved in Phase 1.
- **Location and access info**: site addresses, access instructions, geospatial references if available, and ingress/egress constraints; inherits location identifiers from docs/specs/20_location_and_maps_contracts.md.
- **Operational notes**: free-form notes with required author, timestamp, and visibility scope (e.g., internal-only vs. field-visible); notes are immutable once the run sheet is published.

## Attachments
- Run sheets may reference attachments (PDFs, images, operational plans). Each attachment must declare filename, type, size, checksum, and version linkage to the run sheet revision.
- Attachments are read-only for published/archived revisions; replacing or removing an attachment requires a new revision.

## Audit and RBAC Inheritance
- Run sheets inherit RBAC evaluation from the parent mission; no permissions may bypass organization or project scope.
- Audit trails must capture creation, validation, publication, and archival events, including actor, timestamp, and previous revision reference.
- Exports (PDF/CSV) must embed audit metadata and version identifiers to prevent detached distribution from losing traceability.

## Operational Constraints (Phase 1)
- Documentation-only: no backend, frontend, data model, or migration work is allowed in Phase 1 for this contract.
- Roadmap alignment: future implementation steps must reference this specification and the relevant Phase 1 roadmap entries before enabling write paths.
- Compliance: all representations remain ASCII-only and adhere to existing API conventions for read-only envelopes.
