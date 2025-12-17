# Guard Framework

Phase 0 introduces guard stubs to enforce repository hygiene. All scripts are ASCII-only PowerShell files and must fail loudly on violations.

## Scripts
- ascii_guard.ps1 - scans the repository for non-ASCII characters.
- docs_guard.ps1 - ensures required documentation index files are present.
- roadmap_guard.ps1 - validates that Phase 0 roadmap status is marked Done.
- agents_guard.ps1 - confirms sub-agent files exist and restate AGENT.md precedence.

## Usage
Run guards individually or chain them from PS1/guards.ps1. Any failure blocks progress per AGENT.md stop conditions.
