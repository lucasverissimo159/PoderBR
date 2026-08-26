# Prompt 11 — Systematic QA, Contracts and Failure Injection

Act as the QA Agent and assume other agents believe the system is finished. Challenge that belief.

Read `AGENTS.md`, acceptance criteria, all contracts, methodology and QA context.

## Research

Investigate practical use of:
- property-based tests;
- contract tests;
- deterministic fixtures;
- database integration tests;
- Playwright end-to-end tests;
- mutation/fault injection where useful;
- accessibility automation.

Only adopt techniques whose maintenance cost is justified.

## Test matrix

Cover:
- calculations;
- unit conversion;
- missing/estimated data;
- partial geography;
- upstream schema drift;
- repeated ingestion;
- migration compatibility;
- date boundaries/timezones;
- API validation;
- frontend loading/error states;
- accessibility basics;
- security-sensitive input paths.

## Failure injection

Break fixtures or provider response shapes intentionally and verify deterministic, diagnostic failure instead of silent corruption.

Produce a test plan, automated tests, CI commands, defects and handoff.
