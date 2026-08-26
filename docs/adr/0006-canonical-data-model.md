# ADR 0006: Canonical Data Model, Provenance and Idempotency

## Context
PoderBR requires a robust data engineering foundation. We need a way to store data from multiple, disparate providers (IBGE, CEPEA, Ipeadata) without coupling the analytics logic to the provider's specific schema. Furthermore, data ingestion must be repeatable (idempotent), and every analytical output must trace back to its exact source (provenance).

## Decision

We have adopted a two-tier data model:

1.  **Raw Tier (`raw_observations`)**: A provider-agnostic, narrow table that stores the exact value fetched from the source. It links to a `DataSource` and an `IngestionRun`.
2.  **Normalized Tier (`normalized_prices`, `normalized_incomes`)**: A canonical schema where prices are converted to a standard currency (BRL) and standard units (e.g., 'kg', 'dozen').

### Provenance
Every `NormalizedPrice` or `NormalizedIncome` record contains a `raw_observation_id` foreign key. This allows any piece of data shown on the frontend to be traced back through the analytics layer -> normalized layer -> raw layer -> source URL and ingestion timestamp.

### Data Maturity
We implemented an `ObservationStatus` Enum (`source_verified`, `normalized`, `estimated`, `missing`). A value that is missing from the source is explicitly recorded as `MISSING` with a `null` value in the normalized table, fulfilling the "no fabricated observations" rule.

### Idempotency
We rely on database-level `UniqueConstraint`s:
- Raw: `(source_id, reference_date, geography_id)`
- Normalized: `(item_id, reference_date, geography_id)`
If an ingestion pipeline runs twice for the same month, the database will reject the duplicate (or the pipeline must be configured to `ON CONFLICT DO UPDATE`), guaranteeing idempotency regardless of the orchestrator.

## Consequences
- Adapters (Ingestion scripts) are strictly responsible for writing to `raw_observations`. They must never write to normalized tables or analytics tables.
- A separate "Normalization Job" will read from raw and write to the normalized tables.
- This decoupling allows us to add new data providers without altering the downstream analytics logic.
