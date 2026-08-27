# Handoff: Data Ingestion Phase

## Objective
Implement production-grade ingestion adapters for IBGE SIDRA and Ipeadata to populate the canonical data model, ensuring idempotency, schema validation, and strict provenance tracking.

## Decisions Made
- **Adapter Interface:** Created a `BaseAdapter` class that forces all adapters to declare their source metadata, track execution in `IngestionRun`, and use an upsert strategy (`ON CONFLICT DO UPDATE`) to guarantee idempotency.
- **Provider Isolation:** HTTP requesting and parsing logic is strictly isolated in `app/ingestion/`. The models from `app/models/core.py` are the only boundary crossed.
- **Mocking CEPEA:** Due to the lack of a stable API for CEPEA, a `CepeaMockAdapter` was implemented to fulfill the interface requirements and demonstrate the pattern without introducing fragile web scraping to the MVP.
- **CLI Runner:** Developed `scripts/ingest.py` with an explicit `--dry-run` flag to safely validate schema drift before applying database writes.

## Evidence/Sources
- Ipeadata OData v4 JSON structures.
- IBGE SIDRA v3 API documentation.
- ADR 0006: Canonical Data Model.

## Files Created/Changed
- `app/ingestion/base.py`, `app/ingestion/ibge.py`, `app/ingestion/ipea.py`, `app/ingestion/cepea.py`
- `scripts/ingest.py`
- `tests/unit/test_ingestion.py`
- `docs/RUNBOOK_INGESTION.md`
- `docs/handoffs/INGESTION.md`

## Interfaces Changed
- No external interfaces changed. Internal Python API for ingestion established.

## Tests/Checks
- Unit tests (`test_ingestion.py`) use `unittest.mock.patch` to verify JSON parsing, idempotency constraints (simulated via DB asserts), and error propagation (schema drift detection). No live network calls occur in CI.

## Limitations
- CEPEA adapter is mocked. A real implementation will require an HTML parsing strategy (e.g., BeautifulSoup) or an offline Excel upload process.
- The `ON CONFLICT` logic in `BaseAdapter` uses SQLite-specific dialect imports (`sqlalchemy.dialects.sqlite.insert`). If the system migrates to PostgreSQL, this must be changed to `sqlalchemy.dialects.postgresql.insert`.

## Risks
- IBGE SIDRA occasionally changes the internal variable IDs representing income depending on the PNADC vintage. The adapter currently hardcodes the table and uses a wide query, but this requires monitoring.

## Next Tasks
1. `07 Analytics`: Implement the Normalization Job that reads `raw_observations` and writes `normalized_prices` and `normalized_incomes`, effectively joining the ingested data to the REST API.
