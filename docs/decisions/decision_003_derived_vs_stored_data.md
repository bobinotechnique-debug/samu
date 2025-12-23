# Decision 003 - Derived vs Stored Data

Status: SEALED
Date: 2025-12-24

## Rules
- Stored data is the only source of truth; derived data never drives validation, authorization, or lifecycle decisions.
- Derived data is recomputed from stored facts; cached projections must document inputs and invalidation rules.
- Recomputations are valid whenever any input fact changes or when requested by audit; recomputation must not mutate stored facts.
- API responses may include derived fields computed at read time or served from validated caches; write paths accept only stored facts.

## Data classification
- Stored: organization, project, mission, assignment identifiers and relationships.
- Stored: assignment planned and actual dates, roles, capacity/load, status history, and execution sites.
- Stored: contract identifiers, parties, currency, validity windows, and signed rate tables.
- Derived: planned cost (capacity/load * rate), forecasted burn, and risk scores unless explicitly sealed by a signed contract.
- Derived: availability holds calculated from assignments and collaborator calendars.
- Derived: notification readiness (who to notify, channel readiness) built from stored assignments, collaborators, and contracts.
- Derived: SLA or deadline risk bands calculated from stored deadlines and current acceptance state.

## API impact
- Write endpoints accept stored fields only; derived fields are ignored on input.
- Read endpoints may return derived fields with clear labeling and must include the stored fields they depend on.
- Cached derived responses must include the timestamp and input version used for computation.

## Derived vs stored table
| Data | Derived/Stored | Source of Truth | Recomputable | Notes |
| --- | --- | --- | --- | --- |
| Assignment planned dates | Stored | Assignment record | N/A | Planning timeline anchor. |
| Assignment role and load | Stored | Assignment record | N/A | Defines operational commitment. |
| Contract rate table | Stored | Contract record | N/A | Immutable once signed. |
| Planned cost | Derived | Assignment + contract rate | Yes | Recompute on rate, load, or schedule change. |
| Forecasted burn | Derived | Assignment status + time tracking | Yes | Recompute on status or time entry change. |
| Availability hold | Derived | Assignment + collaborator calendar | Yes | Recompute on assignment or calendar change. |
| Notification readiness | Derived | Assignment + collaborator contact data | Yes | Recompute on contact or acceptance requirement change. |
| SLA risk band | Derived | Assignment deadline + acceptance state | Yes | Recompute on deadline or state change. |
| Risk score | Derived | Planning + contract linkage + acceptance state | Yes | Recompute on any input change. |

## Decision Status
SEALED - blocking for persistence, caching, and API responses
