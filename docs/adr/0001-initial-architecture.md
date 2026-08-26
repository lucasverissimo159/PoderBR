# ADR 0001: Initial Architecture

## Context
PoderBR needs an architecture that allows future Jules agents to build a platform measuring the purchasing power of basic items (starting with proteins) across Brazil over time. The platform must be testable, deterministically reproducible, easy to orchestrate locally for automated agents (Jules), and support clear data provenance.

## Decision

We have selected the following stack for the MVP:

1.  **Backend:** Python + FastAPI.
    *   *Why:* Python is the lingua franca for data processing (pandas/polars) which fits our heavy data manipulation needs. FastAPI provides excellent async performance, automatic OpenAPI documentation (essential for cross-agent API contracts), and strong type-checking (Pydantic). Flask, while simpler, lacks native typing and async integration.
2.  **Frontend:** Vite + React + TypeScript.
    *   *Why:* React's component model and ecosystem maturity make it the safest choice for a modular frontend. TypeScript is non-negotiable for strict contracts. Vite is chosen over Next.js because we initially need a simple Single Page Application without the complexity of Server-Side Rendering (SSR) until we have explicit SEO or load-time requirements.
3.  **Database & Migrations:** PostgreSQL + Alembic (via SQLAlchemy).
    *   *Why:* PostgreSQL is the most robust open-source relational database, perfectly suited for structured historical data, and supports JSON for flexible methodology storage if needed. Alembic provides predictable, versioned schema migrations which are critical for agent reproducibility.
4.  **Testing Strategy:** pytest + Playwright (or Vitest for pure frontend).
    *   *Why:* pytest is the gold standard for Python testing, offering fixtures that are perfect for isolated data tests. Playwright offers the most reliable headless browser testing, crucial for automated QA agents validating UI changes without a display.
5.  **Charting & Accessibility:** Recharts.
    *   *Why:* Recharts is declarative and simple to implement in React. According to recent research, Recharts provides reasonable accessibility hooks and is easier for agents to generate standard charts compared to low-level libraries like Visx, and more flexible than strictly opinionated wrappers.
6.  **Local Orchestration:** standard virtualenvs (uv/pip) + Docker for database/services.
    *   *Why:* As per the Jules setup requirements (lightweight, non-interactive, no long-running servers in setup), standard Python tooling like `uv` combined with a simple `docker-compose` for the DB provides the fastest, most deterministic setup for agent snapshots. Full dockerization of the dev environment is premature and slows down agent interactions.
7.  **CI/CD:** GitHub Actions.
    *   *Why:* Standard, integrated with the repo, declarative, and easy to parse and maintain by agents.

## Consequences
- Agents must define clear Pydantic schemas for all data crossing the backend/frontend boundary.
- All database changes must be accompanied by an Alembic migration.
- The repository must include a fast `scripts/setup.sh` that initializes the `uv` environment and runs pytest without requiring the DB to be running if testing purely logical transformations.
