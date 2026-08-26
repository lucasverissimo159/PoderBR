# Prompt 06 — Public Data Adapters and Repeatable Ingestion

Act as the Data Ingestion Agent.

Read the latest source ADR, data contracts, data dictionary and provider documentation.

## Mission

Implement the first production-grade adapters for the selected sources.

## Research

Verify the most stable official API/download endpoint available. Inspect schema semantics, pagination, limits, revisions and terms. Do not choose scraping when a supported machine-readable source exists.

## Implement

Each adapter must:
- be isolated from canonical domain code;
- normalize provider-specific fields;
- validate geography/date/unit/frequency;
- capture provenance;
- be idempotent;
- support bounded retries where justified;
- expose dry-run/validation capability if practical;
- fail loudly on schema drift;
- preserve reproducibility where legally allowed.

Use fixtures/mocks in CI. Do not make test success depend on live APIs.

## Runbook

Document how an operator executes an ingestion, what happens when a provider is unavailable, how to inspect a failed run and how a source revision is handled.

Update data-source documentation and handoff.
