#!/usr/bin/env python3
import argparse
import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.ingestion.cepea import CepeaMockAdapter
from app.ingestion.ibge import IbgeSidraAdapter
from app.ingestion.ipea import IpeadataAdapter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ADAPTERS = {
    "ipeadata": IpeadataAdapter,
    "ibge": IbgeSidraAdapter,
    "cepea": CepeaMockAdapter,
}


def main():
    parser = argparse.ArgumentParser(description="PoderBR Data Ingestion Runner")
    parser.add_argument(
        "adapter", choices=list(ADAPTERS.keys()) + ["all"], help="Which adapter to run"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch data but do not write to the database",
    )

    args = parser.parse_args()

    # Initialize DB Session
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    to_run = list(ADAPTERS.keys()) if args.adapter == "all" else [args.adapter]

    for adapter_name in to_run:
        logger.info(f"Starting ingestion for: {adapter_name}")
        with SessionLocal() as db:
            adapter_class = ADAPTERS[adapter_name]
            adapter = adapter_class(db)
            try:
                run_record = adapter.run(dry_run=args.dry_run)
                if args.dry_run:
                    logger.info(
                        f"Dry run completed for {adapter_name}. Would have processed {run_record.records_processed} records."
                    )
                else:
                    logger.info(
                        f"Success for {adapter_name}. Run ID: {run_record.id}. Processed: {run_record.records_processed}"
                    )
            except Exception as e:
                logger.error(f"Failed ingestion for {adapter_name}: {e}")
                sys.exit(1)


if __name__ == "__main__":
    main()
