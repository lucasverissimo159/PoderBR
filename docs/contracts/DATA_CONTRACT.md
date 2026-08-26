# Data Contract

## Observation identity

Required conceptual keys:
- provider/source dataset
- geography
- period/date
- protein/measure
- unit

## Required metadata

- provider
- dataset/series id
- source geography id
- retrieval timestamp
- observation status
- methodology version where derived
- revision/vintage information when available

## Rules

No consumer may infer unavailable observations as zero. Unit conversions must be explicit and tested. Source-specific fields stay outside the canonical contract unless documented.
