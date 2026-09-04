from collections.abc import Generator
from datetime import date
from typing import Any

from app.ingestion.base import BaseAdapter
from app.models.core import DataSource


class CepeaMockAdapter(BaseAdapter):
    """
    CEPEA does not have a stable JSON API; data is distributed via HTML scraping
    or Excel. For this MVP, this adapter serves as a mock implementing the
    exact interface to prove out the ingestion pipeline without writing a brittle
    HTML scraper.
    """

    def get_source_metadata(self) -> DataSource:
        return DataSource(
            id="cepea_meat_prices",
            provider="CEPEA/ESALQ",
            dataset_name="Indicadores CEPEA (Boi, Frango, Suíno)",
            url="https://www.cepea.esalq.usp.br/br/consultas-ao-banco-de-dados-do-site.aspx",
        )

    def fetch_data(self) -> Generator[dict[str, Any], None, None]:
        # Yield mock historical data for SP (São Paulo)
        # In a real scenario, this would use pandas.read_excel or beautifulsoup4

        mock_data = [
            {"date": date(2024, 1, 1), "beef": 250.0, "chicken": 7.50, "pork": 120.0},
            {"date": date(2024, 2, 1), "beef": 240.0, "chicken": 7.40, "pork": 115.0},
        ]

        for record in mock_data:
            yield {
                "geography_id": "SP",  # CEPEA often defaults to SP
                "reference_date": record["date"],
                "value": record["beef"],
                "unit": "BRL/arroba",  # Raw unit, normalization layer converts to kg
            }
