import logging
from collections.abc import Generator
from datetime import datetime
from typing import Any

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from app.models.core import DataSource, IngestionRun, RawObservation

logger = logging.getLogger(__name__)


class BaseAdapter:
    def __init__(self, db: Session):
        self.db = db

    def get_source_metadata(self) -> DataSource:
        """Must return a DataSource instance representing this adapter's target."""
        raise NotImplementedError

    def fetch_data(self) -> Generator[dict[str, Any], None, None]:
        """Must yield dictionaries mapping to RawObservation fields."""
        raise NotImplementedError

    def run(self, dry_run: bool = False) -> IngestionRun:
        """Executes the ingestion lifecycle, ensuring tracking and idempotency."""
        source = self.get_source_metadata()

        # Upsert DataSource to ensure it exists
        existing_source = self.db.get(DataSource, source.id)
        if not existing_source:
            if not dry_run:
                self.db.add(source)
                self.db.commit()
                self.db.refresh(source)

        run = IngestionRun(source_id=source.id, status="running")
        if not dry_run:
            self.db.add(run)
            self.db.commit()

        records_processed = 0
        try:
            for raw_data in self.fetch_data():
                if dry_run:
                    logger.info(f"[DRY RUN] Would insert: {raw_data}")
                    records_processed += 1
                    continue

                # We use SQLite's specific ON CONFLICT DO UPDATE (or IGNORE) for idempotency.
                # In Postgres, this would use sqlalchemy.dialects.postgresql.insert
                stmt = (
                    insert(RawObservation)
                    .values(
                        source_id=source.id,
                        geography_id=raw_data["geography_id"],
                        reference_date=raw_data["reference_date"],
                        value=raw_data.get("value"),
                        unit=raw_data["unit"],
                        run_id=run.id,
                        retrieved_at=datetime.now(),
                    )
                    .on_conflict_do_update(
                        index_elements=["source_id", "reference_date", "geography_id"],
                        set_={
                            "value": raw_data.get("value"),
                            "run_id": run.id,
                            "retrieved_at": datetime.now(),
                        },
                    )
                )
                self.db.execute(stmt)
                records_processed += 1

            run.status = "success"
        except Exception as e:
            run.status = "failed"
            logger.error(f"Ingestion failed: {e}")
            if not dry_run:
                self.db.commit()  # Save the failed state
            raise
        finally:
            run.completed_at = datetime.now()
            run.records_processed = records_processed
            if not dry_run:
                self.db.commit()

        return run
