# API Reference

The PoderBR backend exposes a strictly typed, synchronous REST API. The core interaction is reading analytical calculations based on historical data.

## Core Endpoints

### `GET /api/v1/affordability`
Retrieves the affordability index (income burden) and purchasing power data for a specific basket and geography.

**Query Parameters:**
- `basket_id` (String): Identifier for the basket schema (e.g., `protein_v1`).
- `geography_id` (String): State or national ID (e.g., `BR`, `SP`).
- `income_basis` (String): Income identifier (e.g., `minimum_wage`).
- `start_date` (Date, optional): Format `YYYY-MM-DD`.
- `end_date` (Date, optional): Format `YYYY-MM-DD`.
- `base_date` (Date, optional): Defines the $t_0$ for the Purchasing Power Index. Defaults to the first fully valid month in the time series.

**Caching & Limits:**
- Response includes `Cache-Control: public, max-age=3600`.
- Rate limited via IP to `100 requests / minute`.

### `GET /api/v1/quality/status`
Returns the observable health of the statistical pipeline.

**Response payload:**
Includes a `report` on data staleness and anomaly checks, and an `ingestion_summary` tracking the latest runs of the data adapters. Used by the UI to progressively disclose upstream data issues.

### `GET /health`
Returns a 200 OK `{ "status": "ok", "version": "0.1.0" }`. Used for load balancer readiness probes.

## Error Handling
All API errors return a standard schema:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid geography_id provided."
  }
}
```
Standard codes: `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.
