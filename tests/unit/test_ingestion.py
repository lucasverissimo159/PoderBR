from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.ingestion.ibge import IbgeSidraAdapter
from app.ingestion.ipea import IpeadataAdapter
from app.models.core import IngestionRun, RawObservation


def test_ipeadata_adapter_fetch_and_run(db_session):
    adapter = IpeadataAdapter(db_session)

    mock_response_data = {
        "value": [
            {"VALDATA": "2024-01-01T00:00:00-03:00", "VALVALOR": 1412.0},
            {"VALDATA": "2024-02-01T00:00:00-03:00", "VALVALOR": 1412.0},
        ]
    }

    # Mock the HTTPX Client
    with patch("httpx.Client.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_response_data
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        # Test 1: Standard Run
        run = adapter.run(dry_run=False)
        assert run.status == "success"
        assert run.records_processed == 2

        # Verify Database contents
        obs = db_session.query(RawObservation).all()
        assert len(obs) == 2
        assert obs[0].geography_id == "BR"
        assert obs[0].value == 1412.0
        assert obs[0].unit == "BRL"

        # Test 2: Idempotency (Run again with same data)
        run2 = adapter.run(dry_run=False)
        assert run2.status == "success"
        assert run2.records_processed == 2

        # Should still only be 2 records in DB
        obs_after = db_session.query(RawObservation).all()
        assert len(obs_after) == 2


def test_ibge_adapter_date_parsing(db_session):
    adapter = IbgeSidraAdapter(db_session)
    assert adapter._parse_quarter("202401") == date(2024, 1, 1)
    assert adapter._parse_quarter("202402") == date(2024, 4, 1)
    assert adapter._parse_quarter("202403") == date(2024, 7, 1)
    assert adapter._parse_quarter("202404") == date(2024, 10, 1)

    with pytest.raises(ValueError):
        adapter._parse_quarter("INVALID")


def test_ibge_adapter_fetch_schema_drift(db_session):
    adapter = IbgeSidraAdapter(db_session)

    with patch("httpx.Client.get") as mock_get:
        mock_resp = MagicMock()
        # Return unexpected dict instead of list
        mock_resp.json.return_value = {"error": "unexpected format"}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        with pytest.raises(ValueError, match="Schema drift"):
            adapter.run(dry_run=False)

        # Verify run was marked as failed
        run = db_session.query(IngestionRun).first()
        assert run.status == "failed"
