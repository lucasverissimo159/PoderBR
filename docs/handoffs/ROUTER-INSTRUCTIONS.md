# Agent Router Output

## 1. Classification
The task requires acting as a system-level Agent Router that interprets ambiguous/broad user requests, identifies dependencies, and orchestrates the necessary sequence of specialized Jules tasks.

## 2. Prerequisites and Conflicts
- **Prerequisites:** The router must understand the `AGENTS.md` and `docs/ORCHESTRATION.md` workflows, along with the current state of the repository (`docs/handoffs/FINAL-AUDIT.md`, architecture docs, API contracts).
- **Conflicts:** Parallel execution must strictly follow the "Safe Parallelism" rules defined in `ORCHESTRATION.md` to avoid race conditions on contracts, methodologies, or schemas.

## 3. Parallelization
- Independent research tracks (e.g., Data Research vs Product Research) can run in parallel.
- Frontend and Backend can run in parallel *only if* the shared API contract in `docs/API_CONTRACTS.md` or `FRONTEND_BACKEND_CONTRACT.md` remains strictly unchanged, or if an exact, static contract update has already been merged.
- Schema migrations and Analytical core logic cannot run in parallel.

## 4. Canonical Contracts
- `/docs/API_CONTRACTS.md` or `FRONTEND_BACKEND_CONTRACT.md` (for frontend/backend handoffs).
- `/app/models/core.py` (Database schema source of truth).
- `docs/METHODOLOGY.md` (Formulas and definitions).

## 5. Proposed Task Sequence (Generic Template for New Feature Requests)
If a user requests a new feature (e.g., "Add a new dairy basket"), the router will sequence:
1. **Task 1: Data & Product Research (Agent: Research)** - Identify data sources (IBGE/CEPEA) for the new domain, verify geographic coverage, update Methodology docs, and propose the basket schema.
2. **Task 2: Data Ingestion & Model Updates (Agent: Backend/Data)** - Create the adapter for the new source, update models/schemas if necessary, and write ingestion tests.
3. **Task 3: Analytics Integration (Agent: Analytics)** - Verify the Analytics Engine logic handles the new basket type without zero-division or imputation errors.
4. **Task 4: UI Visualization (Agent: Frontend)** - Update the Dashboard and Comparison UI to allow selecting the new basket type, ensuring `AccessibleChart` fallback still works.

## 6. Prompt Examples
* **Task 1 (Research):** "Act as the Data Research agent. Explore IBGE and CEPEA to find data sources for a 'dairy' basket. Verify they have the same geographical/frequency scope as the existing MVP. Update `METHODOLOGY.md` with the findings and propose a basket schema. Do not implement code."
* **Task 2 (Data):** "Act as the Data Ingestion agent. Using the methodology defined in the previous handoff, implement the API adapter for the new dairy sources using `httpx` and `tenacity`. Ensure it writes to the `raw_observations` table deterministically. Ensure no existing tests break."

## 7. Plan Approvals
- **Task 1 (Research)** requires explicit Plan Approval before writing any code to ensure the selected methodology aligns with non-negotiable principles.
- **Tasks that modify schemas or core contracts** must be approved before execution.

## 8. Handoff Expectations
Every task must end with a `docs/handoffs/<TASK_NAME>.md` utilizing the standard template. It must list decisions made, interfaces changed, test results, identified risks, and the explicit instruction for the next agent in the sequence.
