# Handoff: Data Research Phase

## Objective
Identify and evaluate official data sources for income, inflation, and nominal protein prices in Brazil to support the PoderBR affordability MVP. Determine the most defensible historical and geographic coverage strategy.

## Decisions Made
- **Income (Base):** Ipeadata `MTE12_SALMIN12` for National Minimum Wage.
- **Income (Average):** IBGE SIDRA `10280` for PNAD Contínua average income.
- **Inflation:** IBGE SIDRA `1737` & `7060` (IPCA) will be used for general macroeconomic context, but *not* for backward-extrapolating nominal prices.
- **Nominal Prices:** CEPEA/ESALQ will be used for nominal protein prices (Beef, Pork, Chicken).
- **Geographic Scope:** Restricted to National and São Paulo (SP) for the MVP due to the lack of ubiquitous, API-accessible nominal price data for all 27 UFs.
- **Methodology:** Rejected backward-inflation calculation. We will only compare actual historical nominal income against actual historical nominal prices.

## Evidence/Sources
- IBGE SIDRA API Documentation & Endpoints.
- Ipeadata OData API.
- CEPEA/ESALQ methodological notes.
- Research confirmed that IBGE publishes the IPCA as an index/variation, not as nominal shelf prices via their primary APIs.

## Files Created/Changed
- `docs/DATA_SOURCES.md`
- `docs/DATA_DICTIONARY.md`
- `docs/GEOGRAPHIC_COVERAGE.md`
- `docs/DATA_LICENSES.md`
- `docs/adr/0003-data-source-selection.md`
- `docs/handoffs/DATA-RESEARCH.md`

## Interfaces Changed
- N/A

## Tests/Checks
- Verified API endpoints using `curl` and `jq` to ensure data structures match expectations (e.g., confirming SIDRA 10280 contains average income).

## Limitations
- **CEPEA Data Access:** CEPEA does not have a clean REST API. The Data Engineering agent will need to write custom scraping or CSV parsing logic for these sources.
- **Frequency Mismatch:** PNADC income is quarterly; Minimum Wage and prices are monthly.

## Risks
- Depending on CEPEA for prices means we are bound by their publication formats, which may change and break our ingestion scripts.
- Users may request data for other states (e.g., Rio de Janeiro, Bahia), which we cannot provide without violating the "no fabricated observations" rule unless new data sources are found.

## Next Tasks
1. `03 Architecture`: Define the Alembic database migrations based on the `docs/DATA_DICTIONARY.md`.
2. `04 Data Model/ETL`: Implement the ingestion scripts (Python/pandas) for the IBGE and Ipeadata APIs.
