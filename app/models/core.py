import enum
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class ObservationStatus(enum.Enum):
    SOURCE_VERIFIED = "source_verified"
    NORMALIZED = "normalized"
    ESTIMATED = "estimated"
    MISSING = "missing"


def generate_uuid():
    return str(uuid.uuid4())


class Geography(Base):
    __tablename__ = "geography"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g. 'BR', 'SP'
    name: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g. 'national', 'state'


class DataSource(Base):
    """Registry of official data sources (e.g., IBGE, CEPEA)"""

    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g. 'ibge_10280'
    provider: Mapped[str] = mapped_column(String, nullable=False)  # e.g. 'IBGE'
    dataset_name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)  # 'success', 'failed'
    records_processed: Mapped[int] = mapped_column(default=0)


class RawObservation(Base):
    __tablename__ = "raw_observations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    geography_id: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Original source code
    reference_date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    run_id: Mapped[str] = mapped_column(ForeignKey("ingestion_runs.id"))

    # Idempotency: We should only have one raw observation per source, date, and geography.
    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "reference_date",
            "geography_id",
            name="uq_raw_obs_source_date_geo",
        ),
    )


class NormalizedPrice(Base):
    __tablename__ = "normalized_prices"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    item_id: Mapped[str] = mapped_column(String, nullable=False)  # 'beef', 'chicken'
    reference_date: Mapped[date] = mapped_column(Date, nullable=False)
    geography_id: Mapped[str] = mapped_column(ForeignKey("geography.id"))
    price_brl: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    unit: Mapped[str] = mapped_column(String, nullable=False, default="kg")
    status: Mapped[ObservationStatus] = mapped_column(
        Enum(ObservationStatus), nullable=False
    )
    raw_observation_id: Mapped[str | None] = mapped_column(
        ForeignKey("raw_observations.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "item_id",
            "reference_date",
            "geography_id",
            name="uq_norm_price_item_date_geo",
        ),
    )


class NormalizedIncome(Base):
    __tablename__ = "normalized_incomes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    income_basis: Mapped[str] = mapped_column(
        String, nullable=False
    )  # 'minimum_wage', 'average'
    reference_date: Mapped[date] = mapped_column(Date, nullable=False)
    geography_id: Mapped[str] = mapped_column(ForeignKey("geography.id"))
    income_brl: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    status: Mapped[ObservationStatus] = mapped_column(
        Enum(ObservationStatus), nullable=False
    )
    raw_observation_id: Mapped[str | None] = mapped_column(
        ForeignKey("raw_observations.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "income_basis",
            "reference_date",
            "geography_id",
            name="uq_norm_income_basis_date_geo",
        ),
    )


class Basket(Base):
    __tablename__ = "baskets"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g. 'protein_v1'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class BasketItem(Base):
    __tablename__ = "basket_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    basket_id: Mapped[str] = mapped_column(ForeignKey("baskets.id"))
    item_id: Mapped[str] = mapped_column(String, nullable=False)  # 'beef'
    quantity: Mapped[float] = mapped_column(Numeric, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)  # 'kg'

    __table_args__ = (UniqueConstraint("basket_id", "item_id", name="uq_basket_item"),)
