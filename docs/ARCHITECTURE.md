# Architecture - PoderBR

PoderBR follows a **Modular Monolith** architecture, leveraging synchronous APIs, deterministic scheduled ingestion, and a component-driven Single Page Application (SPA).

## System Overview

```text
┌────────────────────────────────────────────────────────┐
│                      FRONTEND                          │
│  (React + Vite + Recharts + React Query + Tailwind)    │
│  - Handles UI state, routing, and data fetching        │
│  - Progressively discloses methodology and data        │
└────────────────────────┬───────────────────────────────┘
                         │ REST API (JSON)
┌────────────────────────▼───────────────────────────────┐
│                      BACKEND                           │
│  (Python + FastAPI + SQLAlchemy + Alembic)             │
│                                                        │
│  ┌───────────────┐ ┌────────────────┐ ┌─────────────┐  │
│  │    API (v1)   │ │   Analytics    │ │   Quality   │  │
│  │ (Validation,  │ │ (Calculations, │ │ (Anomalies, │  │
│  │  Routing)     │ │  Formulas)     │ │  Staleness) │  │
│  └───────┬───────┘ └───────┬────────┘ └──────┬──────┘  │
│          │                 │                 │         │
│  ┌───────▼─────────────────▼─────────────────▼──────┐  │
│  │                  Normalization                   │  │
│  │  (Standardizing Geography, Units, Currencies)    │  │
│  └─────────────────────────┬────────────────────────┘  │
│                            │                           │
│  ┌─────────────────────────▼────────────────────────┐  │
│  │                    Ingestion                     │  │
│  │      (Adapters for IBGE, Ipeadata, CEPEA)        │  │
│  └─────────────────────────┬────────────────────────┘  │
└────────────────────────────┼───────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────┐
│                       DATABASE                         │
│             (PostgreSQL/SQLite via SQLAlchemy)         │
└────────────────────────────────────────────────────────┘
```

## Technology Stack Justification

### Backend
- **FastAPI**: Selected for its asynchronous capabilities, auto-generated OpenAPI documentation, and strict Pydantic payload validation which ensures strong contract boundaries.
- **SQLAlchemy + Alembic**: Provides an ORM with a robust migration system capable of handling our two-tier data model (Raw vs. Normalized).
- **Tenacity**: Ensures upstream resilience by applying bounded exponential backoffs to flaky third-party ingestion endpoints.

### Frontend
- **React + Vite**: Vite offers sub-second cold starts and rapid HMR, significantly improving developer velocity over Webpack. React's component ecosystem allows for reusable domain controls.
- **TanStack Query (React Query)**: Because our data changes infrequently but requires complex loading/error states, React Query handles caching, refetching, and state management elegantly without Redux bloat.
- **Recharts**: Declarative SVG charting that can be explicitly configured to skip `null` values (`connectNulls={false}`), ensuring statistical honesty when data is missing.
- **Tailwind CSS**: Utility-first CSS ensuring strict design consistency and accessible contrast ratios without maintaining separate stylesheet files.

## Core Architectural Principles

1. **Strict Module Boundaries:** The `API` module never imports from the `Ingestion` module directly.
2. **DTO Contracts:** Data moving between layers is validated using Pydantic models. We never pass raw SQLAlchemy ORM models to the presentation layer.
3. **Stateless API:** The backend API relies on HTTP caching headers and database indices. It maintains no session state.
4. **Scheduled Ingestion:** Data updates monthly. Ingestion scripts run asynchronously via cron or CI/CD, writing to the database independently of synchronous API request flows.
