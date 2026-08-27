# Handoff: Backend Domain Phase

## Objective
Implement the FastAPI backend foundation, strictly separating HTTP routing, business logic, and database access to ensure stability, testability, and adherence to the analytics contracts.

## Decisions Made
- **Layered Architecture:** Implemented Routers -> Services -> Repositories.
- **Error Handling:** Created `DomainException` to keep HTTP concepts out of the service layer, with a global FastAPI handler to map these to standard JSON API responses.
- **Missing Data Handling:** The Analytics service explicitly refuses to interpolate missing prices. If a single basket item is missing for a month, the total cost and burden are set to `0.0` and the `quality_flag` is set to `partial`.

## Evidence/Sources
- FastAPI documentation for Exception Handlers and Dependency Injection.
- Previous `FRONTEND_BACKEND_CONTRACT.md` and `ANALYTICS_CONTRACT.md`.

## Files Created/Changed
- `app/main.py`, `app/core/*`
- `app/api/routes/*`, `app/api/dependencies/*`
- `app/schemas/*`, `app/services/*`, `app/repositories/*`
- `tests/unit/test_services.py`, `tests/integration/test_api_analytics.py`, `tests/integration/test_migrations.py`
- `docs/adr/0007-backend-service-layer.md`

## Interfaces Changed
- The REST API is now live and strictly adheres to the `FRONTEND_BACKEND_CONTRACT.md`.

## Tests/Checks
- Unit tests cover the business logic and handling of missing data.
- Integration tests cover the FastAPI injection and JSON serialization.
- Migration smoke test ensures Alembic paths are clear.

## Limitations
- The system is read-only at the API level right now. Ingestion scripts still need to be built to populate the database.

## Risks
- The `calculate_affordability` algorithm groups by month using `date.isoformat()`. This assumes that ingestion normalizes all dates to the first of the month. If ingestion inserts `2024-01-15` for prices and `2024-01-01` for income, the join will fail.

## Next Tasks
1. `06 Data Ingestion`: Implement the Python scripts to actually pull data from IBGE and Ipeadata and populate `raw_observations`.
