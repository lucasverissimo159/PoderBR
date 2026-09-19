# Request: Act as Jules Agent Router for Future Tasks

## 1. Classification
Role: **Agent Router / Orchestrator**.
The request is to establish the routing behavior and blueprint for handling future, potentially ambiguous, broad, or cross-cutting user requests, in alignment with `AGENTS.md` and `docs/ORCHESTRATION.md`.

## 2. Prerequisites & Conflicting Work
*   **Prerequisites:** Before any feature implementation begins, a formal **Research & Methodology** phase must complete. If a request touches the core database model or the REST API, the shared canonical contract (`app/models/core.py`, `docs/API.md`, or API contracts) must be updated and locked.
*   **Conflicts:**
    *   Never assign two agents ownership of the same contract simultaneously (e.g., frontend and backend cannot both define the API independently).
    *   Data Ingestion must not run in parallel with Database Migrations.

## 3. Parallelization
*   **Safe:** UI implementation can run in parallel with Backend/API implementation *only after* the shared API contract is finalized and mocked.
*   **Safe:** Data Research can run in parallel with Platform/Security architecture reviews.
*   **Unsafe:** Methodology updates and Analytics Engine changes must be strictly sequential.

## 4. Canonical Contracts Involved
*   **Data Dictionary / Database:** `app/models/core.py` and Alembic migrations.
*   **Methodology / Formulas:** `docs/METHODOLOGY.md`
*   **API Contract:** `docs/API.md` (and any specific `FRONTEND_BACKEND_CONTRACT.md`)
*   **Handoffs:** `docs/handoffs/` directory.

## 5. Proposed Task Sequence (Blueprint for Cross-Cutting Features)

Whenever a broad feature request arrives (e.g., "Add a transportation cost index to the dashboard"), the router should emit the following task graph:

```text
       [Router Output Triggered]
                  |
    Task 1: Research & Methodology (Agent: Data/Product Research)
                  |
    [Plan Approval Required: Verify Methodology rules]
                  |
          Task 2: Architecture & Contracts (Agent: Architecture)
                  |
    [Plan Approval Required: ADR and Contract Lock]
                  |
      +-----------+-----------+
      |                       |
 Task 3a: Backend &     Task 3b: UI & Dashboard
 Data Ingestion         (Agent: Frontend)
 (Agent: BE/Data)             |
      |                       |
      +-----------+-----------+
                  |
 Task 4: Platform Security & QA Integration (Agent: QA/Sec)
                  |
 Task 5: Final Audit & Documentation (Agent: Release Audit)
```

## 6. Prompts for the Task Sequence

**Prompt 1: Research & Methodology (Data/Product Research Agent)**
> "Act as the Product and Data Research Agent. The user requested [Feature]. Research primary data sources (e.g., IBGE, BACEN) to support this. Verify geographic coverage, frequency, and licensing. You must not fabricate data. Propose updates to `docs/METHODOLOGY.md` and create an initial basket/index schema. Output your findings and update the handoff document. Do NOT write application code."

**Prompt 2: Architecture & Contracts (Architecture Agent)**
> "Act as the Architecture Agent. Review the handoff from the Research Agent regarding [Feature]. If structural changes are needed to the backend or API, write an ADR (in `docs/adr/`) and update `docs/API.md`. Define the strict JSON response payload. Do NOT implement the feature yet. Request plan approval once the ADR and contracts are drafted."

**Prompt 3a: Backend & Data Ingestion (Backend/Data Agent)**
> "Act as the Backend/Data Engineering Agent. Implement the database migrations and data ingestion adapter for [Feature] based on the approved ADR and Methodology. Ensure the adapter is idempotent and handles network failures gracefully (`tenacity`). Implement the analytics logic without interpolating missing data. Add Pytest unit and integration tests. Update your handoff."

**Prompt 3b: UI & Dashboard (Frontend Agent)**
> "Act as the Frontend Agent. Build the UI components for [Feature] based on the strict API contract defined in Task 2. Ensure all new visual charts use Recharts and are wrapped in the `AccessibleChart` component to provide a semantic HTML `DataTable` fallback. Add Playwright E2E tests and Vitest unit tests. Update your handoff."

**Prompt 4: Security & QA Integration (QA/Platform Agent)**
> "Act as the Security and QA Agent. Review the integrated [Feature]. Execute the property-based fuzzing tests using `hypothesis` against the new analytics logic. Run dependency audits (`pip-audit`, `npm audit`). Ensure the new endpoints are covered by `slowapi` rate limiting and do not leak PII in logs. Output the final release readiness."

## 7. Plan Approval Requirements
*   **Task 1 (Research)** and **Task 2 (Architecture)** require strict User/Principal Plan Approval before execution. We must agree on the methodology and API contracts *before* committing engineering resources.
*   **Task 4 (Security)** requires review if new infrastructure or external ports are introduced.

## 8. Handoff Expectations
Between each task, the completing agent MUST create a file in `docs/handoffs/` (e.g., `docs/handoffs/TASK-1-RESEARCH.md`) detailing:
*   `objective`: What was requested.
*   `decisions`: Methodological or technical choices made.
*   `evidence`: Links to primary source API docs or ADRs.
*   `interfaces changed`: Specific API endpoints or DB schemas altered.
*   `limitations`: Known gaps (e.g., "Data only available nationally, not per-state").
*   `next tasks`: Explicit instructions for the next agent in the graph.
