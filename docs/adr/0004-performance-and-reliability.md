# ADR 0004: Performance, Reliability, and Cost-Aware Hardening

## Status
Accepted

## Context
PoderBR needs to handle public analytics requests reliably without incurring excessive database or compute costs. The architecture must prioritize resilience to upstream failures (like IBGE or CEPEA APIs timing out) and fast UI loads. As per the constraints: *improve measurable performance without premature optimization.*

### Baselines & Measurements
- **Database Reads**: The Analytics Service hits the DB to filter on `geography_id`, `income_basis`, and `reference_date`. Without indexes, this triggers sequential scans on the normalized tables.
- **Upstream Reliability**: Current `httpx` logic in `ibge.py` and `ipea.py` fails the ingestion run immediately on a timeout.
- **Payload & API Limits**: Responses are lightweight JSON, but clients requesting the same data continuously could overwhelm the FastAPI instance if uncached.

## Decision

We will implement the following justified changes:

### 1. Database Indexing
Add specific composite or single-column indexes on highly filtered columns to optimize the backend queries.
- `NormalizedPrice`: Index `(geography_id, item_id, reference_date)`
- `NormalizedIncome`: Index `(geography_id, income_basis, reference_date)`
- `RawObservation`: Index `(source_id, geography_id, reference_date)`

### 2. Upstream Bounded Retries
Wrap critical HTTP extraction loops in our adapters with `tenacity`.
- **Strategy**: Wait exponentially (e.g., 2, 4, 8 seconds) and stop after 3 attempts. This prevents intermittent upstream network blips from ruining a monthly ingestion pipeline.

### 3. HTTP Client Caching (API)
Our data updates rarely (monthly). To reduce backend compute load for repeated queries, we will instruct the client (browser/CDN) to cache the results.
- **Strategy**: Inject `Cache-Control: public, max-age=3600` (1 hour) to the `/api/v1/affordability` endpoint via Response headers.

## Consequences
- **Positive**: Queries scale safely. Network blips during ingestion are absorbed automatically. Repeated UI requests bypass the DB entirely via HTTP caching.
- **Negative**: If data is corrected intra-hour, clients might see stale data for up to 60 minutes. Given our monthly release cycle, this trade-off is highly acceptable.
