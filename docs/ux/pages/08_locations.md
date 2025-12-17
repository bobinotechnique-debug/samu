# Locations Page Contract (Phase 1 Step 12)

## 1. Overview
- Name: Locations
- Goal: Provide a read-only catalog of venues, sites, and rooms with map-aware context for planning, inventory, and finance visibility.
- Primary actors: planners, operations coordinators, finance analysts, viewers with project access.

## 2. URL and deep links
- Canonical route: /locations
- Query params: organization_id (required), project_id (optional for project-scoped filtering), location_id (selection), status, capacity_range, hazard_flag, accessibility_flag, cursor, page_size, sort.
- Anchor rules: Anchors remain stable for #header, #filters, #list, #details, #map-summary.

## 3. Regions and required components
- Header: title, organization/project context badges, breadcrumb back to Planning.
- Filters: filter bar for status, hazard, accessibility, capacity range, and text search over name/address.
- List: data table of venues/sites/rooms with status badges and capacity indicators.
- Details: side panel showing location attributes, hierarchy path, time zone, and audit summary; read-only map summary block uses coordinates without rendering live maps.
- Map summary: static projection card listing coordinates and map_reference strings; no embedded maps or routing controls.

## 4. Data model bindings
- Required API endpoints (read-only):
  - GET /api/v1/organizations/{organization_id}/locations?status&hazard_flag&accessibility_flag&capacity_range&cursor&page_size&sort
  - GET /api/v1/organizations/{organization_id}/locations/{location_id}
- Filters/sort/pagination mapping: filter bar maps to query params; data table uses cursor pagination per docs/specs/10_api_conventions.md; sort defaults to name asc, stable across hierarchy.
- Identifier rules: location_id and organization_id required on all requests; project_id filters must not bypass organization scope; hierarchy references (venue_id/site_id/room_id) are opaque and immutable.
- Time zone handling: location time_zone displayed as provided; no automatic conversion in the UI.

## 5. UI states
- Loading: skeleton rows in list; details panel shows loading placeholders; map summary shows loading text, not tiles.
- Empty: clear empty state with guidance to adjust filters; optional call to invite admins to register locations (link only, no mutation in Phase 1).
- Partial data: list loads while details fail or vice versa; render available data with inline warning banner.
- Error: surface API error codes using docs/specs/11_api_error_model.md mapping; retries are manual.
- Permission denied: show explicit denial message; hide list contents but retain header and filters with disabled controls.

## 6. Interactions
- Selection model: clicking a list row loads details panel and updates location_id query param; selection preserved on pagination.
- Hierarchy traversal: details panel displays parent/child references; navigation uses selection, not additional fetch patterns.
- Clipboard: copy coordinates/map_reference text; no share links that embed provider URLs or keys.
- Accessibility: tab order header -> filters -> list -> details -> map summary; all controls keyboard navigable.

## 7. RBAC and ownership
- View: users with organization-level location_view permission per docs/specs/08_rbac_model.md; optional project filter requires project view permission.
- Redaction: if viewer lacks permission for finance overlays, cost_center and tax_region are hidden; hazard notes remain visible for safety.
- No edit: all mutation controls disabled or absent in Phase 1; tooltips indicate read-only scope.

## 8. Audit and traceability
- Page load and filter changes emit view events with organization_id, project_id, and correlation_id when provided by backend.
- Selection changes include location_id, hierarchy path, and observed_at when available.
- No mutations emitted; audit references displayed from read-only payloads (created_at, updated_at, actor_id, source_system).

## 9. Forbidden patterns
- No live map rendering, tiles, or external provider embeds.
- No routing, ETA calculation, or proximity sorting.
- No cross-organization blending of results; organization_id filter is mandatory and enforced client-side and server-side.
- No client-side identifier generation or hierarchy reshaping.
