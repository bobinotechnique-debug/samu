# Agents Contract Audit (2026-01-13)

## Purpose
Audit AGENT.md and agents/* for authority clarity, scope enforcement, stop conditions, output contracts, and error capitalization. All proposals below are diff-ready and implemented where noted.

## Findings
- Authority clarity: Sub-agent files lacked explicit escalation to the Docs Agent and root AGENT.md; added explicit precedence language across all agents.
- Scope enforcement: Agents were missing self-audit checkpoints to enforce scope and roadmap linkage; new Self Audit sections standardize the requirement.
- Stop conditions: Root stop conditions now restated with ASCII-only emphasis and roadmap linkage checks in each agent.
- Output contracts: Added explicit output contracts detailing roadmap references, index updates, changelog updates, and error logging rules.
- Error capitalization: agent_errors templates now enforce uppercase error/event codes and sentence-case narrative fields.

## Applied Diffs (textual)
- AGENT.md: bumped to 2.5.1, added Docs Agent escalation note, and introduced Section 20 Self Audit and Output Contract.
- agents/backend.md: added Authority and Precedence, Output Contract, and Self Audit sections; reinforced ASCII and roadmap rules.
- agents/frontend.md: added Authority and Precedence, Output Contract, and Self Audit sections; reinforced ASCII and roadmap rules.
- agents/devops.md: added Authority and Precedence, Output Contract, and Self Audit sections; reinforced ASCII and roadmap rules.
- agents/docs.md: added Authority and Precedence, Output Contract, and Self Audit sections; reinforced ASCII and roadmap rules.
- agent_errors.md and docs/ops/agent_errors.md: hardened strict template ordering, capitalization expectations, and uppercase error/event code rule.

## Residual Ambiguities
- None detected; authority and escalation paths are explicit, and stop/output contracts are standardized.

## Self Audit
- Roadmap linkage: documentation-only update aligned with phase0/step-00-bootstrap baseline.
- ASCII compliance: all content is ASCII-only.
- Scope alignment: confined to agent contracts and error logging documentation; no business logic or roadmap content modified.
- Outputs produced: updated AGENT.md version, agent contracts, error templates, and this audit record; CHANGELOG entry added.
