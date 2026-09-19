# Observability & Data Quality

Data quality in PoderBR is treated as a core product feature. Given our reliance on upstream government and academic data APIs, missing periods, schema drift, and price anomalies are expected operational realities.

## Principles
1. **Non-Destructive Operations:** We never automatically delete data that looks strange. Anomalous data is flagged for human review via the `QualityService` but remains available to the Analytics Engine.
2. **Explicit Uncertainty:** The UI communicates upstream data issues directly to the user (e.g., via the Methodology Disclosure panel).

## QualityService Heuristics

The `QualityService` (`app/services/quality.py`) generates a `ValidationReport` using the following heuristics:

- **Staleness:** Is the most recent `NormalizedPrice` older than 45 days? If so, flag as a `warning`. Public APIs generally have a 30-day lag; going beyond 45 days usually indicates a broken ingestion adapter.
- **Anomalies (Price Spikes):** We analyze the trailing 6 months of data for every item. If any item shows an absolute Month-over-Month (MoM) price change greater than 50%, we raise a `warning`. This check is performed using standard dictionary-based math to keep the service lightweight.
- **Completeness:** If the database contains *zero* normalized prices, or if an ingestion adapter's latest run ended in a `failed` state, we raise a `critical` flag.

## API Exposure
These heuristics are continuously available at `/api/v1/quality/status`.

## Structured Logging
Python's standard `logging` is routed through `python-json-logger`. This ensures that logs emitted in production environments are strictly structured, parseable by standard aggregation tools (Datadog, Kibana), and prevents multi-line traceback interleaving.
