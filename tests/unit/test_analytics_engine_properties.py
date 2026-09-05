from datetime import date
from hypothesis import given, strategies as st
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


class MockRepositoryForFuzzing:
    def __init__(self, prices, incomes):
        self._prices = prices
        self._incomes = incomes

    def get_geography(self, geography_id: str):
        return Geography(id=geography_id, name="Test Geo", level="national")

    def get_basket(self, basket_id: str):
        return Basket(id=basket_id, name="Test", description="...", is_active=True)

    def get_basket_items(self, basket_id: str):
        # A simple basket: 2kg of beef, 1 dozen eggs
        return [
            BasketItem(item_id="beef", quantity=2.0, unit="kg"),
            BasketItem(item_id="eggs", quantity=1.0, unit="dozen"),
        ]

    def get_normalized_prices(self, geo_id, items, start, end):
        return self._prices

    def get_normalized_incomes(self, geo_id, basis, start, end):
        return self._incomes


@given(
    beef_price=st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False),
    eggs_price=st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False),
    income=st.floats(min_value=-1000.0, max_value=1e9, allow_nan=False, allow_infinity=False),
)
def test_analytics_fuzzing(beef_price, eggs_price, income):
    """
    Fuzz test the core AnalyticsService calculator.
    It must never crash on zero/negative values, merely return 'missing' or 'partial' state.
    """
    prices = [
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 1, 1),
            price_brl=beef_price,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 1, 1),
            price_brl=eggs_price,
            status=ObservationStatus.NORMALIZED,
        ),
    ]
    incomes = [
        NormalizedIncome(
            reference_date=date(2024, 1, 1),
            income_brl=income,
            status=ObservationStatus.NORMALIZED,
        ),
    ]

    repo = MockRepositoryForFuzzing(prices, incomes)
    service = AnalyticsService(repo)
    req = AnalyticsRequest(
        basket_id="test",
        geography_id="BR",
        income_basis="min",
        base_date=date(2024, 1, 1),
    )

    # Should not raise ZeroDivisionError or unhandled exceptions
    res = service.calculate_affordability(req)

    assert len(res.data) == 1
    point = res.data[0]

    basket_cost = (beef_price * 2.0) + (eggs_price * 1.0)

    if income <= 0:
        # Invalid income -> partial data, no burden/ppi
        assert point.quality_flag == "partial"
        assert point.income_burden_pct is None
        assert point.affordability_ratio is None
    elif basket_cost <= 0:
        # Invalid cost
        assert point.quality_flag == "error"
        assert point.income_burden_pct == 0.0
        assert point.affordability_ratio is None
    else:
        # Valid income and valid cost
        assert point.quality_flag == "complete"
        assert point.basket_cost is not None
        assert point.income_burden_pct is not None
        assert point.affordability_ratio is not None
