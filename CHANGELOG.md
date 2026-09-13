# Changelog

All notable changes to the PoderBR project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- **Core Analytics Engine**: Implemented `AnalyticsService` calculating Basket Cost, Income Burden, Affordability Ratio, and Purchasing Power Index (PPI) idempotently.
- **Data Pipeline**: Added generic `BaseAdapter` and concrete adapters for IBGE (PNAD Contínua) and Ipeadata (Minimum Wage) utilizing `httpx` and `tenacity` backoffs.
- **API**: Exposed analytical boundaries via FastAPI `/api/v1/affordability`.
- **Frontend App Shell**: Scaffolding with React, Vite, TailwindCSS, and React Router.
- **Frontend Dashboard**: `Dashboard.tsx` and `Comparison.tsx` integrating Domain Controls (Geography, Dates, Income).
- **Accessible Charts**: Recharts visualizations wrapped in `AccessibleChart` toggles with semantic HTML `DataTable` fallbacks.
- **Data Observability**: Introduced `QualityService` checking staleness and anomalies without silent deletion. Surfaced via `/api/v1/quality/status`.
- **Security Hardening**: Docker multi-stage builds, non-root user isolation, `slowapi` rate limiting, CORS configuration, and CI dependency audits (`pip-audit`).

### Fixed
- Fixed an upstream integration error in `pytest` where SQLAlchemy test-session memory metadata was missing in-memory model loads for `normalized_prices` and `geography`.
- Refactored frontend and backend logic to address Ruff formatting (`E501`) and strict `vitest` isolation rules for E2E tests.
