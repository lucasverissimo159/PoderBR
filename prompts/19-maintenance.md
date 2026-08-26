# Prompt 19 — Long-Term Maintenance and Evidence-Driven Evolution

Act as the long-term maintenance agent.

Read `AGENTS.md`, current ADRs, contracts, quality reports and latest handoffs.

## Objective

Find one high-value bounded improvement in:
- data correctness;
- technical debt;
- developer experience;
- observability;
- accessibility;
- reliability;
- performance;
- documentation.

## Research

For framework/dependency/API/security issues, consult current official docs before changing code.

## Constraints

- one bounded objective;
- no broad cleanup;
- regression test for defects;
- update contracts/docs when behavior changes;
- ADR before architecture changes.

## Output

State evidence, proposed change, alternatives considered, expected impact, tests, rollout/rollback considerations and follow-up task.
