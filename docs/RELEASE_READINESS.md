# Release Readiness Matrix

This matrix serves as the final integration checklist for PoderBR. It validates that the schema, migrations, data sources, frontend logic, and deployment constraints form a coherent system ready for a production candidate release.

## Pass/Fail Matrix

| Sub-system | Category | Validation Goal | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Migrations** | Database | Alembic migrations match SQLAlchemy `models/core.py`. | **PASS** | `alembic upgrade head` executed cleanly. Performance indexes applied successfully. |
| **Analytics** | Calculations | Division by zero is prevented on `0` income or `0` basket costs. | **PASS** | Evaluated via `hypothesis` property-based fuzzing tests. |
| **Analytics** | Methodology | Missing data yields `null` (not zero) for aggregate metrics. | **PASS** | Unit tests verify no silent imputation or extrapolation occurs. |
| **API** | Contracts | REST endpoints match the models defined in `FRONTEND_BACKEND_CONTRACT.md`. | **PASS** | Frontend strictly typed to API output; E2E tests mock matching JSON schemas. |
| **API** | Edge Cases | Invalid dates or unknown Geographies return clean `4XX` status codes. | **PASS** | Covered by `test_api_validation.py`. |
| **Frontend** | UX/Routing | Navigation works between Dashboard and Comparison views. | **PASS** | Verified via Playwright execution (`verify_analytical_dashboard.py`). |
| **Frontend** | Accessibility | All visual charts provide a screen-reader friendly tabular alternative. | **PASS** | Verified via Playwright `AccessibleChart` toggle behavior tests. |
| **Quality** | Observability | Large MoM price spikes or staleness alert users but do not drop data. | **PASS** | `QualityService` exposes warnings to `MethodologyDisclosure` UI successfully. |
| **Platform** | Security | Docker runs as non-root; `pip-audit` runs on CI; IP Rate limiting active. | **PASS** | Implemented via `slowapi`, `.env.example`, and `Dockerfile` constraints. |

## Identified Risks
- **Data Latency:** The IBGE API updates slowly. The `staleness` threshold is currently set to 45 days, but this may need adjusting depending on the official PNAD release schedule to prevent permanent warnings.
- **Node.js Deprecation:** GitHub Actions environment was upgraded to Node 22 to bypass Node 20 deprecation warnings, but dependencies must be monitored for compatibility with Node 22.

## Migration Notes
- Ensure the production database applies `a1bd726d913b_add_performance_indexes.py` immediately to prevent CPU spiking on the `/api/v1/affordability` endpoint under load.

## Final Audit Status
The final Principal Engineer audit (`docs/handoffs/FINAL-AUDIT.md`) has marked the system as **Production-Ready**. No release blockers are currently open.
