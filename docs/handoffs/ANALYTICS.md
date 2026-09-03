# Handoff: Analytics Phase

## Objective
Implement rigorous mathematical calculation of purchasing power metrics, taking care to isolate product scenarios from generalized welfare claims. Ensure extreme edge cases like zero income, division by zero, and missing basket elements are handled without interpolation, preserving data integrity.

## Decisions Made
- **Base Period Calculation:** The `Purchasing Power Index (PPI)` requires a base period where the index equals 100. If the user (`AnalyticsRequest`) does not explicitly provide a `base_date`, the engine dynamically calculates the first fully valid month (prices for all basket items + income > 0) to use as the base `Affordability Ratio`.
- **Zero Income Handling:** If income drops to 0 or is mathematically negative, it defaults the month's metrics to `null` and sets the `quality_flag` to `partial`, completely sidestepping `ZeroDivisionError`s without throwing 500 API errors.
- **Null Propagation:** Missing item prices propagate up to the top level. If 1 out of 4 items is missing, `basket_cost` becomes `null`. This enforces the "no fabricated data" directive.
- **Methodology Transparency:** Updated `METHODOLOGY.md` to explicitly declare that the basket is a "product scenario" and does not reflect generalized cost of living, protecting against inflated welfare claims.

## Evidence/Sources
- Common statistical practices for creating chained or fixed-base indexes.
- `AGENTS.md` directive limiting arbitrary extrapolation.

## Files Created/Changed
- `app/services/analytics.py`, `app/schemas/analytics.py`, `app/api/routes/affordability.py`
- `docs/METHODOLOGY.md`
- `docs/contracts/ANALYTICS_CONTRACT.md`, `docs/contracts/FRONTEND_BACKEND_CONTRACT.md`
- `tests/unit/test_analytics_engine.py`
- `docs/handoffs/ANALYTICS.md`

## Interfaces Changed
- Added `affordability_ratio`, `purchasing_power_index` to the output array.
- Added optional `base_date` to the input query string.

## Tests/Checks
- Hand-calculated test cases matching standard division algorithms.
- Edge case assertions guaranteeing 0 income or partial arrays return strict `None`.

## Limitations
- We still do not apply any basket weighting adjustments over time (e.g. substitution effects are ignored). The basket configuration is strictly static per version.

## Risks
- Depending on the frontend visualization library, `null` values passed down to the charts must be handled correctly (typically by breaking the line chart) rather than drawing lines down to $0.00.

## Next Tasks
1. `08 API`: Ensure standard middleware, rate limiting, and exact OpenAPI schema validation are perfect.
2. `09 Frontend`: Begin scaffolding the Vite/React application and pulling from the newly defined `AffordabilityResponse`.
