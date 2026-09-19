# PoderBR

PoderBR is a public analytics platform designed to explain how income and prices affect purchasing power in Brazil.

This project aims to provide clear, methodologically sound answers to everyday economic questions: *Given a location, period, and income basis, what is the cost of a standardized basket of proteins, how much of the income does it consume, and how has this purchasing power changed over time?*

## Why This Exists?
Inflation numbers often feel disconnected from the grocery store reality. PoderBR isolates specific consumption baskets (starting with proteins: beef, pork, chicken, eggs) to measure real-world affordability without extrapolating into broad "cost of living" claims. We prioritize strict statistical honesty, avoiding silent data imputation or interpolation.

## What is it?
- A transparent, reproducible data pipeline fetching nominal prices and incomes from public APIs (IBGE, Ipeadata).
- A domain-driven calculation engine quantifying *Income Burden* and *Purchasing Power Index (PPI)*.
- An accessible, responsive React dashboard utilizing visual and tabular representations for data journalism and policy analysis.

## Core Features
- **Deterministic Pipeline:** Idempotent, bounded ingestion runs that never corrupt state upon upstream failure.
- **Strict Methodology:** No silent interpolations. If data is missing, the metric is mathematically missing.
- **Accessibility (WCAG 2.2 AA):** All visual Recharts are paired with semantic HTML tables for screen-reader interoperability.
- **Observability:** Health, staleness, and spike anomalies are observable by design through our `QualityService`.

## Quick Start (Clean Environment)

The setup process is deterministic, utilizing `uv` for lightning-fast Python dependency management.

```bash
# Clone the repository
git clone https://github.com/lucasverissimo159/PoderBR.git
cd PoderBR

# Bootstrap the environment (installs python deps, lints, and tests)
./scripts/setup.sh

# Start the application
# Terminal 1: Backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd app/frontend
npm ci
npm run dev
```

For more detailed developer guidelines, see [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md).

## Project Documentation
- **[Methodology](docs/METHODOLOGY.md)**: Mathematical definitions and data-handling caveats.
- **[Architecture](docs/ARCHITECTURE.md)**: System design and monolithic module boundaries.
- **[API Reference](docs/API.md)**: Consumer API contracts.
- **[Security & Operations](docs/SECURITY.md)**: Threat boundaries, rate limiting, and Docker deployment strategies.
- **[Data Pipeline](docs/DATA_PIPELINE.md)**: Details on ingestion adapters and idempotency constraints.
