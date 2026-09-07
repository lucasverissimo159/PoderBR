from datetime import datetime, timedelta

from collections import defaultdict

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.core import DataSource, IngestionRun, NormalizedPrice, ObservationStatus
from app.schemas.quality import (
    IngestionStatusSummary,
    QualityIssue,
    QualityStatusResponse,
    ValidationReport,
)


class QualityService:
    def __init__(self, db: Session):
        self.db = db

    def generate_report(self) -> QualityStatusResponse:
        issues: list[QualityIssue] = []
        is_healthy = True

        # 1. Staleness Check
        # Check if the latest NormalizedPrice is older than 45 days
        latest_price = self.db.scalars(
            select(NormalizedPrice)
            .where(NormalizedPrice.status != ObservationStatus.MISSING)
            .order_by(desc(NormalizedPrice.reference_date))
            .limit(1)
        ).first()

        if latest_price:
            days_stale = (datetime.now().date() - latest_price.reference_date).days
            if days_stale > 45:
                issues.append(QualityIssue(
                    level="warning",
                    category="staleness",
                    message=f"Latest normalized price is {days_stale} days old (Threshold: 45)."
                ))
        else:
            issues.append(QualityIssue(
                level="critical",
                category="completeness",
                message="No normalized prices found in the database."
            ))
            is_healthy = False

        # 2. Anomaly Check (>50% MoM change in prices over the last 6 months)
        six_months_ago = datetime.now().date() - timedelta(days=180)
        recent_prices = self.db.scalars(
            select(NormalizedPrice)
            .where(NormalizedPrice.reference_date >= six_months_ago)
            .where(NormalizedPrice.status != ObservationStatus.MISSING)
            .order_by(NormalizedPrice.item_id, NormalizedPrice.reference_date)
        ).all()

        # Convert to a dictionary grouped by item_id to calculate MoM locally
        if recent_prices:
            # Check for negative prices while grouping
            grouped_prices = defaultdict(list)
            for p in recent_prices:
                price_val = float(p.price_brl) if p.price_brl is not None else 0.0
                if price_val < 0 and is_healthy:
                    issues.append(QualityIssue(
                        level="critical",
                        category="anomaly",
                        message="Negative prices detected in the normalized dataset."
                    ))
                    is_healthy = False
                grouped_prices[p.item_id].append(price_val)

            # Check MoM spikes manually
            for item_id, prices_list in grouped_prices.items():
                for i in range(1, len(prices_list)):
                    prev = prices_list[i-1]
                    curr = prices_list[i]
                    if prev > 0:
                        pct_change = abs((curr - prev) / prev)
                        if pct_change > 0.5:
                            issues.append(QualityIssue(
                                level="warning",
                                category="anomaly",
                                message=f"Spike >50% detected in {item_id} prices over the last 6 months."
                            ))
                            break # Only record one spike issue per item to avoid spam

        # 3. Ingestion Summary
        sources = self.db.scalars(select(DataSource)).all()
        ingestion_summary = []
        for s in sources:
            latest_run = self.db.scalars(
                select(IngestionRun)
                .where(IngestionRun.source_id == s.id)
                .order_by(desc(IngestionRun.started_at))
                .limit(1)
            ).first()

            if latest_run:
                ingestion_summary.append(IngestionStatusSummary(
                    source_id=s.id,
                    last_run_status=latest_run.status,
                    last_run_time=latest_run.completed_at or latest_run.started_at
                ))
                if latest_run.status == "failed":
                    issues.append(QualityIssue(
                        level="warning",
                        category="completeness",
                        message=f"Latest ingestion run for {s.id} failed."
                    ))
            else:
                ingestion_summary.append(IngestionStatusSummary(
                    source_id=s.id,
                    last_run_status="none",
                    last_run_time=None
                ))

        return QualityStatusResponse(
            report=ValidationReport(
                is_healthy=is_healthy,
                last_evaluated=datetime.now(),
                issues=issues
            ),
            ingestion_summary=ingestion_summary
        )
