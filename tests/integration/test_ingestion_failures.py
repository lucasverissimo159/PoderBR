import pytest
from httpx import Response, Request, TimeoutException
from app.ingestion.ibge import IbgeSidraAdapter
from app.models.core import IngestionRun, RawObservation


def test_ibge_adapter_network_timeout(db_session, monkeypatch):
    """
    Simulate a network timeout during ingestion.
    The adapter should gracefully catch it, fail the ingestion run deterministically,
    and not corrupt the database with partial raw observations.
    """
    def mock_get(*args, **kwargs):
        raise TimeoutException("Connection timed out", request=Request("GET", "https://test"))

    # We mock the httpx.Client.get method
    monkeypatch.setattr("httpx.Client.get", mock_get)

    adapter = IbgeSidraAdapter(db_session)

    with pytest.raises(TimeoutException):
        adapter.run()

    # Verify no raw observations were inserted due to failure
    obs_count = db_session.query(RawObservation).count()
    assert obs_count == 0

    # Verify the failure run was logged properly (if the adapter handles it)
    # The current BaseAdapter.run does not catch exceptions around fetch_data,
    # it lets them bubble up for the cron to handle. But it creates the run first.
    # Actually, the BaseAdapter wraps fetch_data in a transaction but doesn't swallow exceptions.

    # We expect an ingestion run to be created but not marked 'success'
    run = db_session.query(IngestionRun).first()
    assert run is not None
    assert run.status == "failed"  # The base adapter handles setting it to failed


def test_ibge_adapter_schema_drift(db_session, monkeypatch):
    """
    Simulate upstream schema drift (invalid JSON structure).
    The adapter should fail predictably during extraction/normalization.
    """
    def mock_get(*args, **kwargs):
        # Provide a JSON that doesn't match the expected IBGE SIDRA format
        return Response(
            status_code=200,
            json={"unexpected_key": "value"},
            request=Request("GET", "https://test")
        )

    monkeypatch.setattr("httpx.Client.get", mock_get)

    adapter = IbgeSidraAdapter(db_session)

    # The adapter validates if it's a non-empty list. If we pass invalid structure,
    # it raises ValueError or yields empty. Here, we test a structure that passes
    # the top level list check but has wrong internal dictionary keys (like missing "resultados")
    # Actually, the code handles missing "resultados" gracefully by yielding nothing.
    # To cause a failure, let's pass a dict instead of a list.
    with pytest.raises(ValueError, match="Schema drift: IBGE SIDRA returned empty or non-list data"):
        adapter.run()

    # Database must remain uncorrupted
    obs_count = db_session.query(RawObservation).count()
    assert obs_count == 0
