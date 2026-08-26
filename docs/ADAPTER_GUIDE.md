# Ingestion Adapter Guide

This guide explains how to add a new data provider to PoderBR without breaking the analytics or presentation layers.

## The Adapter Pattern
An ingestion adapter is a script (usually in `app/ingestion/`) responsible for communicating with an external API (like IBGE SIDRA or Ipeadata), parsing the response, and saving it to the database.

## Rules for Adapters

1. **Write ONLY to `raw_observations`.**
   Never write directly to `normalized_prices` or `affordability_metrics`. Your job is extraction and basic loading (EL), not transformation (T).

2. **Register the Source.**
   Ensure the provider is registered in the `data_sources` table before inserting observations.

3. **Track the Run.**
   Create an `IngestionRun` record when the script starts, and update it to `success` or `failed` when it finishes. Link all extracted raw observations to this run ID.

4. **Handle Idempotency Gracefully.**
   The database enforces uniqueness on `(source_id, reference_date, geography_id)`. If you fetch historical data that has already been ingested, your script should either skip existing records or perform an upsert (`ON CONFLICT DO UPDATE`), but it should not crash.

5. **Do Not Normalize Geography.**
   If the source provides geography as a custom internal ID (e.g., IBGE's state code `35`), store `35` in `geography_id` in the `raw_observations` table. The normalization layer will map `35` to `SP`.

## Example Flow
1. Fetch data from `https://api.example.com/meat-prices`.
2. Parse JSON.
3. For each data point, create a `RawObservation` object.
4. `db.session.add_all(observations)`
5. `db.session.commit()`
