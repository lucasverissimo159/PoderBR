from collections import defaultdict
from datetime import date, datetime
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
        Calculates the affordability index (income burden) idempotently based on
        historical data.
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

        # Because income data (like PNAD) might be quarterly, we need a smarter
        # strategy. We find the latest available income that applies to each month.
        sorted_incomes = sorted(
            [
                i
                for i in incomes
                if i.status != ObservationStatus.MISSING and i.income_brl is not None
            ],
            key=lambda x: x.reference_date,
        )

        # We assume an income value applies forward until a new value is recorded.
        def get_applicable_income(target_date: date) -> float | None:
            applicable = None
            for inc in sorted_incomes:
                if inc.reference_date <= target_date:
                    applicable = float(inc.income_brl)
                else:
                    break
            return applicable

        for price in prices:
            date_str = price.reference_date.isoformat()
            if (
                price.status != ObservationStatus.MISSING
                and price.price_brl is not None
            ):
                data_by_date[date_str]["components"][price.item_id] = float(
                    price.price_brl
                )

        # Now backfill the applicable income for every month we have price data
        for d_str in data_by_date.keys():
            d_obj = datetime.fromisoformat(d_str).date()
            data_by_date[d_str]["income"] = get_applicable_income(d_obj)

        # 4. Perform Domain Calculations
        response_data: list[AffordabilityDataPoint] = []

        base_date_str = req.base_date.isoformat() if req.base_date else None
        base_affordability_ratio = None

        # First Pass: Identify valid base date and its affordability ratio
        sorted_dates = sorted(data_by_date.keys())

        # If no base_date specified, try to find the first complete month
        if not base_date_str:
            for d_str in sorted_dates:
                comps = data_by_date[d_str]["components"]
                inc = data_by_date[d_str]["income"]
                if len(comps) == len(item_quantities) and inc and inc > 0:
                    base_date_str = d_str
                    break

        # Calculate base_affordability_ratio if base_date is valid
        if base_date_str and base_date_str in data_by_date:
            b_comps = data_by_date[base_date_str]["components"]
            b_inc = data_by_date[base_date_str]["income"]
            if len(b_comps) == len(item_quantities) and b_inc and b_inc > 0:
                b_cost = sum(
                    b_comps[item_id] * item_quantities[item_id] for item_id in b_comps
                )
                base_affordability_ratio = b_inc / b_cost

        # Second Pass: Calculate all metrics
        for date_str in sorted_dates:
            components = data_by_date[date_str]["components"]
            income_val = data_by_date[date_str]["income"]

            # Check if we have prices for ALL basket items and income > 0
            is_complete = len(components) == len(item_quantities)
            has_valid_income = income_val is not None and income_val > 0

            if not is_complete or not has_valid_income:
                # Based on rule: do not interpolate. Mark as partial/missing
                # and return nulls.
                response_data.append(
                    AffordabilityDataPoint(
                        date=date_str,
                        basket_cost=None,
                        income=income_val or 0.0,
                        income_burden_pct=None,
                        affordability_ratio=None,
                        purchasing_power_index=None,
                        quality_flag="partial",
                        components=components,
                    )
                )
                continue

            # Calculate Basket Cost: Sum(Price * Quantity)
            basket_cost = sum(
                components[item_id] * item_quantities[item_id] for item_id in components
            )

            # Guard against zero basket cost to prevent division by zero
            if basket_cost <= 0:
                response_data.append(
                    AffordabilityDataPoint(
                        date=date_str,
                        basket_cost=0.0,
                        income=income_val,
                        income_burden_pct=0.0,
                        affordability_ratio=None,
                        purchasing_power_index=None,
                        quality_flag="error",
                        components=components,
                    )
                )
                continue

            # Calculate Metrics
            burden_pct = (basket_cost / income_val) * 100
            affordability_ratio = income_val / basket_cost

            ppi = None
            if base_affordability_ratio is not None:
                # PPI = (Current Affordability / Base Affordability) * 100
                ppi = (affordability_ratio / base_affordability_ratio) * 100

            response_data.append(
                AffordabilityDataPoint(
                    date=date_str,
                    basket_cost=round(basket_cost, 2),
                    income=round(income_val, 2),
                    income_burden_pct=round(burden_pct, 2),
                    affordability_ratio=round(affordability_ratio, 2),
                    purchasing_power_index=round(ppi, 2) if ppi is not None else None,
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
                # In a real scenario, take max(retrieved_at)
                last_updated=datetime.now(),
            ),
            data=response_data,
        )
