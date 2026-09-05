from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_missing_required_params():
    """Verify that omitting required parameters yields a 422 Unprocessable Entity."""
    response = client.get("/api/v1/affordability")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # FastAPI default validation error format

def test_api_invalid_date_format():
    """Verify that providing malformed dates yields a 422 rather than a 500 error."""
    response = client.get(
        "/api/v1/affordability?basket_id=test&geography_id=BR&income_basis=min&start_date=invalid-date"
    )
    assert response.status_code == 422
    data = response.json()
    assert "start_date" in str(data["detail"])

def test_api_not_found_geography(db_session):
    """Verify that an unknown geography yields a clean 404 (DomainException mapping)."""
    # Since we use db_session dependency override generally, we don't necessarily need it
    # if it just returns an empty result, but it should trigger a NotFoundException from the service.
    from app.api.dependencies.db import get_db
    from app.main import app as main_app
    from app.db.base import Base
    import app.models  # noqa

    from unittest.mock import MagicMock
    from app.services.analytics import AnalyticsService
    from app.core.exceptions import NotFoundException

    # Instead of hitting a real database for validation error checking,
    # mock the service to just throw the expected exception.
    mock_service = MagicMock(spec=AnalyticsService)
    mock_service.calculate_affordability.side_effect = NotFoundException("Geography UNKNOWN_GEO")

    # Override the service dependency directly
    from app.api.routes.affordability import get_analytics_service
    main_app.dependency_overrides[get_analytics_service] = lambda: mock_service

    response = client.get(
        "/api/v1/affordability?basket_id=test&geography_id=UNKNOWN_GEO&income_basis=min"
    )

    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "NOT_FOUND"

    main_app.dependency_overrides.clear()
