# Agent Error Log

## Summary
Every Codex failure must be logged exactly once using the required template. Entries should remain concise and actionable while mapping back to roadmap steps.

## How to add an entry
1. Confirm the failure is not already logged for the same context.
2. Copy the entry template below into the log, filling every field.
3. Keep content ASCII-only to satisfy guard enforcement.

## Entry template
- Date: YYYY-MM-DD
- Context (step ref): roadmap reference such as docs/roadmap/phase0/step-01-harden-bootstrap
- Symptom: concise description of the observed failure
- Root cause: analysis of why the failure occurred
- Fix: remediation applied to resolve the issue
- Prevention: guard, documentation, or process update to avoid recurrence
- Files touched: list of files modified during remediation

## Known Failure Patterns
- Missing roadmap linkage before implementation.
- Guard scripts not invoked prior to commits.
- Non-ASCII characters introduced into tracked files.
