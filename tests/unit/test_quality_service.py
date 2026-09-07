from datetime import datetime, timedelta

from app.models.core import DataSource, IngestionRun, NormalizedPrice, ObservationStatus
from app.services.quality import QualityService


def test_quality_service_healthy(db_session):
    service = QualityService(db_session)

    # Setup healthy data
    today = datetime.now().date()
    p1 = NormalizedPrice(
        item_id="beef",
        reference_date=today,
        geography_id="BR",
        price_brl=30.0,
        status=ObservationStatus.NORMALIZED
    )
    p2 = NormalizedPrice(
        item_id="beef",
        reference_date=today - timedelta(days=30),
        geography_id="BR",
        price_brl=29.0, # Normal MoM change
        status=ObservationStatus.NORMALIZED
    )

    ds = DataSource(id="test_ds", provider="test", dataset_name="test", url="test")
    run = IngestionRun(source_id="test_ds", status="success", started_at=datetime.now(), completed_at=datetime.now())

    db_session.add_all([p1, p2, ds, run])
    db_session.commit()

    res = service.generate_report()
    assert res.report.is_healthy is True
    assert len(res.report.issues) == 0
    assert len(res.ingestion_summary) == 1
    assert res.ingestion_summary[0].last_run_status == "success"

def test_quality_service_staleness(db_session):
    service = QualityService(db_session)

    # Setup stale data
    stale_date = datetime.now().date() - timedelta(days=60)
    p1 = NormalizedPrice(
        item_id="beef",
        reference_date=stale_date,
        geography_id="BR",
        price_brl=30.0,
        status=ObservationStatus.NORMALIZED
    )
    db_session.add(p1)
    db_session.commit()

    res = service.generate_report()
    # Not critically unhealthy, but has a staleness warning
    assert res.report.is_healthy is True
    assert len(res.report.issues) == 1
    assert res.report.issues[0].category == "staleness"

def test_quality_service_anomaly_spike(db_session):
    service = QualityService(db_session)

    # Setup spike data (> 50% jump)
    today = datetime.now().date()
    p1 = NormalizedPrice(
        item_id="beef",
        reference_date=today,
        geography_id="BR",
        price_brl=60.0, # 100% jump
        status=ObservationStatus.NORMALIZED
    )
    p2 = NormalizedPrice(
        item_id="beef",
        reference_date=today - timedelta(days=30),
        geography_id="BR",
        price_brl=30.0,
        status=ObservationStatus.NORMALIZED
    )

    db_session.add_all([p1, p2])
    db_session.commit()

    res = service.generate_report()

    # Spikes are warnings, not strictly unhealthy (as real prices can spike)
    assert res.report.is_healthy is True
    anomaly_issues = [i for i in res.report.issues if i.category == "anomaly"]
    assert len(anomaly_issues) == 1
    assert "Spike >50%" in anomaly_issues[0].message
