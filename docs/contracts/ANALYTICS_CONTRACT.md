# Analytics Contract

This contract defines the mathematical operations performed in the Analytics domain.

## Formulas

1.  **Basket Cost:**
    ```text
    basket_cost(date, geography) = Σ (item_quantity * normalized_price(item, date, geography))
    ```

2.  **Income Burden:**
    ```text
    income_burden_pct(date, geography) = (basket_cost / income(date, geography)) * 100
    ```

## Python Interface (Pydantic)
The Analytics domain must expose functions that accept and return strictly typed Pydantic models.

```python
from pydantic import BaseModel
from datetime import date

class AnalyticsRequest(BaseModel):
    basket_id: str
    geography_id: str
    target_date: date

class AffordabilityResult(BaseModel):
    date: date
    basket_cost: float
    income: float
    burden_pct: float
    is_partial: bool
```
