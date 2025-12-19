# Phase 1 Extension - Planning Cost View (Spec 29)

## Purpose
- Provide real-time, planning-driven cost visibility without introducing accounting-grade calculations.
- Keep organization as the security boundary and project as the functional boundary while using missions as the execution and cost aggregation unit.
- Honor Phase 1 lock rules by delivering documentation-only guidance that does not add business logic or persistence.

## Scope and Principles
- Inputs are derived from planning data only: assignments, planned dates/duration, and declared rates or cachets.
- Costs are declarative and non-binding; no financial value is legally authoritative.
- No storage of computed totals; all cost outputs are derived views recomputed on demand or from cached planning state.
- Assignments remain project-scoped; no cross-project or cross-organization aggregation is permitted.

## Inputs and Derivation Rules
- **Assignments**: source planned collaborator, role, mission, and scheduled dates.
- **Rates/Cachets**: declarative rate or cachet attached to the assignment or role within the project.
- **Mission Duration**: planning duration derived from mission schedule and assignment coverage.
- **Cost Formula**: `derived cost = assignment coverage x declared rate/cachet`; no rounding or payroll adjustments are applied in this view.
- **Source of Truth**: planning data and declarative rates/cachets; no accounting ledgers, invoices, or payments are consulted.

## Derived Views
- **Cost per day**: displays derived cost for each planned day of an assignment using the active rate/cachet; read-only and refreshed from planning data.
- **Cost per mission**: aggregates derived assignment costs over the mission timeline; only missions within the current project are in scope.
- **Cost per project**: aggregates derived mission costs inside the same project; cross-project rollups are forbidden.

## Display and Visibility Rules
- Views are display-only; no persisted totals, accruals, or journal-like records are created.
- Finance roles can see rate/cachet inputs; non-finance roles receive read-only totals with obfuscated rate/cachet where required by RBAC.
- All views must indicate that values are derived estimates, not accounting or payroll outputs.
- Updates follow planning changes; no manual overrides in the derived view layer.

## Audit Notes
- Derived views are reproducible from planning data and declarative rates/cachets and are explicitly non-authoritative for accounting or payroll.
- Audit trails capture the source planning snapshot reference but do not store computed totals.

## Non-Goals
- Payroll calculations, payslips, or legal declarations.
- Accounting validation, ledger postings, or regulatory exports.
- Automatic payments, banking integrations, or storage of computed balances.
