from datetime import date

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


class MockRepositoryForEngine:
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


def test_engine_hand_calculated_metrics():
    """
    Test scenario:
    Basket: 2kg beef, 1 dozen eggs
    Month 1 (Base): Beef=30, Eggs=10 -> Basket Cost = 2(30) + 1(10) = 70. Income = 700.
        Burden = 70/700 = 10%.
        Affordability = 700/70 = 10.
        PPI = 100.
    Month 2: Beef=40, Eggs=10 -> Basket Cost = 2(40) + 1(10) = 90. Income = 700.
        Burden = 90/700 = 12.86%.
        Affordability = 700/90 = 7.78.
        PPI = (7.78 / 10) * 100 = 77.8.
    """
    prices = [
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 1, 1),
            price_brl=30.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 1, 1),
            price_brl=10.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 2, 1),
            price_brl=40.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 2, 1),
            price_brl=10.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]
    incomes = [
        NormalizedIncome(
            reference_date=date(2024, 1, 1),
            income_brl=700.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]

    repo = MockRepositoryForEngine(prices, incomes)
    service = AnalyticsService(repo)
    req = AnalyticsRequest(
        basket_id="test",
        geography_id="BR",
        income_basis="min",
        base_date=date(2024, 1, 1),
    )

    res = service.calculate_affordability(req)

    m1 = res.data[0]
    assert m1.basket_cost == 70.0
    assert m1.income_burden_pct == 10.0
    assert m1.affordability_ratio == 10.0
    assert m1.purchasing_power_index == 100.0
    assert m1.quality_flag == "complete"

    m2 = res.data[1]
    assert m2.basket_cost == 90.0
    assert m2.income_burden_pct == 12.86
    assert m2.affordability_ratio == 7.78
    assert m2.purchasing_power_index == 77.78
    assert m2.quality_flag == "complete"


def test_engine_zero_income_handling():
    """Ensure zero income does not cause ZeroDivisionError, marks as error/partial."""
    prices = [
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 1, 1),
            price_brl=30.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 1, 1),
            price_brl=10.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]
    incomes = [
        NormalizedIncome(
            reference_date=date(2024, 1, 1),
            income_brl=0.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]

    repo = MockRepositoryForEngine(prices, incomes)
    service = AnalyticsService(repo)
    req = AnalyticsRequest(basket_id="test", geography_id="BR", income_basis="min")

    res = service.calculate_affordability(req)

    m1 = res.data[0]
    # Because income is 0, has_valid_income is False, meaning the metric defaults to partial/nulls
    assert m1.quality_flag == "partial"
    assert m1.basket_cost is None
    assert m1.income_burden_pct is None


def test_engine_partial_basket_handling():
    """Ensure missing price components yield null metrics."""
    prices = [
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 1, 1),
            price_brl=30.0,
            status=ObservationStatus.NORMALIZED,
        ),
        # Eggs are missing
    ]
    incomes = [
        NormalizedIncome(
            reference_date=date(2024, 1, 1),
            income_brl=700.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]

    repo = MockRepositoryForEngine(prices, incomes)
    service = AnalyticsService(repo)
    req = AnalyticsRequest(basket_id="test", geography_id="BR", income_basis="min")

    res = service.calculate_affordability(req)

    m1 = res.data[0]
    assert m1.quality_flag == "partial"
    assert m1.basket_cost is None
    assert m1.income_burden_pct is None
    assert m1.affordability_ratio is None
    assert m1.purchasing_power_index is None


def test_engine_quarterly_income_carry_forward():
    """Ensure quarterly income applies forward to the subsequent months in that quarter."""
    prices = [
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 1, 1),
            price_brl=30.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 1, 1),
            price_brl=10.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="beef",
            reference_date=date(2024, 2, 1),
            price_brl=30.0,
            status=ObservationStatus.NORMALIZED,
        ),
        NormalizedPrice(
            item_id="eggs",
            reference_date=date(2024, 2, 1),
            price_brl=10.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]
    incomes = [
        # Only Q1 data
        NormalizedIncome(
            reference_date=date(2024, 1, 1),
            income_brl=700.0,
            status=ObservationStatus.NORMALIZED,
        ),
    ]

    repo = MockRepositoryForEngine(prices, incomes)
    service = AnalyticsService(repo)
    req = AnalyticsRequest(basket_id="test", geography_id="BR", income_basis="min")

    res = service.calculate_affordability(req)

    assert len(res.data) == 2
    assert res.data[0].income == 700.0
    assert res.data[0].quality_flag == "complete"
    assert res.data[1].income == 700.0  # Carried forward to Feb
    assert res.data[1].quality_flag == "complete"
