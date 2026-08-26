# Architecture - PoderBR

PoderBR follows a **Modular Monolith** architecture.

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
│  (Python + FastAPI + SQLAlchemy + Alembic + pandas)    │
│                                                        │
│  ┌───────────────┐ ┌────────────────┐ ┌─────────────┐  │
│  │    API (v1)   │ │   Analytics    │ │   Baskets   │  │
│  │ (Validation,  │ │ (Calculations, │ │ (Methodology│  │
│  │  Routing)     │ │  Formulas)     │ │  Versions)  │  │
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
│                    (PostgreSQL)                        │
└────────────────────────────────────────────────────────┘
```

## Core Principles

1.  **Strict Boundaries:** The `API` module never imports from the `Ingestion` module directly. Data flows vertically.
2.  **DTO Contracts:** Data moving between layers is validated using Pydantic models. We do not pass raw SQLAlchemy models to the presentation layer.
3.  **Stateless API:** The backend API relies on HTTP caching headers and database speed. It does not maintain session state.
4.  **Scheduled Ingestion:** Data updates monthly. Ingestion scripts run asynchronously via cron or CI/CD pipelines, writing to the database independently of API requests.
