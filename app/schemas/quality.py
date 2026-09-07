from datetime import datetime

from pydantic import BaseModel


class QualityIssue(BaseModel):
    level: str  # "warning", "critical"
    category: str # "staleness", "anomaly", "completeness"
    message: str

class ValidationReport(BaseModel):
    is_healthy: bool
    last_evaluated: datetime
    issues: list[QualityIssue]

class IngestionStatusSummary(BaseModel):
    source_id: str
    last_run_status: str
    last_run_time: datetime | None

class QualityStatusResponse(BaseModel):
    report: ValidationReport
    ingestion_summary: list[IngestionStatusSummary]
