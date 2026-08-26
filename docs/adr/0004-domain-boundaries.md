# ADR 0004: Domain Boundaries & Modular Monolith Strategy

## Context
PoderBR needs to ingest data from external sources (IBGE, Ipeadata, CEPEA), normalize it, apply economic formulas (analytics), and serve it via an API to a React frontend. We must decide how to organize this logic to prevent "spaghetti code" and ensure future agents can safely modify one area without breaking another.

## Decision

We will adopt a **Modular Monolith** architecture based on Domain-Driven Design (DDD) principles, using a Vertical Slice / Feature-based folder structure rather than a purely layered one.

The application will be divided into explicit domains:
1. **Ingestion (`app/ingestion/`)**: Responsible for fetching data from external APIs (IBGE, Ipeadata, CEPEA). It knows about HTTP requests, scraping, and raw JSON/CSV parsing. It writes to the `raw_observations` table.
2. **Normalization (`app/normalization/`)**: Responsible for taking raw observations and converting them into canonical types (e.g., standardizing geography codes, converting currencies to BRL, normalizing units to kg/dozen). Writes to `normalized_prices` and `normalized_income`.
3. **Analytics (`app/analytics/`)**: The core domain. Contains the business logic for calculating the basket cost and income burden. It reads normalized data, applies the methodology, and generates `affordability_metrics`.
4. **API (`app/api/`)**: The HTTP presentation layer. It defines FastAPI routers, validates inputs using Pydantic, and returns JSON. It depends on Analytics for data.

**Cross-cutting concerns:**
- **Database (`app/db/`)**: SQLAlchemy engine, session management, and Alembic migrations.
- **Models (`app/models/`)**: Shared SQLAlchemy ORM models (internal to the backend).

**Contracts Between Boundaries:**
Domains must communicate via explicitly defined Pydantic models (Data Transfer Objects), not by passing raw SQLAlchemy ORM objects. This ensures that changes in the database schema do not implicitly break the API or Analytics logic.

## Consequences
- We will not use microservices. The operational overhead of deploying multiple services for an MVP with monthly data updates is unjustified.
- Agents working on `app/ingestion/` should not need to modify `app/api/`.
- All database migrations remain unified in a single Alembic history.
