# Cross-Domain Read Models (Phase 1 Step 11)

## Purpose
Define authoritative, read-only projections that combine Planning, Inventory, Finance, and Operations data without introducing mutation paths. These views guarantee organization- and project-scoped consumption while preserving ownership boundaries set in Phase 1 Steps 00-10.

## Scope and Constraints
- Documentation-only under Phase 1; no backend, frontend, infra, or CI changes.
- Organization_id and project_id are mandatory in every view; no cross-organization access.
- Read models are denormalized projections sourced from domain systems but never mutate source data.
- Snapshots capture effective data at retrieval time with explicit version metadata; no background jobs or auto-calculation logic.
- All contracts follow docs/specs/10_api_conventions.md, docs/specs/11_api_error_model.md, docs/specs/12_api_versioning.md, and docs/specs/13_identifiers_and_time.md.

## Read Models

### Planning x Inventory: Mission Equipment Read Model
- **Source domains**: Planning (Mission, Assignment), Inventory (Equipment catalog, availability, maintenance states).
- **Payload**: Mission, required equipment categories/capabilities, candidate equipment references, availability windows, conflicts, maintenance overlays, organization_id, project_id.
- **Snapshot timing**: Point-in-time at query execution; mission and equipment states are captured with observed_at timestamps.
- **Versioning and audit**: Each record includes projection_version, source_schema_version, generated_at (UTC), and traceable source_ids; changes require append-only history, never overwrite source.
- **Coupling guardrails**: No write backs to Planning or Inventory; conflicts are surfaced but not resolved; no implicit assignment creation.

### Planning x Finance: Mission Cost Attribution Read Model
- **Source domains**: Planning (Mission milestones, Assignments), Finance (rates, cost actuals/budgets).
- **Payload**: Mission milestones with rate snapshots, assignment references, cost buckets (labor, equipment, travel), currency, precision, organization_id, project_id.
- **Snapshot timing**: Uses the effective rate and budget snapshot valid at mission start time with retrieval timestamp; retroactive adjustments produce a new snapshot version, not mutation.
- **Versioning and audit**: projection_version, rate_snapshot_id, budget_snapshot_id, generated_at (UTC), provenance (source systems, calculation inputs), and audit trail references per docs/specs/09_audit_and_traceability.md.
- **Coupling guardrails**: No automatic accruals or invoice generation; Planning cannot drive Finance writes; Finance cannot override mission structure.

### Planning x Finance: Project Aggregated Cost Read Model
- **Source domains**: Planning (Project, Missions), Finance (rate cards, budgets, actuals).
- **Payload**: Aggregated costs by mission phase and category, rate snapshot references, budget variance, currency, organization_id, project_id.
- **Snapshot timing**: Generated on-demand per query with aggregation timestamp; aggregation rules are deterministic and documented in Finance schemas.
- **Versioning and audit**: projection_version, aggregation_version, generated_at (UTC), source revision identifiers, and audit trail links; previous aggregations remain discoverable.
- **Coupling guardrails**: No automatic rebilling or project status changes; aggregation does not persist to Finance ledgers during Phase 1.

### Inventory x Finance: Equipment Usage Cost Read Model
- **Source domains**: Inventory (Equipment catalog, usage logs, maintenance states), Finance (rate cards, depreciation/usage costs).
- **Payload**: Equipment reference, usage intervals tied to missions/assignments, maintenance state overlays, cost attribution by category, currency, organization_id, project_id.
- **Snapshot timing**: On-demand projection using the effective rate card at usage start with retrieval timestamp; maintenance states are read-only overlays.
- **Versioning and audit**: projection_version, rate_snapshot_id, maintenance_state_version, generated_at (UTC), traceable source_ids; append-only history for reconciliation.
- **Coupling guardrails**: No scheduling changes, no maintenance automation, and no ledger postings; Finance cannot change equipment availability through this model.

### Planning x Inventory x Finance: Assignment Rate Snapshot Reference
- **Source domains**: Planning (Assignments, Missions), Inventory (Equipment allocations if present), Finance (rate cards, allowances).
- **Payload**: Assignment reference, applicable rate snapshot id, equipment dependency references, effective dates, currency, organization_id, project_id.
- **Snapshot timing**: Rate snapshot captured at assignment confirmation; retrieval includes observed_at to reflect when the read model was produced.
- **Versioning and audit**: projection_version, rate_snapshot_id, generated_at (UTC), audit correlation id; new rate versions append, prior snapshots remain immutable.
- **Coupling guardrails**: No automatic reassignment or rate recalculation; Planning cannot alter Finance rates, and Finance cannot edit assignments through this view.

## Snapshot and Versioning Rules
- Projections are immutable once emitted; new information creates a new projection_version with references to source revisions.
- Timestamps use UTC ISO 8601; effective_from/effective_to enforce deterministic interpretation.
- Audit fields (generated_at, generated_by_system, provenance) are mandatory and align with docs/specs/09_audit_and_traceability.md.

## Forbidden Coupling Patterns
- No bidirectional writes or side effects triggered by read model access.
- No implicit dependency on background jobs, schedulers, or event pipelines to refresh projections during Phase 1.
- No hidden data joins that bypass ownership boundaries; all joins must be explicit and organization/project scoped.
- No client-driven identifier generation; all identifiers remain server-issued and opaque.

## Compliance and Alignment
- Contracts inherit constraints from Phase 1 Steps 00-10 and are tagged to roadmap Phase 1 Step 11 for traceability.
- All read models must be indexed in docs/specs/INDEX.md and specs/INDEX.md and referenced in roadmap indexes without enabling implementation work.
