# Ownership

This document defines file, domain, and shared-contract ownership for the PoderBR platform. Jules agents must consult this to avoid concurrent modification conflicts.

## Domains

*   **Ingestion (ETL/Data Sources)**: `app/ingestion/`, `data/raw/`
*   **Normalization (Data Model)**: `app/models/`, `alembic/`
*   **Analytics (Domain Logic)**: `app/analytics/`, `analytics/`
*   **API (Contracts/Routes)**: `app/api/`
*   **Frontend (UI/Visualization)**: `frontend/` (To be created)

## Shared Contracts

The following files and concepts represent shared contracts. Altering them requires cross-domain coordination and updates to contract tests.

1.  **API OpenAPI Schema**: Changes to endpoint requests/responses.
2.  **Database Schema**: Alembic migrations and SQLAlchemy models.
3.  **Methodology Constants**: The defined basket composition and base periods.
4.  **Normalized Data Schema**: The shape of the data after ingestion and before analytics.

## Agent Ownership (Current Phase)

*   **Bootstrap Agent**: Bootstrapping all base directories, configuration, and documentation. Ownership of `scripts/setup.sh`.
