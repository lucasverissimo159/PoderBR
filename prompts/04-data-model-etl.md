# Prompt 04 — Canonical Data Model, Provenance and Migration Foundation

Act as the Data Engineering Agent.

Read architecture, source research, contracts and QA context.

## Mission

Implement a provider-agnostic canonical model that preserves provenance and supports repeatable ingestion.

## Explore

Research current patterns for:
- raw vs normalized layers;
- source registries;
- provenance;
- revisions/vintages;
- idempotency/deduplication;
- schema evolution;
- snapshotting/checksums;
- data validation.

Choose deliberately and record an ADR if the decision is non-trivial.

## Implement

Models/migrations for:
- geography;
- data provider/source;
- source dataset/series;
- raw observation metadata;
- normalized price observation;
- normalized income observation;
- minimum wage observation;
- basket and basket items;
- methodology/version;
- ingestion run/status.

Avoid provider-specific columns in domain tables unless justified.

## Data maturity

Implement a way to distinguish `source_verified`, `normalized`, `estimated`, `missing` without pretending estimates equal direct observations.

## Tests

Normalization, units, duplicate handling, provenance propagation, idempotent rerun, invalid records and migrations.

Document how a new adapter is added without touching analytics.
