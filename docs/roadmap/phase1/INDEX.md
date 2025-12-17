# Phase 1 Roadmap Index

## Status
Active; executing Step 04 to lock API and integration conventions; Steps 05-07 completed and registered; Step 11 active to document cross-domain read models and integration rules; Steps 08-10 proposed for extended domains.

## Steps
- docs/roadmap/phase1/step-00.md - Phase 1 Step 00: initiate documentation-focused phase (Status: Done).
- docs/roadmap/phase1/step-02.md - Phase 1 Step 02: architecture guardrails, contracts, and failure patterns (Status: Done).
- docs/roadmap/phase1/step-03.md - Phase 1 Step 03: data ownership, RBAC, and audit rules (Status: Done).
- docs/roadmap/phase1/step-04.md - Phase 1 Step 04: API and integration conventions (Status: In progress).
- docs/roadmap/phase1/step-05.md - Phase 1 Step 05: UX visual language and view specifications (Status: Done).
- docs/roadmap/phase1/step-06.md - Phase 1 Step 06: UI component contracts (Status: Done).
- docs/roadmap/phase1/step-07.md - Phase 1 Step 07: UI page contracts (Status: Done).
- docs/roadmap/phase1/step-08.md - Phase 1 Step 08: Roadmap and execution sheets (Status: Proposed).
- docs/roadmap/phase1/step-09.md - Phase 1 Step 09: Inventory and equipment management (Status: Proposed).
- docs/roadmap/phase1/step-10.md - Phase 1 Step 10: Finance and accounting (Status: Proposed).
- Phase 1 Step 11: Cross-domain read models and integration rules documented in docs/specs/18_cross_domain_read_models.md and docs/specs/19_domain_integration_rules.md (Status: Active).

## Notes
- Phase 1 prohibits backend, frontend, and infrastructure code changes; scope is limited to documentation artifacts.
- Step 02 depends on foundational domain documentation outcomes from Step 01 (glossary, domain model, project/mission model).
- Step 03 depends on Step 01 for terminology and Step 02 for architecture and contract guardrails.
- Step 04 depends on Steps 02 and 03 to align API contracts with architecture, ownership, RBAC, and audit invariants.
- Step 05 depends on Step 04 outputs for API alignment and keeps UX surfaces consistent with visual language rules.
- Step 06 depends on Step 05 visual language decisions to keep component contracts consistent across views.
- Step 07 assembles the approved Step 06 components under Step 04 conventions and the page contract rules in docs/specs/16_ui_page_contracts.md.
- Step 08 captures operational roadmap execution artifacts and relies on Steps 02-04 for ownership, RBAC, audit, and API conventions.
- Step 09 documents equipment catalog, availability, and conflict rules bound to organization/project scopes under Steps 02-04 constraints.
- Step 10 records finance and accounting contracts aligned to ownership, RBAC, audit, identifier, and API conventions defined in Steps 02-04.
