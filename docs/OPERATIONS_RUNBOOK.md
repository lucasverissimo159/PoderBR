# Operations & Security Runbook

This document covers operational guidelines, security boundaries, and CI/CD operations for PoderBR.

## 1. Security Boundaries & Out-of-Scope Controls
- **Authentication/Authorization**: Out of scope for MVP. The platform provides public read-only access to analytical metrics. There are no user accounts, passwords, or OAuth flows.
- **PII / User Data**: The platform does not collect, store, or process Personally Identifiable Information. User-supplied income data used in the UI is evaluated ephemerally and never logged or stored in the database.
- **Secrets Management**: No secrets (API keys, passwords, database URLs) are committed to the repository. The application relies on environment variables (`.env`). Deployment environments must inject these securely (e.g., GitHub Secrets, AWS Parameter Store, Kubernetes Secrets).

## 2. Platform Hardening
- **Docker**: The containerized backend runs as a non-root user (`poderbr`). `docker-compose.yml` mounts the root filesystem as `read_only: true` with explicitly scoped `tmpfs` mounts to prevent persistence of malicious payloads.
- **Security Headers**: Standard headers (HSTS, X-Content-Type-Options, X-Frame-Options) are enforced via FastAPI middleware.
- **CORS**: Strictly limited via the `CORS_ORIGINS` environment variable.
- **Rate Limiting**: Bounded rate limiting is implemented via `slowapi` on expensive calculation endpoints (e.g., `/api/v1/affordability`) to mitigate scraping or DoS attacks.
- **Logging**: JSON-structured logging is enabled to integrate seamlessly with standard aggregators (Datadog, ELK). Uvicorn access logs are reduced to `WARNING` in production to prevent query-parameter leakage.

## 3. Dependency Management & CI Supply Chain
- **Auditing**: GitHub Actions runs `pip-audit` on every PR/push to detect known vulnerabilities in Python dependencies.
- **Versions**: Node and Python versions are pinned in `.github/workflows/ci.yml`.
- **Action**: Developers should regularly update `pyproject.toml` and lockfiles to incorporate security patches.

## 4. Health, Readiness, and Observability
- **Endpoint**: `/health` returns `{ "status": "ok" }`. This is used by Docker health checks and load balancers.
- **Monitoring**: Alerts should be configured if `/health` fails 3 consecutive times.

## 5. Backup & Restore Assumptions
- **Database**: The PostgreSQL database contains normalized prices, incomes, and ingestion history. While upstream data (IBGE/CEPEA) can technically be re-ingested from scratch, historical versions may drift.
- **Strategy**:
  - Nightly automated snapshots of the RDS/PostgreSQL volume.
  - Write-Ahead Logging (WAL) archiving for Point-In-Time-Recovery (PITR) up to 7 days.
- **Restore Test**: Operations must verify backup restoration in a staging environment quarterly.

## 6. Upstream Provider Failure (Resilience)
If IBGE or CEPEA endpoints go down:
1. Ingestion cron jobs will fail deterministically (logged as `failed` in `IngestionRun`).
2. Existing normalized data remains safely cached and served by the API.
3. The platform does *not* corrupt current data if a partial payload is returned (idempotency constraints and schema-drift handling).
