from datetime import date

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.dependencies.db import get_db
from app.core.security import limiter
from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import AffordabilityResponse, AnalyticsRequest
from app.services.analytics import AnalyticsService

router = APIRouter()


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    repository = AnalyticsRepository(db)
    return AnalyticsService(repository)


@router.get("/affordability", response_model=AffordabilityResponse)
@limiter.limit("100/minute")
def get_affordability(
    request: Request,
    response: Response,
    basket_id: str,
    geography_id: str,
    income_basis: str,
    start_date: date | None = None,
    end_date: date | None = None,
    base_date: date | None = None,
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Retrieve the affordability index (income burden) for a specific basket
    and geography.
    """
    # In a real app this is data that changes once a month.
    # Caching it for 1 hour locally/in CDNs is extremely safe.
    response.headers["Cache-Control"] = "public, max-age=3600"

    req = AnalyticsRequest(
        basket_id=basket_id,
        geography_id=geography_id,
        income_basis=income_basis,
        start_date=start_date,
        end_date=end_date,
        base_date=base_date,
    )
    return service.calculate_affordability(req)
