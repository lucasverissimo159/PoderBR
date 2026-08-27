from datetime import date, datetime

from pydantic import BaseModel


class GeographyMeta(BaseModel):
    id: str
    name: str


class AffordabilityMeta(BaseModel):
    basket_id: str
    geography: GeographyMeta
    income_basis: str
    methodology_version: str
    last_updated: datetime


class AffordabilityDataPoint(BaseModel):
    date: date
    basket_cost: float | None
    income: float
    income_burden_pct: float | None
    quality_flag: str
    components: dict[str, float]


class AffordabilityResponse(BaseModel):
    meta: AffordabilityMeta
    data: list[AffordabilityDataPoint]


class AnalyticsRequest(BaseModel):
    """Internal DTO for passing request params to the service layer"""

    basket_id: str
    geography_id: str
    income_basis: str
    start_date: date | None = None
    end_date: date | None = None
