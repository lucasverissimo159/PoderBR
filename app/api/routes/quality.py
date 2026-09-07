from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.dependencies.db import get_db
from app.core.security import limiter
from app.schemas.quality import QualityStatusResponse
from app.services.quality import QualityService

router = APIRouter()

def get_quality_service(db: Session = Depends(get_db)) -> QualityService:
    return QualityService(db)

@router.get("/status", response_model=QualityStatusResponse)
@limiter.limit("10/minute")
def get_quality_status(
    request: Request,
    service: QualityService = Depends(get_quality_service)
):
    """
    Returns the observable health of the statistical pipeline.
    This includes staleness checks, anomaly flags, and recent ingestion run history.
    """
    return service.generate_report()
