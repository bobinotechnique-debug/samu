# Baseline Lock Report

## Branch and Commit
- Branch: work (main branch not present in local clone)
- Commit: a1f3141c15416b8d82d0cb1b3bfbb42351c84c82

## Guards Executed
- `python tools/guards/run_guards.py` - PASS (ASCII, agents, docs, roadmap guards)
- `pwsh PS1/guards.ps1` - NOT RUN (pwsh unavailable in container; cross-platform guards executed)

## Tests Executed
- Backend: `cd backend && pytest` - PASS (22 tests, PendingDeprecationWarning about multipart import)
- Frontend: `cd frontend && npm run test` - PASS (3 files; React Router future flag warnings only)

## CI Verification
- `.github/workflows/ci.yml` runs guards, backend linting, backend tests, and frontend tests on push and pull_request across Ubuntu, macOS, and Windows; ordering matches local execution.
- CI status for main not observable in the current environment; no local guard or test failures detected.

## Minimal Fixes Applied
- None.

## Final Status
- GREEN (guards and tests pass locally; PowerShell guard pending due to missing pwsh)
