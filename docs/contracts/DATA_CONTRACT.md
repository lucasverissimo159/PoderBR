# Data Contract

This contract defines the internal data models representing the database schema (SQLAlchemy/Alembic). Any change to these models requires an Alembic migration.

## Model: `RawObservation`
- `id`: UUID (PK)
- `source_provider`: VARCHAR (e.g., 'cepea', 'ibge')
- `source_dataset_id`: VARCHAR
- `reference_date`: DATE
- `geography_id`: VARCHAR
- `raw_value`: NUMERIC
- `raw_unit`: VARCHAR
- `retrieved_at`: TIMESTAMP

## Model: `NormalizedPrice`
- `id`: UUID (PK)
- `item_id`: VARCHAR (e.g., 'beef')
- `reference_date`: DATE
- `geography_id`: VARCHAR
- `price_brl`: NUMERIC
- `unit`: VARCHAR (e.g., 'kg')
- `raw_observation_id`: UUID (FK)

## Model: `NormalizedIncome`
- `id`: UUID (PK)
- `income_basis`: VARCHAR (e.g., 'minimum_wage')
- `reference_date`: DATE
- `geography_id`: VARCHAR
- `income_brl`: NUMERIC
- `raw_observation_id`: UUID (FK)
