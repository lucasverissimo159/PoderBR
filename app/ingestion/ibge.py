import re
from collections.abc import Generator
from datetime import date
from typing import Any

import httpx

from app.ingestion.base import BaseAdapter
from app.models.core import DataSource


class IbgeSidraAdapter(BaseAdapter):
    """Adapter for IBGE SIDRA Average Income (Table 10280)."""

    BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"
    DATASET_ID = "10280"

    def get_source_metadata(self) -> DataSource:
        return DataSource(
            id=f"ibge_sidra_{self.DATASET_ID}",
            provider="IBGE PNAD Contínua",
            dataset_name="Valor do rendimento nominal mensal médio",
            url=f"{self.BASE_URL}/{self.DATASET_ID}",
        )

    def _parse_quarter(self, quarter_str: str) -> date:
        """
        Parses 'YYYY0Q' (e.g., '202401' for Q1 2024) to a start date
        (e.g., 2024-01-01).
        """
        match = re.match(r"(\d{4})0(\d)", quarter_str)
        if not match:
            raise ValueError(f"Invalid quarter format: {quarter_str}")
        year = int(match.group(1))
        quarter = int(match.group(2))
        month = (quarter - 1) * 3 + 1
        return date(year, month, 1)

    def fetch_data(self) -> Generator[dict[str, Any], None, None]:
        with httpx.Client(timeout=30.0) as client:
            # We query national (1) and state (3) levels.
            # Variable 12384 is the specific average income variable within table 10280
            # (needs verification against actual SIDRA, assuming standard shape for now)
            # URL format:
            # /api/v3/agregados/table/periodos/all/variaveis?localidades=N1[all]|N3[all]
            locs = "N1[all]|N3[all]"
            path = f"{self.DATASET_ID}/periodos/all/variaveis?localidades={locs}"
            url = f"{self.BASE_URL}/{path}"
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, list) or len(data) == 0:
                raise ValueError(
                    "Schema drift: IBGE SIDRA returned empty or non-list data"
                )

            for variable_group in data:
                # Iterate through results per geography
                for result in variable_group.get("resultados", []):
                    geo_id = result.get("localidade", {}).get("id")
                    if not geo_id:
                        continue

                    for series in result.get("series", []):
                        for period, value_str in series.items():
                            if (
                                value_str == "-"
                                or value_str == "..."
                                or value_str == "X"
                            ):
                                value = None
                            else:
                                try:
                                    value = float(value_str)
                                except ValueError:
                                    value = None

                            try:
                                ref_date = self._parse_quarter(period)
                            except ValueError:
                                continue  # Skip invalid dates safely

                            yield {
                                "geography_id": geo_id,
                                "reference_date": ref_date,
                                "value": value,
                                "unit": "BRL",
                            }
