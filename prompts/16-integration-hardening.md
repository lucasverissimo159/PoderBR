# Prompt 16 — Integration Agent: Reconcile the Whole System

Act as Integration Agent. No feature invention.

Read `AGENTS.md`, all ADRs, contracts, product/methodology documents and latest handoffs.

## Process

1. Inspect git history/current branch and diffs.
2. Check schema, migrations, source adapters, analytics, API, frontend, tests and docs as one system.
3. Find duplicate concepts, inconsistent names, units, enum values, date semantics and versions.
4. Validate that contracts match their consumers.
5. Validate methodology and provenance all the way from source to UI.
6. Fix evidence-backed inconsistencies only.
7. Update ADRs when durable decisions are required.

## Validation

Run full applicable tests, type/lint checks, build, migrations, smoke flow, quality checks and representative API/UI journeys.

Create/update `docs/RELEASE_READINESS.md` with pass/fail matrix, risks, migration notes and blockers.

Do not equate “tests green” with statistical validity.
