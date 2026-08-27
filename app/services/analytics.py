from collections import defaultdict
from datetime import datetime
from typing import Any

from app.core.exceptions import NotFoundException, ValidationException
from app.models.core import ObservationStatus
from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import (
    AffordabilityDataPoint,
    AffordabilityMeta,
    AffordabilityResponse,
    AnalyticsRequest,
    GeographyMeta,
)


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    def calculate_affordability(self, req: AnalyticsRequest) -> AffordabilityResponse:
        """
        Calculates the affordability index (income burden) idempotently based on historical data.
        Returns a structured response matching FRONTEND_BACKEND_CONTRACT.md.
        """
        # 1. Validate dependencies (Geography, Basket)
        geo = self.repository.get_geography(req.geography_id)
        if not geo:
            raise NotFoundException(f"Geography {req.geography_id}")

        basket = self.repository.get_basket(req.basket_id)
        if not basket or not basket.is_active:
            raise NotFoundException(f"Basket {req.basket_id}")

        basket_items = self.repository.get_basket_items(req.basket_id)
        if not basket_items:
            raise ValidationException(f"Basket {req.basket_id} has no items.")

        item_quantities = {item.item_id: float(item.quantity) for item in basket_items}

        # 2. Fetch normalized data
        prices = self.repository.get_normalized_prices(
            req.geography_id, list(item_quantities.keys()), req.start_date, req.end_date
        )
        incomes = self.repository.get_normalized_incomes(
            req.geography_id, req.income_basis, req.start_date, req.end_date
        )

        # 3. Group data by reference_date
        # We need all prices and the income for a given month to calculate the burden.
        data_by_date: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"components": {}, "income": None}
        )

        for price in prices:
            date_str = price.reference_date.isoformat()
            if (
                price.status != ObservationStatus.MISSING
                and price.price_brl is not None
            ):
                data_by_date[date_str]["components"][price.item_id] = float(
                    price.price_brl
                )

        for income in incomes:
            date_str = income.reference_date.isoformat()
            if (
                income.status != ObservationStatus.MISSING
                and income.income_brl is not None
            ):
                data_by_date[date_str]["income"] = float(income.income_brl)

        # 4. Perform Domain Calculations
        response_data: list[AffordabilityDataPoint] = []

        for date_str in sorted(data_by_date.keys()):
            components = data_by_date[date_str]["components"]
            income_val = data_by_date[date_str]["income"]

            # Check if we have prices for ALL basket items
            is_complete = len(components) == len(item_quantities)

            if not is_complete or not income_val:
                # Based on rule: do not interpolate. Mark as partial/missing and return nulls, not 0.0.
                response_data.append(
                    AffordabilityDataPoint(
                        date=date_str,
                        basket_cost=None,
                        income=income_val or 0.0,
                        income_burden_pct=None,
                        quality_flag="partial",
                        components=components,
                    )
                )
                continue

            # Calculate Basket Cost: Sum(Price * Quantity)
            basket_cost = sum(
                components[item_id] * item_quantities[item_id] for item_id in components
            )

            # Calculate Burden
            burden_pct = (basket_cost / income_val) * 100

            response_data.append(
                AffordabilityDataPoint(
                    date=date_str,
                    basket_cost=round(basket_cost, 2),
                    income=round(income_val, 2),
                    income_burden_pct=round(burden_pct, 2),
                    quality_flag="complete",
                    components=components,
                )
            )

        # 5. Construct final schema
        return AffordabilityResponse(
            meta=AffordabilityMeta(
                basket_id=req.basket_id,
                geography=GeographyMeta(id=geo.id, name=geo.name),
                income_basis=req.income_basis,
                methodology_version="1.0",
                last_updated=datetime.now(),  # In a real scenario, take max(retrieved_at)
            ),
            data=response_data,
        )
