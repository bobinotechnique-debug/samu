# Phase 1 - Step 12: Locations and Maps Contracts (Proposed)

## Purpose
Define authoritative location and map reference contracts that enable planning, operations, inventory, and finance to share consistent location metadata without activating routing or live mapping.

## Scope
- Documentation only; no backend, frontend, infrastructure, or CI modifications.
- Location hierarchy (venue, site, room/area) with immutable identifiers scoped by organization_id.
- Address normalization, coordinates, time zone attribution, and descriptive map references.
- Read-only projections for planning visibility, inventory storage, and finance attribution.
- Index updates and roadmap registration for Step 12 outputs.

## Assumptions
- All locations are scoped by organization_id with opaque identifiers.
- Projects and missions reference locations by immutable identifiers; hierarchy is read-only in Phase 1.
- No external map provider integration or geospatial computation during Phase 1.

## Exclusions
- Live map rendering, routing engines, distance calculations, or geofencing.
- External API integrations for maps or geocoding.
- Any mutation flows for locations in Phase 1.

## Objective
Publish location and maps documentation that aligns with Phase 1 API conventions and ownership rules while keeping location usage read-only across domains.

## Deliverables
- docs/specs/20_location_and_maps_contracts.md covering identifiers, hierarchy, address/coordinate fields, and forbidden routing patterns.
- docs/ux/pages/08_locations.md defining the read-only Locations page contract.
- Updated indexes: docs/specs/INDEX.md, specs/INDEX.md, docs/ux/pages/INDEX.md, docs/roadmap/phase1/INDEX.md, docs/roadmap/INDEX.md.

## Acceptance Criteria
- Location contracts define identifiers, hierarchy, immutability, and organization ownership rules.
- Map-related fields are descriptive only and forbid routing or distance calculations.
- All references align with Phase 1 API conventions, identifier/time rules, and ownership guardrails.
- Documentation is ASCII-only, indexed, and contains no TODO placeholders.

## Dependencies
- Step 04 API conventions.
- Step 07 UI page contracts.
- Steps 08-11 extended domain and integration contracts.
