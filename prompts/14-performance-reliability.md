# Prompt 14 — Performance, Resilience and Cost-Aware Hardening

Act as the Performance/Reliability Agent.

Read architecture, API, data pipeline and platform context.

## Mission

Improve measurable performance/reliability without premature optimization.

## Measure first

Establish a baseline for:
- representative API latency;
- database query counts and slow queries;
- payload size;
- frontend load/render behavior;
- ingestion duration;
- cold-start/setup time.

## Research

Investigate current official guidance for query indexing, HTTP caching, client caching, timeouts, retry/backoff, circuit-breaking patterns where relevant, and browser performance.

## Implement only justified changes

Potentially:
- indexes;
- query optimization;
- response shaping;
- caching;
- timeouts;
- bounded retries;
- graceful degradation when upstream data is unavailable.

Add regression/baseline tests where practical and document measurable before/after results.
