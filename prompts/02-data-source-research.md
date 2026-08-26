# Prompt 02 — Public Data Research, Historical Coverage and Licensing

Act as the Data Research Agent. This is research-heavy; do not implement live ingestion.

Read `AGENTS.md`, `docs/PROJECT_CONTEXT.md`, `agent-context/data.md`, current ADRs.

## Mission

Find defensible historical data strategies for:
- beef, pork, chicken and eggs prices;
- income by geography;
- national minimum wage;
- inflation/deflators;
- geography metadata.

## Required research

Start with official/current primary sources. Investigate IBGE/SIDRA and other credible Brazilian statistical/public providers. Examine APIs, downloadable tables and machine-readable endpoints.

For every candidate source document:
- provider;
- table/series/dataset id;
- stable URL/documentation;
- geography;
- frequency;
- historical coverage;
- unit;
- whether it is a price level or index;
- revision/vintage behavior;
- access constraints;
- license/attribution requirements when visible;
- reproducibility concerns;
- suitability score.

## Compare strategies

At least three:
1. direct nominal price levels;
2. source price levels plus explicit official inflation adjustment;
3. mixed-source strategy with documented comparability limitations.

Explain which comparisons are valid and which are not. Investigate whether state-level coverage really exists or whether the correct MVP scope is capitals/research areas.

## Deliverables

Create/update:
- `docs/DATA_SOURCES.md`
- `docs/DATA_DICTIONARY.md`
- `docs/GEOGRAPHIC_COVERAGE.md`
- `docs/DATA_LICENSES.md`
- `docs/adr/0003-data-source-selection.md`
- `docs/handoffs/DATA-RESEARCH.md`

Do not silently fill geographic or temporal gaps. Recommend the smallest defensible MVP coverage.
