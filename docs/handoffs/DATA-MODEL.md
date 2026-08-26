# Handoff: Data Model Phase

## Objective
Implement a provider-agnostic canonical data model using SQLAlchemy/Alembic that preserves data provenance, handles duplicate/idempotent ingestion, and implements data maturity states, ensuring a clean decoupling between external APIs and internal analytics.

## Decisions Made
- **Two-Tier Architecture:** Data is strictly segregated into `raw_observations` (provider-specific geography and units) and `normalized_prices`/`incomes` (canonical geography and standard units).
- **Idempotency:** Implemented at the database level via explicit `UniqueConstraint`s to prevent duplicate time-series entries regardless of how many times an ingestion script runs.
- **Data Maturity:** Implemented via the `ObservationStatus` Enum, explicitly defining when a value is `MISSING` versus `SOURCE_VERIFIED`.

## Evidence/Sources
- SQLAlchemy 2.0 documentation for typed mappings (`Mapped[T]`) and `DeclarativeBase`.
- Alembic configuration for autogenerating migrations.

## Files Created/Changed
- `app/db/base.py`, `app/db/session.py`
- `app/models/core.py`, `app/models/__init__.py`
- `alembic/env.py`, `alembic.ini`, `alembic/versions/*_initial_canonical_data_model.py`
- `tests/unit/test_canonical_model.py`, `tests/conftest.py`
- `docs/adr/0006-canonical-data-model.md`
- `docs/ADAPTER_GUIDE.md`
- `docs/handoffs/DATA-MODEL.md`

## Interfaces Changed
- Database schema established (Data Contract enforced).

## Tests/Checks
- Wrote and passed `test_canonical_model.py` which explicitly tests the unique constraints (idempotency) and enum states using an in-memory SQLite database.

## Limitations
- The `NormalizedIncome` and `NormalizedPrice` models currently assume Brazilian currency (`price_brl`). If pre-1994 data (Cruzeiro) is ever required, the schema will need an additional `currency` column.

## Risks
- Ingestion agents might attempt to bypass `raw_observations` and write directly to `normalized_prices`. This must be caught in code review, as it breaks the provenance chain.

## Next Tasks
1. `05 Backend`: Implement the repository layer and basic FastAPI routing.
2. `06 Ingestion`: Create the first concrete ingestion adapters for IBGE and Ipeadata following the `ADAPTER_GUIDE.md`.
