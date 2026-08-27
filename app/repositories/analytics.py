from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.core import (
    Basket,
    BasketItem,
    Geography,
    NormalizedIncome,
    NormalizedPrice,
)


class AnalyticsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_geography(self, geography_id: str) -> Geography | None:
        return self.session.get(Geography, geography_id)

    def get_basket_items(self, basket_id: str) -> list[BasketItem]:
        stmt = select(BasketItem).where(BasketItem.basket_id == basket_id)
        return list(self.session.scalars(stmt))

    def get_basket(self, basket_id: str) -> Basket | None:
        return self.session.get(Basket, basket_id)

    def get_normalized_prices(
        self,
        geography_id: str,
        item_ids: list[str],
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[NormalizedPrice]:
        stmt = select(NormalizedPrice).where(
            NormalizedPrice.geography_id == geography_id,
            NormalizedPrice.item_id.in_(item_ids),
        )
        if start_date:
            stmt = stmt.where(NormalizedPrice.reference_date >= start_date)
        if end_date:
            stmt = stmt.where(NormalizedPrice.reference_date <= end_date)

        return list(self.session.scalars(stmt))

    def get_normalized_incomes(
        self,
        geography_id: str,
        income_basis: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[NormalizedIncome]:
        stmt = select(NormalizedIncome).where(
            NormalizedIncome.geography_id == geography_id,
            NormalizedIncome.income_basis == income_basis,
        )
        if start_date:
            stmt = stmt.where(NormalizedIncome.reference_date >= start_date)
        if end_date:
            stmt = stmt.where(NormalizedIncome.reference_date <= end_date)

        return list(self.session.scalars(stmt))
