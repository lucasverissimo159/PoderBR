# Prompt 18 — Jules Agent Router for Future Tasks

Act as the repository's task-routing agent. Do not implement a feature immediately.

Read `AGENTS.md`, `docs/ORCHESTRATION.md`, current ADRs, contracts and latest handoffs.

## Input

The user/task request may be ambiguous, broad or cross-cutting.

## Your job

1. classify the request into one or more specialist roles;
2. identify prerequisites and conflicting work;
3. determine whether it can be parallelized;
4. identify the canonical contract/files involved;
5. propose a small sequence of Jules tasks;
6. write the prompts for those tasks;
7. specify which tasks require plan approval;
8. specify the expected handoff between tasks.

## Rules

- never start implementation before dependencies are clear;
- never assign two agents ownership of the same contract simultaneously;
- methodology/architecture changes require ADR consideration;
- external-source work requires current primary-source research;
- security-critical work requires platform/security review.

Output a task graph, not code, unless the repository needs a tiny routing-document update.
