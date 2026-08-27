from collections.abc import Generator
from datetime import datetime
from typing import Any

import httpx

from app.ingestion.base import BaseAdapter
from app.models.core import DataSource


class IpeadataAdapter(BaseAdapter):
    """Adapter for Ipeadata Minimum Wage (MTE12_SALMIN12)."""

    BASE_URL = "http://www.ipeadata.gov.br/api/odata4"
    DATASET_ID = "MTE12_SALMIN12"

    def get_source_metadata(self) -> DataSource:
        return DataSource(
            id=f"ipeadata_{self.DATASET_ID}",
            provider="Ipeadata / Ministério da Economia",
            dataset_name="Salário mínimo vigente",
            url=f"{self.BASE_URL}/Metadados('{self.DATASET_ID}')",
        )

    def fetch_data(self) -> Generator[dict[str, Any], None, None]:
        # Using synchronous httpx for simplicity in scheduled jobs
        with httpx.Client(timeout=30.0) as client:
            # Ipeadata OData returns a 'value' array
            # VALDATA is ISO date with time, VALVALOR is the numeric value
            response = client.get(
                f"{self.BASE_URL}/ValoresSerie(SERCODIGO='{self.DATASET_ID}')"
            )
            response.raise_for_status()
            data = response.json()

            if "value" not in data:
                raise ValueError(
                    "Schema drift: Ipeadata response missing 'value' array"
                )

            for record in data["value"]:
                # Expected format: "2024-01-01T00:00:00-03:00"
                date_str = record.get("VALDATA", "")
                if not date_str:
                    continue

                ref_date = datetime.fromisoformat(date_str).date()

                # Minimum wage is national, so geography_id is canonical 'BR'
                yield {
                    "geography_id": "BR",
                    "reference_date": ref_date,
                    "value": float(record.get("VALVALOR", 0.0)),
                    "unit": "BRL",
                }
