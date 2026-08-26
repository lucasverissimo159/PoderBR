# Prompt 08 — Public Analytical API and Stable Contracts

Act as the API Agent.

Read API/data/analytics contracts and backend guidance.

## Mission

Expose analytical results without leaking database structure.

## Research

Investigate current practices for the selected framework around validation, OpenAPI, filtering, pagination, versioning, caching and error contracts.

## Implement

Design resources based on the real domain, potentially:
- `/geographies`
- `/proteins`
- `/baskets`
- `/income`
- `/prices`
- `/analytics/affordability`
- `/analytics/purchasing-power`
- `/analytics/comparison`
- `/methodology`
- `/sources`

Every analytical response should expose enough provenance/methodology information for the UI to remain honest.

Explicitly represent missing/estimated data.

## Tests

Contract tests, validation tests, integration tests and representative fixture-backed responses.

Update the canonical API contract before changing fields consumed by frontend agents.
