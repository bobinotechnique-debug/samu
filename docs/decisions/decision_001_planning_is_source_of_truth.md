# Decision 001 - Planning Is the Source of Truth

Status: LOCKED
Date: 2025-12-19

## Problem statement
Operational planning drifts when administrative artifacts (contracts, invoices, payroll events) are treated as preconditions. Teams need a single authoritative object that reflects how work is scheduled and performed, regardless of missing paperwork or delayed approvals.

## Observed reality (field-based reasoning)
- Missions start and shift before contracts are fully executed.
- Assignments can be valid and in-flight while payroll or invoicing lags.
- Acceptation signals intent and risk posture but rarely blocks execution.
- Execution sites and collaborators adapt in real time; administrative updates follow later.

## Explicit decision
Planning objects are the sole source of truth for what must happen, is happening, or has happened. Administrative artifacts may inform risk but never overrule or gate planning states.

## What this decision ENABLES
- Teams can create and adjust missions and assignments immediately, even without contracts or payroll setup.
- Risk signals surface missing administrative steps without preventing scheduling or execution.
- Historical planning timelines anchor audits and downstream reconciliation.

## What this decision FORBIDS
- Blocking or cancelling planning events because a contract, invoice, or payroll record is absent or late.
- Overwriting planning timelines to match administrative dates instead of operational reality.
- Treating acceptation or contract status as the authoritative indicator of execution.

## Consequences
### Domain model
- Planning entities (project, mission, assignment) remain primary; administrative entities are secondary projections.
- Assignments persist and remain valid even when no contract exists or when acceptation is pending.
- State transitions prioritize operational updates; administrative states attach as annotations and alerts.

### UX and planning surfaces
- Planning views allow creation and edits without contract prerequisites.
- UI highlights risk badges for missing contracts, acceptation, or payroll linkage but never disables planning actions.
- History and audit trails display planning changes as the canonical timeline; admin events appear as non-blocking context.

### Notifications and acceptation
- Notifications escalate missing contracts or acceptation as risk, not blockers.
- Acceptation updates adjust risk posture but do not alter planning states retroactively.
- Alerts include remediation guidance while preserving the planned schedule.

### Contracts, payroll, invoicing
- Contracts, payroll, and invoicing consume planning data; they cannot dictate planning existence or timing.
- Reconciliation flows align administrative records to the planning timeline instead of reshaping planning.
- Cost accrual and billing derive from planning states, with adjustments recorded as administrative deltas.

## Anti-drift rules (hard constraints)
- No workflow may block planning creation or edits due to missing administrative artifacts.
- Planning timestamps are immutable once published; corrections are additive with explicit rationale.
- Administrative systems must consume planning as-is and emit alerts when misaligned, never overwrite.

## Non-goals
- Defining contract lifecycle automation.
- Automating payroll or invoicing generation.
- Expanding HR policies beyond the planning scope.
