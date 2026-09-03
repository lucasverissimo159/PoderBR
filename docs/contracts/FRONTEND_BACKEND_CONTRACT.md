# Frontend-Backend Contract

This contract defines the core HTTP APIs exposed by the backend to the frontend.

## Endpoint: `GET /api/v1/affordability`

**Query Parameters:**
- `basket_id` (String): e.g., 'protein_v1'
- `geography_id` (String): e.g., 'BR', 'SP'
- `income_basis` (String): e.g., 'minimum_wage', 'average_income'
- `start_date` (Date, optional): YYYY-MM-DD
- `end_date` (Date, optional): YYYY-MM-DD
- `base_date` (Date, optional): YYYY-MM-DD (Defaults to first available date)

**Response (200 OK):**
```json
{
  "meta": {
    "basket_id": "protein_v1",
    "geography": { "id": "SP", "name": "São Paulo" },
    "income_basis": "minimum_wage",
    "methodology_version": "1.0",
    "last_updated": "2024-05-15T10:00:00Z"
  },
  "data": [
    {
      "date": "2024-01-01",
      "basket_cost": 250.50,
      "income": 1412.00,
      "income_burden_pct": 17.74,
      "affordability_ratio": 5.63,
      "purchasing_power_index": 100.0,
      "quality_flag": "complete",
      "components": {
        "beef": 150.00,
        "pork": 50.50,
        "chicken": 30.00,
        "eggs": 20.00
      }
    }
    // ... historic data points
  ]
}
```

## Error Handling
All API errors must return a standard schema:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid geography_id provided."
  }
}
```
