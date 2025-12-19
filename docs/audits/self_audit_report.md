# Codex Self Audit Report

## Summary

* Overall status: MINOR_GAPS

## Verified Areas

* Roadmap indexes cover Phase 0 through Phase 2 with explicit step listings and lock notes, keeping deliverables traceable to numbered steps.【F:docs/roadmap/INDEX.md†L8-L52】
* Agent governance defines precedence, operating cycle, data ownership boundaries, and explicit global stop conditions for non-compliant work.【F:AGENT.md†L61-L149】
* Assignment engagement rules preserve project/org scoping, treat assignments as the atomic cost unit, and gate contract generation on acceptance with idempotent processing safeguards.【F:docs/specs/33_assignment_engagement_states.md†L15-L64】【F:docs/specs/35_contract_generation_pipeline.md†L7-L39】
* Notification and acceptance flows are documented as non-legal, non-blocking signals with forbidden irreversible side effects, aligning with auditability requirements.【F:docs/specs/34_notifications_and_acceptance.md†L7-L50】

## Detected Gaps

* GAP-01  
  Description: Two Phase 1 coherence audits (mission run sheet integration and accounting/contracts amendment) exist but are not registered in specs indexes, leaving them orphaned from navigation and guard coverage.  
  Impact: MEDIUM  
  Affected documents: docs/specs/phase1_coherence_audit.md; docs/specs/phase1_coherence_audit_compta_contrats.md; docs/specs/INDEX.md; specs/INDEX.md.【F:docs/specs/phase1_coherence_audit.md†L1-L34】【F:docs/specs/phase1_coherence_audit_compta_contrats.md†L1-L41】【F:docs/specs/INDEX.md†L40-L60】【F:specs/INDEX.md†L38-L59】

* GAP-02  
  Description: Specification numbering collides between Phase 1 (20_location_and_maps_contracts, 21_notifications_and_messaging_contracts) and Phase 2 architecture specs (20_architecture_HLD, 21_architecture_LLD), creating ambiguity when mapping requirements to roadmap steps and changelog entries.  
  Impact: MEDIUM  
  Affected documents: docs/specs/INDEX.md; specs/INDEX.md; docs/specs/20_location_and_maps_contracts.md; docs/specs/20_architecture_HLD.md; docs/specs/21_notifications_and_messaging_contracts.md; docs/specs/21_architecture_LLD.md.【F:docs/specs/INDEX.md†L30-L60】【F:specs/INDEX.md†L28-L59】

## Contradictions

* CT-01  
  Conflicting documents: docs/specs/30_contract_assignment_link.md vs. docs/specs/33_assignment_engagement_states.md  
  Explanation: Spec 30 allows a single contract to reference multiple assignments within a project, while Spec 33 defines the assignment as the atomic cost unit with contracts binding to assignment_id, creating ambiguity on whether contracts must stay one-to-one with assignments for costing and audit trails.【F:docs/specs/30_contract_assignment_link.md†L8-L20】【F:docs/specs/33_assignment_engagement_states.md†L15-L38】

* CT-02  
  Conflicting documents: docs/specs/28_contrats.md vs. docs/specs/35_contract_generation_pipeline.md  
  Explanation: The contracts spec permits draft contract generation from templates without acceptance prerequisites, whereas the pipeline spec forbids contract generation before explicit acceptance, leaving the pre-acceptance draft workflow undefined and potentially non-compliant.【F:docs/specs/28_contrats.md†L30-L49】【F:docs/specs/35_contract_generation_pipeline.md†L7-L38】

## Recommended Fixes

1. Register all existing Phase 1 coherence audits in docs/specs/INDEX.md and specs/INDEX.md under the Step 14 amendment path to restore navigation and guard coverage (map to Phase 1 Step 14).  
2. Disambiguate spec numbering between Phase 1 and Phase 2 by adding phase/step qualifiers or renumbering the later-phase architecture specs in indexes (map to Phase 2 Steps 01-02).  
3. Align contract-to-assignment semantics by clarifying whether contracts must stay one-to-one with assignments and by defining whether pre-acceptance draft generation is allowed or moved post-acceptance (map to Phase 1 Step 22 and Phase 2 Step 21).

## Stop Conditions

Codex may continue after tracking the listed gaps; no blocking issues detected that require an immediate STOP under AGENT.md.
