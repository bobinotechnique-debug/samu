# Phase 1 Coherence Audit - Accounting and Contracts Extension

## Summary
Coherent. The new Accounting (docs/specs/27_comptabilite.md) and Contracts (docs/specs/28_contrats.md) specifications align with Phase 1 constraints, maintain project-centric scoping, and avoid prohibited finance/legal automation.

## Documents Reviewed
- docs/specs/INDEX.md
- specs/INDEX.md
- docs/specs/00_glossary.md
- docs/specs/01_domain_model.md
- docs/specs/02_project_mission_model.md
- docs/specs/03_multi_tenancy_and_security.md
- docs/specs/04_architecture_principles.md
- docs/specs/05_domain_contracts.md
- docs/specs/06_known_failure_patterns.md
- docs/specs/07_data_ownership.md
- docs/specs/08_rbac_model.md
- docs/specs/09_audit_and_traceability.md
- docs/specs/10_api_conventions.md
- docs/specs/13_identifiers_and_time.md
- docs/specs/17_phase1_extended_domains.md
- docs/specs/25_mission_run_sheet.md
- docs/specs/27_comptabilite.md
- docs/specs/28_contrats.md
- docs/roadmap/phase1/INDEX.md
- docs/roadmap/phase1/step-14.md
- docs/roadmap/phase1/step-10.md
- docs/roadmap/phase1/step-21-accounting-and-contracts.md

## Coherence Checks
- Organization remains the security boundary and project the functional boundary across both new specs, matching the multi-tenancy contract; no cross-organization access is introduced.
- Mandatory project linkage for invoices, bills, expenses, budget lines, payments, and all contract types upholds the rule that no planning or execution exists outside a project/mission context.
- Permissions reuse the existing RBAC roles (org_owner, org_admin, project_manager, planner, member, viewer) with default-deny evaluation, preventing role proliferation or bypass of the RBAC model.
- Audit and traceability requirements (status transitions, attachments, exports, and signature metadata) align with the Phase 1 audit contract and preserve immutable history instead of allowing deletions.
- Export scope is limited to CSV/PDF with watermarking and contextual metadata; advanced financial/legal outputs (FEC, bank sync, regulatory filings) remain explicitly out of scope, preventing conflicts with Phase 1 constraints.
- Attachment handling follows immutable, checksum-tracked storage consistent with data ownership and audit rules; archiving replaces deletion to avoid identifier reuse.
- Contract lifecycles and amendment handling maintain single active versions per project/mission, avoiding conflicts with assignment and mission models that depend on stable identifiers.
- Payment records and invoice/bill lifecycles stay documentation-only and avoid ledger logic, respecting the Phase 1 prohibition on backend/financial processing.
- Roadmap linkage is explicit through a new Phase 1 amendment step and references to the existing Step 10 finance scope, keeping navigation and governance intact.

## Follow-Ups
None identified; the specs integrate without contradiction under Phase 1 governance.
