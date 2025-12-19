# Phase 1 Extension - Cost Centers (Spec 31)

## Purpose
- Enable fine-grain financial pilotage tied to planning without introducing accounting complexity.
- Keep organization as the security boundary and project as the functional boundary while using missions as the execution and cost aggregation unit.
- Provide documentation-only guidance with derived reporting and no accounting ledger semantics.

## Cost Center Entity
- Examples: technical, artistic, transport, catering, accommodation, post-production.
- Cost centers are declarative categories scoped to the project and organization; no cross-organization sharing.
- No accounting chart-of-accounts mapping is created; this remains a planning-oriented classification.

## Link Rules for Financial Lines
- **Financial line -> project**: mandatory; no line can exist without a project context.
- **Financial line -> mission**: mandatory for mission-bound spend; optional only for project-level lines that are not mission-specific.
- **Financial line -> cost center**: mandatory; every line must be classified.
- No cross-project aggregation or linkage is allowed; derived reports stay within a single project boundary.

## Usage in Reports and Views
- Reports and planning cost views can filter and group by cost center within the project.
- Derived cost calculations remain display-only; no storage of computed totals or balances.
- Cost center breakdowns must align with missions and assignments when rendered in planning-derived cost views.

## Constraints and Non-Goals
- No accounting chart-of-accounts, journal postings, or legal exports.
- No automatic payments or banking synchronization.
- No aggregation across organizations or projects; mission remains the aggregation unit for execution and costs.
