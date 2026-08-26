# ADR 0002: Data Source Strategy

## Context
PoderBR needs reliable, public, primary data sources to calculate the cost of a protein basket and compare it against income. We need to decide which APIs to target for macroeconomic data (inflation, income) and specific agricultural/price data.

## Decision

We have evaluated the primary Brazilian public data APIs:

1.  **IBGE SIDRA API (Sistema IBGE de Recuperação Automática):**
    *   *Role:* Primary source for demographic, income (PNAD Continua), and inflation (IPCA) data.
    *   *Why:* IBGE is the official statistical institute of Brazil. SIDRA provides a robust REST API (`https://servicodados.ibge.gov.br/api/v3/agregados`) that allows querying specific tables, variables, and territorial levels. It is the absolute source of truth for the IPCA (inflation index) and official employment/income statistics.
2.  **Ipeadata API:**
    *   *Role:* Secondary source for historical macroeconomic series and consolidated financial data not easily queryable via SIDRA.
    *   *Why:* Ipeadata aggregates many sources (including IBGE, Central Bank) and provides an OData API (`http://www.ipeadata.gov.br/api/odata4/`). It's useful for long-term historical series, but we must strictly adhere to the principle of "Source != indicator" and trace back to the primary provider documented in Ipeadata's metadata.

**Data Handling Principles:**
- All adapters must fetch data via these APIs and cache/store raw responses before normalization.
- We will not use secondary wrapper libraries if they obscure the original API request; we will write direct HTTP clients (e.g., using `httpx` in Python) to ensure we control the exact query parameters and headers.
- If a data point is missing in the API for a specific geography/time, it remains `missing` in our system. No silent imputation.

## Consequences
- Data ingestion agents must implement rate limiting and respect API usage guidelines.
- Each dataset pulled must include metadata (retrieval time, source URL, exact query parameters) to satisfy the reproducibility and data provenance requirements.
