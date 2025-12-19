# Phase 1 - Step 22: Planning Economic Extension (Amendment)

## Purpose
Document an amendment that strengthens planning-driven economic pilotage and contract coherence under the Phase 1 lock (Step 14).

## Status
Proposed (documentation-only amendment; no business logic or persistence changes).

## Objectives
- Extend planning cost visibility with derived, display-only views scoped to project and mission.
- Bind contracts to assignments with lifecycle and warning rules to surface completeness gaps without blocking execution.
- Introduce project- and mission-scoped cost centers for planning-oriented reporting without accounting ledgers.

## Deliverables
- docs/specs/29_planning_cost_view.md covering derived planning cost views (per-day, per-mission, per-project).
- docs/specs/30_contract_assignment_link.md documenting contract-to-assignment linkage and non-blocking completeness alerts.
- docs/specs/31_cost_centers.md defining cost center classification and linkage rules for planning financial lines.
- Index updates (docs/specs/INDEX.md, specs/INDEX.md) registering the new specifications.
- CHANGELOG.md entry referencing this amendment.

## Acceptance Criteria
- All specifications remain ASCII-only, Phase 1 aligned, and non-authoritative for accounting or payments.
- Organization is the security boundary; project is the functional boundary; missions are the execution and cost aggregation unit.
- Derived costs are display-only with no stored totals; no cross-project aggregation or legal exports.
- Contract completeness warnings surface in dashboards and project views without blocking planning.

## Notes
- This step amends the sealed Phase 1 scope via the Step 14 charter and follows the Step 21 precedent for finance and contract documentation.
- Any future corrections must reference this amendment and preserve the non-regression rules from docs/roadmap/phase1/step-14.md.
