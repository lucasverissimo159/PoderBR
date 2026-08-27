from datetime import date

from fastapi.testclient import TestClient

from app.api.dependencies.db import get_db
from app.main import app
from app.models.core import (
    Basket,
    BasketItem,
    Geography,
    NormalizedIncome,
    NormalizedPrice,
    ObservationStatus,
)

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_affordability_integration(db_session):
    # Override dependency
    app.dependency_overrides[get_db] = lambda: db_session

    # Setup DB
    geo = Geography(id="BR", name="Brasil", level="national")
    basket = Basket(id="test_basket", name="Test", description="Test", is_active=True)
    b_item = BasketItem(
        basket_id="test_basket", item_id="beef", quantity=1.0, unit="kg"
    )

    price = NormalizedPrice(
        item_id="beef",
        reference_date=date(2024, 1, 1),
        geography_id="BR",
        price_brl=40.0,
        unit="kg",
        status=ObservationStatus.NORMALIZED,
    )
    income = NormalizedIncome(
        income_basis="min_wage",
        reference_date=date(2024, 1, 1),
        geography_id="BR",
        income_brl=1000.0,
        status=ObservationStatus.NORMALIZED,
    )

    db_session.add_all([geo, basket, b_item, price, income])
    db_session.commit()

    # Must explicitly unexpire/refresh OR simply query inside the same session block
    db_session.refresh(geo)
    db_session.refresh(basket)

    # Request API
    response = client.get(
        "/api/v1/affordability?basket_id=test_basket&geography_id=BR&income_basis=min_wage"
    )
    assert response.status_code == 200

    data = response.json()
    assert data["meta"]["basket_id"] == "test_basket"
    assert len(data["data"]) == 1

    point = data["data"][0]
    assert point["basket_cost"] == 40.0
    assert point["income"] == 1000.0
    assert point["income_burden_pct"] == 4.0
    assert point["quality_flag"] == "complete"

    # Cleanup override
    app.dependency_overrides.clear()
