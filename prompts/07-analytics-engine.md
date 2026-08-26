# Prompt 07 — Purchasing-Power Analytics Engine

Act as the Analytics Agent. This is mathematically and methodologically sensitive.

Read methodology, data contracts, data sources, architecture and analytics context.

## Research

Verify economic/statistical conventions before implementation. Compare alternatives where the metric could be defined multiple ways.

## Metrics

Implement only justified metrics, potentially including:
- unit protein cost;
- basket cost;
- income burden;
- affordability ratio;
- quantity purchasable;
- purchasing-power index vs declared base;
- nominal vs real comparisons;
- controlled decomposition/sensitivity analysis.

## Basket

Make composition versioned/configurable. Research whether a reference basket can be justified; otherwise present the basket as a product scenario rather than a universal consumption truth.

## Requirements

Every metric must declare:
- formula;
- units;
- time basis;
- income basis;
- basket/methodology version;
- interpretation;
- invalid/missing cases.

Round only at presentation boundaries.

## Tests

Known hand-calculated cases, unit conversions, zero/negative invalids, missing/partial baskets, base-period consistency, sensitivity and regression tests.

Update `docs/METHODOLOGY.md` with equations and caveats.
