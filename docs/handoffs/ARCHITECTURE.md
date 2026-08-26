# Handoff: Architecture Phase

## Objective
Establish clear domain boundaries, software architecture patterns, and interface contracts for PoderBR so future agents can implement ingestion, backend logic, and frontend visualization without architectural conflicts.

## Decisions Made
- **Architecture Pattern:** Feature-based Modular Monolith using FastAPI.
- **Data Fetching/State (Frontend):** React Query / TanStack Query, relying heavily on HTTP caching headers due to the low frequency (monthly) of data updates.
- **API Pattern:** Synchronous REST API (`/api/v1/...`). Background data ingestion will happen via scheduled cron/scripts, not real-time scraping during API requests.
- **Contracts:** Cross-boundary communication (e.g., between the Database and the API, or Backend and Frontend) is strictly governed by explicit contracts (Pydantic models, JSON schemas) documented in `docs/contracts/`.

## Evidence/Sources
- FastAPI documentation for modular routing (APIRouter) and dependency injection.
- React Query documentation for managing asynchronous server state.
- DDD (Domain Driven Design) principles applied to Python applications.

## Files Created/Changed
- `docs/ARCHITECTURE.md`
- `docs/DOMAIN_MODEL.md`
- `docs/adr/0004-domain-boundaries.md`
- `docs/adr/0005-api-strategy.md`
- `docs/API_CONTRACTS.md`
- `docs/contracts/FRONTEND_BACKEND_CONTRACT.md`
- `docs/contracts/DATA_CONTRACT.md`
- `docs/contracts/ANALYTICS_CONTRACT.md`
- `docs/handoffs/ARCHITECTURE.md`

## Interfaces Changed
- N/A (Defined interfaces, no implementation changed yet).

## Tests/Checks
- Contract files have been written clearly to allow future unit testing based on Pydantic schemas.

## Limitations
- We have not chosen a specific Python scheduling library (e.g., APScheduler) yet, assuming standard cron or GitHub Actions will trigger ingestion for the MVP.
- Authentication/Authorization architecture is explicitly omitted per MVP requirements.

## Risks
- The frontend and backend agents must strictly adhere to `FRONTEND_BACKEND_CONTRACT.md`. Any divergence will break the application.
- The `DATA_CONTRACT.md` might need adjustment once actual data ingestion begins if the source APIs return unexpected formats.

## Next Tasks
1. `04 Data Model/ETL`: Implement SQLAlchemy models and Alembic migrations based on `DATA_CONTRACT.md`.
2. `05 Backend`: Implement the FastAPI router and Pydantic schemas based on `FRONTEND_BACKEND_CONTRACT.md`.
