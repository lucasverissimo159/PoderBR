# Handoff: Bootstrap Phase

## Objective
Establish the repository structure, documentation, and technical foundations for the PoderBR project, enabling future Jules agents to work efficiently.

## Decisions Made
- Selected Python (FastAPI, SQLAlchemy, pandas) for the backend to handle data-heavy workloads and provide clear API contracts.
- Selected React (Vite, Recharts) for the future frontend.
- Selected PostgreSQL + Alembic for deterministic, versioned data storage.
- Selected GitHub Actions for CI.
- Selected IBGE (SIDRA) and Ipeadata as the primary sources for macroeconomic public data in Brazil.

## Evidence/Sources
- Official documentation for FastAPI, React, Vite, Recharts.
- IBGE SIDRA API documentation (`https://servicodados.ibge.gov.br/api/v3/agregados`).
- Ipeadata API documentation (`http://www.ipeadata.gov.br/api/odata4/`).

## Files Created/Changed
- `AGENTS.md`, `README.md` (Updated)
- `docs/PROJECT_CONTEXT.md`, `docs/ORCHESTRATION.md`, `docs/JULES_WORKFLOW.md` (Updated/Reviewed)
- `docs/adr/0001-initial-architecture.md`, `docs/adr/0002-data-source-strategy.md`
- `docs/CONTRIBUTING.md`, `docs/METHODOLOGY.md`, `docs/AGENT_STATE.md`, `docs/OWNERSHIP.md`
- `docs/handoffs/BOOTSTRAP.md`
- `.gitignore`, `.editorconfig`, `LICENSE`, `pyproject.toml`
- Directory structure: `app/`, `data/`, `analytics/`, `tests/`, `scripts/`
- `scripts/setup.sh` (deterministic environment setup)
- `.github/workflows/ci.yml` (CI pipeline)

## Interfaces Changed
- N/A (Initial creation)

## Tests/Checks
- Created a `setup.sh` script that installs `uv`, creates a virtual environment, installs dependencies, runs `ruff` linting, and runs a dummy `pytest` suite to validate the environment.

## Limitations
- No actual data is ingested yet.
- The `METHODOLOGY.md` contains unverified assumptions regarding the basket composition and data sources for nominal prices.
- The frontend directory is not yet bootstrapped, as the focus is on the backend/data foundation first.

## Risks
- The APIs for nominal protein prices (e.g., CEPEA) might be harder to query programmatically than IBGE macroeconomic data.

## Next Tasks
1. `01 Product Research`
2. `02 Data Research`
3. `03 Architecture`
