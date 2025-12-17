# Domain Interaction Contracts

## Purpose
Define explicit, testable contracts governing interactions between core domains to preserve boundaries and traceability.

## Scope
- Applies to organization, project, mission, user/collaborator, and planning domains.
- Contracts guide API design, data modeling, and documentation across agents.
- Planning is referenced for alignment but not implemented in Phase 1.

## Contract Structure
- Inputs: Required identifiers and validated fields the domain expects.
- Outputs: Authoritative data the domain emits for downstream use.
- Ownership: Agent responsible for accuracy and lifecycle.
- Forbidden Dependencies: Interactions that violate separation of concerns or security boundaries.

## Contracts

### Organization Contract
- Inputs: organization_id (required), admin actor identity, compliance profile reference.
- Outputs: organization profile, policy set (security, tenancy), audit context for downstream domains.
- Ownership: Backend Agent maintains authoritative organization data and validation; Docs Agent maintains spec accuracy.
- Forbidden Dependencies: Direct data reads from other organizations; frontend-only derivations of organization policy.

### Project Contract
- Inputs: project_id (required), organization_id (required), project charter (name, scope), owner user reference.
- Outputs: project profile, mission list reference, allowable scheduling window, organization alignment confirmation.
- Ownership: Backend Agent for data and enforcement; Docs Agent for contract currency.
- Forbidden Dependencies: Missions or plans without organization_id; cross-organization project references; frontend-originated business rules.

### Mission Contract
- Inputs: mission_id (required), project_id (required), organization_id (required), mission objective, assigned collaborators.
- Outputs: mission status, assignment list, execution constraints, linkage to project milestones.
- Ownership: Backend Agent governs mission lifecycle; Docs Agent documents scope and constraints.
- Forbidden Dependencies: Mission execution or scheduling without project_id; cross-project collaborator reuse without organization validation; infra scripts altering mission data.

### User / Collaborator Contract
- Inputs: collaborator_id (required), organization_id (required), role, availability profile, permission set.
- Outputs: validated collaborator profile, role-scoped capabilities, audit trail entries for assignments.
- Ownership: Backend Agent for identity and permissions; Docs Agent for documented expectations; Frontend Agent may render but not author rules.
- Forbidden Dependencies: Cross-organization collaborator reuse; frontend-authored permission logic; missions or plans that omit organization validation for collaborators.

### Planning Contract (Future-Facing)
- Inputs: project_id (required), organization_id (required), planning scope (missions, assignments), temporal constraints, risk inputs.
- Outputs: planning timeline draft, dependency map, risk register hook, readiness checks for mission execution.
- Ownership: Shared between Backend Agent (planning engines) and Docs Agent (spec alignment) when implemented; remains documentation-only in Phase 1.
- Forbidden Dependencies: Planning without project_id; data ingestion from other organizations; frontend-owned planning calculations; execution triggers without backend validation.

## Related Specifications
- Data ownership constraints and required identifiers are defined in docs/specs/07_data_ownership.md.
- Role and permission expectations that govern contract execution are detailed in docs/specs/08_rbac_model.md.
- Audit obligations for contract-driven events are outlined in docs/specs/09_audit_and_traceability.md.
