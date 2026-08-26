# API Contracts Index

This index tracks all cross-boundary contracts in the PoderBR architecture. Any agent modifying an interface must ensure these documents are updated and that consumer tests are aligned.

## Contract Registry

1. **Frontend-Backend Contract:** Defines the REST/JSON schemas exposed by FastAPI and consumed by the React app. [View `docs/contracts/FRONTEND_BACKEND_CONTRACT.md`](./contracts/FRONTEND_BACKEND_CONTRACT.md)
2. **Data (Database) Contract:** Defines the core PostgreSQL tables and schemas for raw and normalized data. [View `docs/contracts/DATA_CONTRACT.md`](./contracts/DATA_CONTRACT.md)
3. **Analytics Contract:** Defines the exact mathematical formulas and domain interfaces for the purchasing power calculations. [View `docs/contracts/ANALYTICS_CONTRACT.md`](./contracts/ANALYTICS_CONTRACT.md)
