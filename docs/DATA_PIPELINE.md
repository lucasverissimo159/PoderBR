# Data Pipeline

The data ingestion pipeline for PoderBR is designed to be idempotent, resilient, and distinct from the synchronous API serving layer.

## The Ingestion Architecture

```text
External API ──► Fetch (httpx + tenacity) ──► Yield Raw Dicts ──► Upsert to raw_observations
```

### 1. Base Adapter Pattern
All ingestion sources (IBGE, CEPEA, Ipeadata) inherit from `app.ingestion.base.BaseAdapter`. The base adapter handles:
- Upserting the `DataSource` registry metadata.
- Generating a UUID tracking `IngestionRun`.
- Wrapping the ingestion loop in a database transaction.
- Safely handling errors without polluting the database with partial states.

### 2. Idempotency Constraints
We use `ON CONFLICT DO UPDATE` (SQLite) or `INSERT ... ON CONFLICT` (Postgres) within the database logic.
A `UniqueConstraint` on `(source_id, reference_date, geography_id)` guarantees that re-running an ingestion script for past dates will simply update the existing observation rather than duplicating it.

### 3. Resilience
External public APIs are notoriously flaky.
We wrap our extraction requests with `tenacity`, applying bounded exponential backoffs. If a timeout occurs, it retries 3 times before failing the `IngestionRun` deterministically.

### 4. Normalization Separation
The pipeline only writes to `raw_observations`. A separate normalization process maps `raw_observations` to `normalized_prices` and `normalized_incomes`, translating complex source codes (like IBGE's variable 12384) into standard Domain identifiers (like `average_income`).
