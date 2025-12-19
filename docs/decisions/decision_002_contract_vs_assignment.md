# Decision 002 — Contract vs Assignment

Status: LOCKED
Date: 2025-12-19

## Problem statement
Teams conflate assignments with contracts, causing planning to stall when paperwork is incomplete. The product needs clear separation so missions and assignments proceed on operational timelines while contracts capture legal commitments.

## Options considered
1) Treat assignments as valid only when linked to an executed contract. Rejected: contradicts operational reality, blocks planning, and hides risk instead of surfacing it.
2) Allow assignments to exist independently, with contracts linked when available and risk signaled through alerts. Accepted: aligns with real-world execution and preserves planning continuity.

## Final decision
Assignments are independent planning objects. Contracts may link to assignments to record legal and financial terms, but their absence never prevents assignment creation or evolution.

## Canonical definitions
- Mission: A project-scoped unit of work with objectives, scope, schedule, and execution sites.
- Assignment: The planned allocation of a collaborator to a mission with role, time frame, and load. It represents operational intent and execution state.
- Contract: A legal agreement that may cover one or more assignments, defining obligations, rates, and liabilities. It is administrative, not a planning driver.

## Explicit invariants
- Every assignment belongs to exactly one project and one mission.
- An assignment may have zero or many linked contracts; lack of a contract does not invalidate the assignment.
- Acceptation status may affect risk scoring but cannot veto assignment existence.
- Administrative data can annotate assignments but cannot mutate planning states.

## Forbidden patterns
- Blocking assignment creation or updates because no contract is attached.
- Forcing a one-to-one mapping between contracts and assignments.
- Retroactively altering assignment history to align with contract signature dates.
- Embedding business logic for contracts inside planning components or UX flows.

## Consequences
### Planning write path
- Users can create and adjust assignments without contract prerequisites; the UI captures optional contract references and raises risk warnings when absent.
- Edits to assignments prioritize operational correctness; contract linkage is an additive field, not a gating check.

### Persistence model
- Assignments store planning states and identifiers independently of contract tables.
- Contract linkage uses references or join tables without enforcing existence for assignment creation.
- Audit logs record contract links as annotations; planning history remains intact and primary.

### UX flows
- Forms and editors surface contract fields as optional with inline risk cues when empty or outdated.
- Dashboards display planning status as primary; contract and acceptation signals appear as badges and callouts.
- Correction flows add or update contract links without rewriting assignment timelines.

### Notifications and alerts
- Alerts trigger when assignments lack valid contracts or when contract terms diverge from planning data, classified as risk not blockers.
- Acceptation updates adjust alert severity but do not block notifications or planning actions.
- System messages emphasize reconciliation steps rather than denial of operations.

### Cost and risk computation
- Cost estimates derive from assignment data; contract terms refine rates when present.
- Risk scoring increases when assignments lack contracts or have mismatched terms; no automatic shutdown occurs.
- Financial projections use planning as baseline with contractual adjustments layered as modifiers.

## Anti-drift rules
- No validation rule may reject a planning action due to missing contracts.
- Contract data must never overwrite planning history; corrections are additive with traceable deltas.
- Any process that couples contract and assignment identifiers must permit multiple or zero links without blocking planning writes.

## Non-goals
- Automating contract generation or e-signature workflows.
- Implementing payroll, invoicing, or payment processing logic.
- Establishing HR policies or compliance checks beyond surfacing risk and alerts.
