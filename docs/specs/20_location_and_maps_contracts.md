# Location and Maps Contracts (Phase 1 Step 12)

## Purpose
Define authoritative, read-only contracts for locations, venues, and map references that support planning, operations, inventory, and finance without enabling routing or execution logic.

## Scope and Constraints
- Documentation only under Phase 1; no backend, frontend, infrastructure, or CI changes.
- All location records are scoped by organization_id with immutable identifiers; projects and missions reference locations by those identifiers.
- Hierarchy supports Venue -> Site -> Room/Area with optional capacity and constraint metadata.
- Geographic coordinates and address fields are descriptive only; no routing, distance calculation, or external map provider integration.
- Time zone attribution is mandatory for every location to align scheduling and finance windows.
- All contracts follow docs/specs/10_api_conventions.md, docs/specs/11_api_error_model.md, docs/specs/12_api_versioning.md, and docs/specs/13_identifiers_and_time.md.

## Core Location Model
- **Identifiers**: location_id is opaque and immutable; organization_id required on every payload; venue_id/site_id/room_id remain stable once issued.
- **Hierarchy**: Venue contains Sites; Sites contain Rooms/Areas; hierarchy is read-only and cannot be reshaped in Phase 1.
- **Attributes**: name (immutable slug + display label), description, address block (street, city, region/state, postal_code, country), coordinates (latitude, longitude), map_reference (grid or provider-agnostic link), time_zone.
- **Capacity and constraints**: capacity (people), equipment_capacity (count or volumetric note), hazard_flags (informational), accessibility_flags; these fields inform planning but cannot trigger validation logic.
- **Status**: status field indicates active, deprecated, or offline for planning visibility; deprecation does not delete identifiers.

## Planning Integration (Read-Only)
- Missions reference venue_id/site_id/room_id and organization_id; project_id is mandatory for mission bindings.
- Timeline and travel visibility consumes coordinates and time_zone as metadata only; no distance or duration calculations are allowed.
- Conflict badges may render when locations are offline or deprecated, but conflict evaluation is sourced from planning APIs, not inferred from this contract.

## Inventory Integration (Read-Only)
- Equipment storage references venue_id/site_id/room_id; storage assignments inherit organization_id and optional project_id when tied to missions.
- Transfer visibility surfaces source and destination location identifiers with observed_at timestamps; no transfer automation or routing steps are allowed.
- Hazard and accessibility flags are informational overlays for planners when staging equipment.

## Finance Integration (Read-Only)
- Location metadata can annotate cost centers or tax_region flags; Finance references organization_id and location identifiers but does not alter location data.
- Cost attribution uses location identifiers to tag expenses; no automatic accruals, billing, or tax computation occurs in Phase 1.

## Map and Coordinate Rules
- Coordinates are captured as provided and are not validated against external services; no reverse geocoding or enrichment is permitted.
- Map references are provider-agnostic strings or grid references; they must not embed API keys or signed URLs.
- Routing, turn-by-turn directions, and ETA calculations are explicitly forbidden; any projection remains descriptive only.

## Immutability and Ownership
- Location identifiers are immutable once issued; renames preserve identifiers and audit history while keeping prior labels discoverable.
- Organization ownership forbids cross-organization visibility; sharing or aggregating locations across organizations is not allowed.
- Updates to capacity or status are versioned changes recorded through append-only history; deletion is prohibited in Phase 1.

## Audit and Time Rules
- All payloads include created_at, updated_at, and observed_at timestamps in UTC ISO 8601; time_zone reflects the physical location for scheduling context.
- Audit references follow docs/specs/09_audit_and_traceability.md with actor_id, correlation_id, and source_system when applicable.
- No client-generated identifiers are accepted; servers issue opaque ids and enforce organization_id on every API entry point.

## Forbidden Patterns
- No live map rendering, embedded map widgets, or tile downloads within this contract.
- No routing, pathfinding, geofencing, or proximity calculations.
- No external provider dependencies (Google Maps, Mapbox, OpenStreetMap APIs) during Phase 1.
- No silent mutation of location records through planning, inventory, or finance flows; all use is read-only.
