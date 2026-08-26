# Data Dictionary

This document defines the core data structures for ingestion and analytics in PoderBR.

## 1. Raw Observations
The `raw_observations` table stores data exactly as received from APIs before any transformation.
- `id` (UUID): Primary key.
- `source_id` (String): e.g., 'ibge_sidra_1737', 'ipea_MTE12_SALMIN12'.
- `provider` (String): 'ibge', 'ipeadata', 'cepea'.
- `dataset_ref` (String): The table or series code.
- `geography_id` (String): Original geography code from the source (e.g., IBGE State Code '35').
- `geography_level` (String): 'national', 'state', 'metropolitan_area'.
- `reference_date` (Date): The month/quarter the data represents.
- `value` (Numeric): The raw numerical value.
- `unit` (String): 'BRL', 'Index', 'Percentage', 'R$/kg'.
- `retrieval_timestamp` (DateTime): When the agent/system fetched the data.

## 2. Normalized Prices
The `normalized_prices` table holds cleaned, comparable nominal prices for the basket items.
- `item_id` (String): 'beef', 'pork', 'chicken', 'eggs'.
- `reference_date` (Date): First day of the reference month.
- `geography_id` (String): Canonical state or national code (e.g., 'BR', 'SP').
- `nominal_price` (Numeric): The exact monetary value in the currency of the time.
- `currency` (String): 'BRL' (Real), 'BRR' (Cruzeiro Real), etc. For the MVP, we only handle BRL (post-1994).
- `price_unit` (String): Always normalized to 'kg' for meat and 'dozen' for eggs.
- `source_observation_id` (UUID): Foreign key to `raw_observations`.

## 3. Analytics Output
The `affordability_metrics` table holds calculated indicators.
- `reference_date` (Date).
- `geography_id` (String).
- `income_basis` (String): 'minimum_wage', 'average_income'.
- `basket_version` (String): e.g., 'v1.0'.
- `basket_cost_nominal` (Numeric).
- `income_nominal` (Numeric).
- `income_burden_pct` (Numeric): `(basket_cost_nominal / income_nominal) * 100`.
- `data_quality_flag` (String): 'complete', 'partial', 'estimated'.
