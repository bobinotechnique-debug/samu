# Domain Integration Rules (Phase 1 Step 11)

## Purpose
Document read-level integration contracts across Planning, Inventory, Finance, and Operations to prevent hidden coupling and to align all cross-domain access with Phase 1 constraints before implementation.

## Scope and Constraints
- Applies to read-only integrations; no workflow orchestration, schedulers, or event pipelines in Phase 1.
- Organization_id and project_id are required on every read path; cross-organization access is forbidden.
- No bidirectional writes, side effects, or implicit state changes triggered by read models.
- All contracts inherit API, versioning, identifier, RBAC, and audit requirements from docs/specs/10_api_conventions.md, docs/specs/11_api_error_model.md, docs/specs/12_api_versioning.md, docs/specs/13_identifiers_and_time.md, docs/specs/07_data_ownership.md, and docs/specs/09_audit_and_traceability.md.

## Integration Contracts

### Cross-Domain Read Model Registration
- Every read model must declare source domains, ownership, and provenance fields; projections cannot redefine authoritative fields from source domains.
- Versioning must be explicit: projection_version, source_schema_version, and source_revision identifiers are mandatory.
- Snapshots are immutable; new facts generate new projection versions rather than editing prior emissions.

### Referential Link Rules
- Links between Project, Mission, Assignment, Equipment, and Cost/Rate references must use opaque, server-issued identifiers.
- Links are organization- and project-scoped; missing scope fields invalidate the projection.
- References must include observed_at timestamps when the link was captured to avoid time-skewed reads.

### Snapshot and Versioning Discipline
- Snapshot timing is explicitly documented per model (mission start, assignment confirmation, rate card effective period, maintenance state observed_at).
- Projections must store effective_from/effective_to ranges where applicable to allow deterministic reconciliation.
- Audit envelopes (generated_at, generated_by_system, correlation_id) are mandatory for traceability and replay-free reads.

### Conflict Visibility and Guardrails
- Conflicts (equipment overbooking, rate mismatch, mission overlap) are surfaced as read-only indicators with deterministic calculation notes; no auto-resolution in Phase 1.
- Maintenance states are visible but cannot trigger scheduling or cost recalculations.
- Finance reads cannot alter Planning or Inventory states, and Planning reads cannot generate Finance postings.

### Forbidden Coupling Patterns
- No implicit dependency on write order across domains; reads must tolerate independent deployment and versioning.
- No client-driven joins that bypass API contracts; composite projections are produced server-side under documented schemas.
- No inference of availability or budget approvals beyond what is explicitly stated in source domains.
- No background jobs, sync engines, or batch mutations introduced through read models in Phase 1.

### Alignment and Governance
- Integration rules are indexed alongside docs/specs/18_cross_domain_read_models.md to keep Phase 1 Step 11 traceable.
- Changes to integration contracts must update roadmap indexes and changelog entries and remain ASCII-only with no TODO placeholders.
- Future implementation phases must honor these constraints and extend them with explicit roadmap approval before enabling writes or orchestration.
