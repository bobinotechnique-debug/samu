# Guard Framework

Phase 0 introduces guard stubs to enforce repository hygiene. All scripts are ASCII-only PowerShell files and must fail loudly on violations.

Cross-platform Python equivalents mirror each PowerShell guard to keep validation runnable on Linux, macOS, and Windows CI runners.

## Scripts
- ascii_guard.ps1 / ascii_guard.py - scans the repository for non-ASCII characters.
- docs_guard.ps1 / docs_guard.py - ensures required documentation index files are present.
- roadmap_guard.ps1 / roadmap_guard.py - validates that Phase 0 roadmap status is marked Done.
- agents_guard.ps1 / agents_guard.py - confirms sub-agent files exist and restate AGENT.md precedence.
- run_guards.py - orchestrates all Python guards for cross-platform usage.

## Usage
Run guards individually or chain them from PS1/guards.ps1. Python users can execute `python tools/guards/run_guards.py` from the repository root. Any failure blocks progress per AGENT.md stop conditions.
