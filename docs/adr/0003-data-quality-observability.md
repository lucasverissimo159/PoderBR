# ADR 0003: Data Quality and Observability

## Status
Accepted

## Context
PoderBR relies on downstream calculations based on public data sources (IBGE, CEPEA). These sources can suffer from schema drift, delayed publishing, or temporary anomalies. Historically, data quality is an implicit hope; we need to make it an observable product capability.

The challenge is to handle anomalies without destroying the fundamental statistical premise of the platform (no silent interpolations, no destructive auto-deletion of valid but surprising data).

## Decision
We will implement an explicit **Data Quality Observability Layer**.

### 1. Non-Destructive Quality Checks
We will implement a `QualityService` that evaluates the state of the database and generates a `ValidationReport`. This service will run heuristic checks:
- **Freshness**: Flag if the latest normalized price or income is older than a configurable threshold (e.g., 45 days, considering public data lags).
- **Anomalies**: Detect Month-over-Month (MoM) spikes greater than 50% in any specific protein.
- **Completeness**: Ensure all expected regions (`BR`, `SP`) have recent ingestion runs.

Crucially, **we will not delete data** that triggers these checks. We simply flag them in a transparent JSON report.

### 2. Operational Thresholds
- **Spike Threshold**: > 50% absolute change month-over-month. (Meat prices can fluctuate, but a 50% jump in 30 days warrants an observable warning).
- **Staleness Threshold**: > 45 days without a successful `IngestionRun`.

### 3. API & Frontend Integration
We will expose `/api/v1/quality/status` which returns the `ValidationReport` and the status of the latest `IngestionRuns`.
The Frontend will consume this and surface a non-intrusive warning badge within the `MethodologyDisclosure` component if the data is deemed stale or anomalous, ensuring users understand the current limitations of the platform.

## Consequences
- **Positive**: We move from implicit trust to explicit observability. The platform self-reports its health.
- **Negative**: Adds overhead to the backend processing. A full historical scan for anomalies is expensive, so anomaly checks will be restricted to the trailing 3-6 months.
