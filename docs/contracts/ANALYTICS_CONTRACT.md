# Analytics Contract

This contract defines the mathematical operations performed in the Analytics domain.

## Formulas

See `docs/METHODOLOGY.md` for full mathematical definitions of:
1. Basket Cost
2. Income Burden
3. Affordability Ratio
4. Purchasing Power Index (PPI)

## Python Interface (Pydantic)
The Analytics domain must expose functions that accept and return strictly typed Pydantic models.

```python
from pydantic import BaseModel
from datetime import date
from typing import Dict, List, Optional

class AnalyticsRequest(BaseModel):
    basket_id: str
    geography_id: str
    income_basis: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    base_date: Optional[date] = None

class AffordabilityDataPoint(BaseModel):
    date: date
    basket_cost: Optional[float]
    income: float
    income_burden_pct: Optional[float]
    affordability_ratio: Optional[float]
    purchasing_power_index: Optional[float]
    quality_flag: str
    components: Dict[str, float]

class AffordabilityResponse(BaseModel):
    meta: dict
    data: List[AffordabilityDataPoint]
```
