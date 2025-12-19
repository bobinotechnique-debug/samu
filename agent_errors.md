# Agent Error Log

Entries must follow this template. The canonical log is maintained in docs/ops/agent_errors.md.

## Required format (strict, ASCII-only)
- Date: YYYY-MM-DD
- Context (step ref): roadmap step reference (e.g., phase0/step-00-bootstrap)
- Agent: root or sub-agent name (capitalized, e.g., Backend, Frontend, DevOps, Docs)
- Symptom: sentence-case description of the observed failure
- Root cause: sentence-case description of why the failure occurred
- Fix: sentence-case remediation applied to resolve the issue
- Prevention: guard, documentation, or process update to avoid recurrence
- Files touched: comma-separated list of modified files or `none`

All field labels must appear exactly as shown. Error or event codes, when present, must be uppercase (e.g., ERR_GUARD_MISSING).
