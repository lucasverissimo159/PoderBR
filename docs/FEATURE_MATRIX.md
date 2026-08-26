# Feature Matrix & Backlog

This backlog is dependency-aware. Agents must complete Phase 1 before moving to Phase 2.

## Phase 1: Core Data Foundation (Data & Backend Agents)
| ID | Feature | Dependency | Agent Role | Status |
|---|---|---|---|---|
| F1.1 | Define final basket quantities based on nutritional or historical POF standards | None | Data Research | Pending |
| F1.2 | Identify exact IBGE/SIDRA API endpoints for Minimum Wage and Average Income | None | Data Research | Pending |
| F1.3 | Identify exact API/source for nominal protein prices (e.g., CEPEA, IBGE SNIPC) | None | Data Research | Pending |
| F1.4 | Design DB schema for raw observations, normalized prices, and methodology versioning | F1.1, F1.2, F1.3 | Architecture | Pending |
| F1.5 | Implement ingestion scripts for Income Data | F1.4 | Data Engineering | Pending |
| F1.6 | Implement ingestion scripts for Protein Price Data | F1.4 | Data Engineering | Pending |
| F1.7 | Implement Domain Analytics logic (calculate `basket_cost`, `income_burden`) | F1.5, F1.6 | Backend/Domain | Pending |

## Phase 2: API & Presentation (API & Frontend Agents)
| ID | Feature | Dependency | Agent Role | Status |
|---|---|---|---|---|
| F2.1 | Define OpenAPI schema for dashboard endpoints (historical trend, current snapshot) | F1.7 | API | Pending |
| F2.2 | Implement FastAPI endpoints matching the OpenAPI schema | F2.1 | Backend/API | Pending |
| F2.3 | Scaffold React/Vite frontend application | None | Frontend | Pending |
| F2.4 | Implement base UI components (Selectors for Geography/Income, Layout) | F2.3 | Frontend | Pending |
| F2.5 | Implement Recharts visualization (Trend line with progressive disclosure tooltips) | F2.4, F2.1 | Dashboard | Pending |
| F2.6 | Implement Accessible Data Table view (for screen readers) | F2.4, F2.1 | Frontend | Pending |
| F2.7 | Implement Methodology and Provenance disclosure panels | F2.3 | Frontend | Pending |

## Phase 3: Quality & Refinement (QA & Platform)
| ID | Feature | Dependency | Agent Role | Status |
|---|---|---|---|---|
| F3.1 | End-to-End Playwright tests for user flows (Empty states, successful render) | F2.5 | QA | Pending |
| F3.2 | Verify a11y compliance (Keyboard navigation, contrast) | F2.6 | QA | Pending |
| F3.3 | Implement error state handling in UI (API failures) | F2.5 | Frontend | Pending |
