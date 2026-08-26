from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.core import (
    DataSource,
    Geography,
    IngestionRun,
    NormalizedPrice,
    ObservationStatus,
    RawObservation,
)


def test_idempotency_raw_observations(db_session):
    # Setup baseline data
    source = DataSource(
        id="ibge_test", provider="IBGE", dataset_name="Test", url="http://test.com"
    )
    run = IngestionRun(source_id=source.id, status="success")
    db_session.add_all([source, run])
    db_session.commit()

    # Insert first observation
    obs1 = RawObservation(
        source_id=source.id,
        geography_id="35",
        reference_date=date(2024, 1, 1),
        value=100.5,
        unit="R$",
        run_id=run.id,
    )
    db_session.add(obs1)
    db_session.commit()

    # Attempt to insert duplicate observation (same source, date, geo)
    obs2 = RawObservation(
        source_id=source.id,
        geography_id="35",
        reference_date=date(2024, 1, 1),
        value=101.0,
        unit="R$",
        run_id=run.id,
    )
    db_session.add(obs2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_data_maturity_status(db_session):
    geo = Geography(id="BR", name="Brasil", level="national")
    db_session.add(geo)
    db_session.commit()

    # Valid normalized price
    price = NormalizedPrice(
        item_id="beef",
        reference_date=date(2024, 1, 1),
        geography_id="BR",
        price_brl=35.0,
        unit="kg",
        status=ObservationStatus.NORMALIZED,
    )
    db_session.add(price)
    db_session.commit()

    assert price.status == ObservationStatus.NORMALIZED

    # Missing price
    missing_price = NormalizedPrice(
        item_id="pork",
        reference_date=date(2024, 1, 1),
        geography_id="BR",
        price_brl=None,
        unit="kg",
        status=ObservationStatus.MISSING,
    )
    db_session.add(missing_price)
    db_session.commit()

    assert missing_price.status == ObservationStatus.MISSING
    assert missing_price.price_brl is None
