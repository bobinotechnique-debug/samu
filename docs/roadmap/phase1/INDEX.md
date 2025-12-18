# Phase 1 Roadmap Index

## Status
LOCKED. Phase 1 documentation is sealed; Step 14 enforces immutability and non-regression for all prior steps (00-13). Any amendment requires a new spec with migration notes and explicit references to the locked artifacts.

## Steps
- docs/roadmap/phase1/step-00.md - Phase 1 Step 00: initiate documentation-focused phase (Status: Done).
- docs/roadmap/phase1/step-01-foundational-domain.md - Phase 1 Step 01: foundational domain baselines (Status: Done).
- docs/roadmap/phase1/step-02.md - Phase 1 Step 02: architecture guardrails, contracts, and failure patterns (Status: Done).
- docs/roadmap/phase1/step-03.md - Phase 1 Step 03: data ownership, RBAC, and audit rules (Status: Done).
- docs/roadmap/phase1/step-04.md - Phase 1 Step 04: API and integration conventions (Status: In progress).
- docs/roadmap/phase1/step-05.md - Phase 1 Step 05: UX visual language and view specifications (Status: Done).
- docs/roadmap/phase1/step-06.md - Phase 1 Step 06: UI component contracts (Status: Done).
- docs/roadmap/phase1/step-07.md - Phase 1 Step 07: UI page contracts (Status: Done).
- docs/roadmap/phase1/step-08.md - Phase 1 Step 08: Roadmap and execution sheets (Status: Proposed).
- docs/roadmap/phase1/step-09.md - Phase 1 Step 09: Inventory and equipment management (Status: Proposed).
- docs/roadmap/phase1/step-10.md - Phase 1 Step 10: Finance and accounting (Status: Proposed).
- docs/roadmap/phase1/step-11.md - Phase 1 Step 11: Cross-domain read models and integration rules (Status: Active; delivers docs/specs/18_cross_domain_read_models.md and docs/specs/19_domain_integration_rules.md).
- docs/roadmap/phase1/step-12.md - Phase 1 Step 12: Locations and maps contracts (Status: Proposed).
- docs/roadmap/phase1/step-13-notifications-and-messaging.md - Phase 1 Step 13: Notifications and messaging contracts (Status: Proposed).
- docs/roadmap/phase1/step-14.md - Phase 1 Step 14: Global lock and non-regression charter (Status: Locked; seals Phase 1 scope and establishes amendment path).
- docs/roadmap/phase1/step-15.md - Phase 1 Step 15: UI component contracts (Status: Done; reconciled registration to align numbering).
- docs/roadmap/phase1/step-16.md - Phase 1 Step 16: UI page contracts for planning, mission, collaborator, and project surfaces (Status: Done; resumes numbering without renumbering prior artifacts).
- docs/roadmap/phase1/step-17.md - Phase 1 Step 17: Domain object contracts (Status: Proposed).
- docs/roadmap/phase1/step-18.md - Phase 1 Step 18: Planning rules and constraints contract (Status: Proposed).
- docs/roadmap/phase1/step-19.md - Phase 1 Step 19: State machines and lifecycles (Status: Proposed).
- docs/roadmap/phase1/step-20.md - Phase 1 Step 20: Permissions and responsibility matrix (Status: Proposed).
- docs/roadmap/phase1/diagram.md - Phase 1 diagram showing locked and proposed steps.

## Notes
- Step 14 lock: statuses listed above are historical; all artifacts are sealed and any update requires a Step 14 amendment with migration notes.
- Phase 1 prohibits backend, frontend, and infrastructure code changes; scope is limited to documentation artifacts unless amended through Step 14 rules.
- Step 02 depends on foundational domain documentation outcomes from Step 01 (glossary, domain model, project/mission model).
- Step 03 depends on Step 01 for terminology and Step 02 for architecture and contract guardrails.
- Step 04 depends on Steps 02 and 03 to align API contracts with architecture, ownership, RBAC, and audit invariants.
- Step 05 depends on Step 04 outputs for API alignment and keeps UX surfaces consistent with visual language rules.
- Step 06 depends on Step 05 visual language decisions to keep component contracts consistent across views.
- Step 07 assembles the approved Step 06 components under Step 04 conventions and the page contract rules in docs/specs/16_ui_page_contracts.md.
- Step 08 captures operational roadmap execution artifacts and relies on Steps 02-04 for ownership, RBAC, audit, and API conventions.
- Step 09 documents equipment catalog, availability, and conflict rules bound to organization/project scopes under Steps 02-04 constraints.
- Step 10 records finance and accounting contracts aligned to ownership, RBAC, audit, identifier, and API conventions defined in Steps 02-04.
- Step 14 locks the entire Phase 1 roadmap and requires formal amendment specs for any changes to the sealed artifacts.
- Step 15 registers the validated UI component contracts without renumbering earlier artifacts and anchors the numbering sequence after the Step 07 registration gap.
- Step 16 assembles the validated components into page contracts and continues the roadmap numbering for subsequent steps.
