# Agent Error Log

## Summary
Every Codex failure must be logged exactly once using the required template. Entries should remain concise and actionable while mapping back to roadmap steps.

## How to add an entry
1. Confirm the failure is not already logged for the same context.
2. Copy the entry template below into the log, filling every field.
3. Keep content ASCII-only to satisfy guard enforcement.

## Entry template (strict, ASCII-only)
- Date: YYYY-MM-DD
- Context (step ref): roadmap reference such as phase0/step-01-harden-bootstrap
- Agent: root or sub-agent name (capitalized, e.g., Backend, Frontend, DevOps, Docs)
- Symptom: sentence-case description of the observed failure
- Root cause: sentence-case description of why the failure occurred
- Fix: sentence-case remediation applied to resolve the issue
- Prevention: guard, documentation, or process update to avoid recurrence
- Files touched: comma-separated list of files modified during remediation or `none`

All field labels must appear exactly as shown. Error or event codes, when present, must be uppercase (e.g., ERR_GUARD_MISSING).

## Known Failure Patterns
- Missing roadmap linkage before implementation.
- Guard scripts not invoked prior to commits.
- Non-ASCII characters introduced into tracked files.
