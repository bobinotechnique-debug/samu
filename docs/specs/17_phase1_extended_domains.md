# Phase 1 Extended Domain Specifications (Proposed Steps 08-10)

## Purpose
Extend Phase 1 documentation to cover roadmap operations, inventory and equipment management, and finance and accounting contracts before any implementation begins. These specifications remain documentation-only and lock expectations that later phases must implement without deviation.

## Scope
- Documentation-only contracts for operational roadmap execution, inventory and equipment lifecycle management, and finance/accounting read models.
- Alignment with existing API conventions, ownership rules, RBAC, audit, and multi-tenancy constraints from earlier Phase 1 steps.
- Requirements for indexing, roadmap linkage, and printable/export-friendly read models to keep operational users unblocked without code changes.

## Constraints
- Phase 1 forbids backend, frontend, infrastructure, and CI modifications.
- Organization remains the security boundary; all contracts include organization_id and project_id scoping where relevant.
- No cross-organization data access, no client-generated authoritative identifiers, and UTC/ISO 8601 time handling per docs/specs/13_identifiers_and_time.md.
- All exports, PDFs, and print views are read-only until implementation phases unlock write paths.

## Domain Contracts

### Roadmap and Execution Sheets (Step 08)
- **Operational run sheets**: define required fields (project, mission, site, collaborators, time windows, checkpoints, dependencies, RBAC constraints) and formats for day-of execution without granting write access.
- **Daily / event-based planning exports**: CSV and PDF exports that respect filtering (by date, mission status, ownership) and preserve audit metadata without exposing internal identifiers publicly.
- **Print and PDF oriented views**: read-only layouts optimized for on-site consumption; must include pagination rules, watermarking requirements, and explicit disclaimers about authoritative data sources.
- **Read-only operational contracts**: explicit GET-only API envelopes that mirror docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md; forbid mutation endpoints and enforce organization/project scoping.

### Inventory and Equipment Management (Step 09)
- **Equipment catalog**: required attributes (reference code, category, capability tags, maintenance windows, owning organization) and validation rules for catalog entries.
- **Availability and assignment**: read models that map equipment to projects/missions with time-bound availability, compatibility with mission requirements, and conflict detection rules.
- **Conflict and maintenance states**: canonical states (available, reserved, in-mission, maintenance, decommissioned) with transition constraints and audit hooks; conflicts cannot be auto-resolved in Phase 1.
- **Ownership and organization scoping**: all catalog and assignment records carry organization_id; cross-organization lending is forbidden unless a future roadmap step explicitly approves it.

### Finance and Accounting (Step 10)
- **Cost tracking per project and mission**: required data points for actuals (labor, equipment, travel) and how they align with mission milestones and assignments.
- **Rates, budgets, and forecasts**: contract for storing rate cards, budget baselines, and forecast snapshots with effective dates and currency handling; all amounts must declare currency and precision rules.
- **Invoicing and export contracts**: read-only invoice drafts and export specifications (CSV/PDF) aligned to API conventions; no payment processing or ledger mutations in Phase 1.
- **Accounting read models**: immutable projections suitable for reconciliation and audits, including provenance fields (source system, generated_at, version) and ties to organization/project scopes.

## Governance and Alignment
- Every domain contract references roadmap entries in docs/roadmap/phase1/step-08.md, step-09.md, and step-10.md and must be indexed in docs/specs/INDEX.md and specs/INDEX.md.
- Documentation must remain ASCII-only, cite applicable Phase 1 constraints, and avoid TODO placeholders.
- Implementation planning must trace back to these contracts and respect existing audit, RBAC, and multi-tenancy rules before any code work begins.
