# Ingestion Runbook

This document describes how to operate, debug, and maintain the ingestion layer of PoderBR.

## 1. Running Ingestion
The ingestion pipelines are executed via the CLI runner.

### Standard Run
To ingest all sources sequentially:
```bash
uv run python scripts/ingest.py all
```

To run a specific adapter (e.g., Ipeadata):
```bash
uv run python scripts/ingest.py ipeadata
```

### Dry Run (Validation)
To validate the API response format without altering the database:
```bash
uv run python scripts/ingest.py all --dry-run
```
This is highly recommended after deploying updates to check for upstream schema drift.

## 2. Handling Failures and Retries

### Idempotency
All adapters are built to be idempotent using `ON CONFLICT DO UPDATE`. If a run fails halfway through, you do not need to clean the database. Simply re-run the script.

### Provider Unavailable (HTTP 5xx)
If an official source (e.g., IBGE SIDRA) returns a 500 series error, the script will crash and log the exception.
**Action:** Wait and retry. These APIs occasionally experience downtime. The analytics layer will continue functioning using cached database records.

### Schema Drift (HTTP 200, but parsing fails)
If IBGE or Ipeadata change their JSON schema, the adapter will raise a `ValueError("Schema drift...")` and mark the `IngestionRun` as `failed`.
**Action:**
1. Execute a `--dry-run` to inspect the new payload format in the logs.
2. Update the corresponding parser in `app/ingestion/`.
3. Write a test case capturing the new schema format.
4. Redeploy and re-run.

## 3. Investigating the Database
To inspect the status of recent ingestion runs via `sqlite3`:
```sql
SELECT id, source_id, started_at, status, records_processed FROM ingestion_runs ORDER BY started_at DESC LIMIT 5;
```

To verify provenance of a specific value:
```sql
SELECT * FROM raw_observations WHERE source_id = 'ipeadata_MTE12_SALMIN12' ORDER BY reference_date DESC;
```
