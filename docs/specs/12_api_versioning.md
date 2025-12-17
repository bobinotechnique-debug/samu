# API Versioning and Compatibility

## Purpose
Define the versioning strategy and compatibility rules that govern API evolution and prevent breaking changes without controlled rollout.

## Scope
- Applies to all HTTP APIs exposed under /api/{version}/.
- Covers version identifiers, backward compatibility expectations, deprecation process, forbidden breaking changes, and minimum support windows.
- Binding for backend and frontend changes in future phases.

## Assumptions
- Version v1 is the initial stable contract for Phase 1 outputs.
- Error codes and conventions defined in related specs are part of the public contract.
- Phase 1 produces documentation only; implementation will comply in later steps.

## Exclusions
- SDK-specific versioning schemes.
- Feature flag rollout mechanics or AB testing strategies.
- Database migration strategies; only API surface compatibility is addressed here.

## Versioning Strategy
- API versions MUST be encoded in the URI as /api/v{major}/ (e.g., /api/v1/projects).
- Major versions MUST increment only when backward-incompatible changes are introduced and approved through the deprecation process.
- Minor or patch adjustments that remain backward compatible MUST NOT change the URI version; they MUST be documented in changelogs and communicated to clients.

## Backward Compatibility Rules
- Within a major version, existing endpoints, fields, error codes, and behaviors MUST remain backward compatible.
- Additive changes (new optional fields, new resources, new error codes) MUST NOT break existing clients and MUST default to safe behavior.
- Field removals, type changes, or behavior changes that alter semantics within a major version are forbidden.

## Deprecation Process
- Deprecating any endpoint, field, or error code MUST include a public notice, target removal date, and migration guidance.
- Deprecation notices MUST be recorded in release notes and relevant documentation, referencing the affected version.
- Removal of deprecated elements MUST coincide with a new major version; silent removals are forbidden.

## Forbidden Breaking Changes
- Changing response shapes, renaming fields, or altering identifier formats within the same major version is forbidden.
- Modifying authentication flows, token formats, or required headers without a new major version is forbidden.
- Altering error envelope structure or existing error codes within a major version is forbidden.

## Minimum Support Window
- Each stable major version MUST be supported for at least 12 months after the next major version is released, unless a security emergency requires earlier retirement with documented justification.
- Critical security fixes MUST be backported to all supported major versions until their support window closes.
- Clients MUST be provided with migration guides and timelines before support is withdrawn.
