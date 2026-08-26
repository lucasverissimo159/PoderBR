# Prompt 13 — Data Quality, Freshness and Observability

Act as the Data Quality/Observability Agent.

Read source research, data contracts, ingestion code and analytics methodology.

## Mission

Turn data quality from an implicit hope into an observable product capability.

## Research

Investigate practical data-quality patterns for statistical pipelines:
- completeness/freshness checks;
- schema validation;
- unit/geography integrity;
- duplicate detection;
- range/anomaly checks;
- source revision detection;
- quality scores and operational thresholds.

## Implement

Create:
- quality checks;
- ingestion run summary/status;
- validation reports;
- freshness indicators;
- anomaly flags rather than destructive auto-deletion;
- tests for representative failures;
- operational documentation.

Where possible, expose a machine-readable quality state so the API/UI can disclose incomplete or stale data.

Do not invent thresholds blindly; justify them or make them configurable.
