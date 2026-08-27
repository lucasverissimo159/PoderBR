from datetime import date

import pytest

from app.core.exceptions import NotFoundException
from app.models.core import (
    Basket,
    BasketItem,
    Geography,
    NormalizedIncome,
    NormalizedPrice,
    ObservationStatus,
)
from app.schemas.analytics import AnalyticsRequest
from app.services.analytics import AnalyticsService


class MockAnalyticsRepository:
    def get_geography(self, geography_id: str):
        if geography_id == "SP":
            return Geography(id="SP", name="São Paulo", level="state")
        return None

    def get_basket(self, basket_id: str):
        if basket_id == "protein":
            return Basket(
                id="protein", name="Protein Basket", description="...", is_active=True
            )
        return None

    def get_basket_items(self, basket_id: str):
        if basket_id == "protein":
            return [
                BasketItem(item_id="beef", quantity=5.0, unit="kg"),
                BasketItem(item_id="chicken", quantity=3.0, unit="kg"),
            ]
        return []

    def get_normalized_prices(self, geo_id, items, start, end):
        return [
            NormalizedPrice(
                item_id="beef",
                reference_date=date(2024, 1, 1),
                price_brl=30.0,
                status=ObservationStatus.NORMALIZED,
            ),
            NormalizedPrice(
                item_id="chicken",
                reference_date=date(2024, 1, 1),
                price_brl=15.0,
                status=ObservationStatus.NORMALIZED,
            ),
            # Missing beef in Feb
            NormalizedPrice(
                item_id="chicken",
                reference_date=date(2024, 2, 1),
                price_brl=16.0,
                status=ObservationStatus.NORMALIZED,
            ),
        ]

    def get_normalized_incomes(self, geo_id, basis, start, end):
        return [
            NormalizedIncome(
                reference_date=date(2024, 1, 1),
                income_brl=1412.0,
                status=ObservationStatus.NORMALIZED,
            ),
            NormalizedIncome(
                reference_date=date(2024, 2, 1),
                income_brl=1412.0,
                status=ObservationStatus.NORMALIZED,
            ),
        ]


def test_analytics_service_calculation_success():
    repo = MockAnalyticsRepository()
    service = AnalyticsService(repo)

    req = AnalyticsRequest(
        basket_id="protein", geography_id="SP", income_basis="min_wage"
    )
    res = service.calculate_affordability(req)

    assert res.meta.basket_id == "protein"
    assert res.meta.geography.name == "São Paulo"

    # We should have 2 data points (Jan and Feb)
    assert len(res.data) == 2

    jan_data = [d for d in res.data if d.date == date(2024, 1, 1)][0]
    # Basket cost: 5kg beef * 30.0 + 3kg chicken * 15.0 = 150 + 45 = 195
    assert jan_data.basket_cost == 195.0
    assert jan_data.income == 1412.0
    assert jan_data.quality_flag == "complete"
    assert round(jan_data.income_burden_pct, 2) == round((195.0 / 1412.0) * 100, 2)

    feb_data = [d for d in res.data if d.date == date(2024, 2, 1)][0]
    # Feb is missing beef, so it should be marked partial and cost not calculated (null)
    assert feb_data.quality_flag == "partial"
    assert feb_data.basket_cost is None


def test_analytics_service_not_found():
    repo = MockAnalyticsRepository()
    service = AnalyticsService(repo)

    req = AnalyticsRequest(
        basket_id="protein", geography_id="INVALID", income_basis="min_wage"
    )
    with pytest.raises(NotFoundException):
        service.calculate_affordability(req)
