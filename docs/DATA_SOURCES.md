# Candidate Data Sources

## 1. National Minimum Wage (Salário Mínimo)
- **Provider:** Ipeadata / Ministério da Economia
- **Dataset ID:** `MTE12_SALMIN12` (OData API)
- **Stable URL:** `http://www.ipeadata.gov.br/api/odata4/Metadados('MTE12_SALMIN12')`
- **Geography:** National (Brazil)
- **Frequency:** Monthly
- **Historical Coverage:** Since July 1940
- **Unit:** R$ (Nominal value)
- **Type:** Price level (Income base)
- **Revision Behavior:** Stable historical series. Revisions only occur if legislation retroactively changes, which is rare.
- **Access Constraints:** Public OData API, no rate limit specified but requires polite usage.
- **License/Attribution:** Public domain (Open Data), attribute to Ipeadata / Min. Economia.
- **Reproducibility:** Very high.
- **Suitability Score:** 10/10. Perfect for baseline income calculations.

## 2. Average Income (Rendimento Médio Nominal)
- **Provider:** IBGE / PNAD Contínua
- **Dataset ID:** `10280` (SIDRA API) - "Valor do rendimento nominal mensal médio..."
- **Stable URL:** `https://servicodados.ibge.gov.br/api/v3/agregados/10280`
- **Geography:** National, Regions, States (UFs)
- **Frequency:** Quarterly
- **Historical Coverage:** Since 2012
- **Unit:** R$ (Nominal value)
- **Type:** Price level (Income base)
- **Revision Behavior:** Occasional revisions due to demographic weighting updates (last major revision in 2021).
- **Access Constraints:** Public REST API, max 50000 records per request.
- **License/Attribution:** Open Data, attribute to IBGE PNADC.
- **Reproducibility:** High, but requires tracking exact methodology vintage.
- **Suitability Score:** 8/10. Crucial for geographic comparison, but quarterly frequency introduces temporal gaps compared to monthly prices.

## 3. Inflation / Deflators (IPCA)
- **Provider:** IBGE / SNIPC (Sistema Nacional de Índices de Preços ao Consumidor)
- **Dataset ID:** `1737` (Historical index) and `7060` (Detailed groups since 2020)
- **Stable URL:** `https://servicodados.ibge.gov.br/api/v3/agregados/1737`
- **Geography:** National, Regions, Metropolitan Areas, and specific capitals (e.g., Aracaju, Belém). *Not all states have coverage.*
- **Frequency:** Monthly
- **Historical Coverage:** Since Dec 1979
- **Unit:** Number-index or % variation
- **Type:** Index
- **Revision Behavior:** Generally not revised once published, making it a highly stable deflator.
- **Suitability Score:** 10/10 for deflating historical nominal values.

## 4. Nominal Protein Prices (The Basket)
- **Provider:** CEPEA / ESALQ (Centro de Estudos Avançados em Economia Aplicada)
- **Dataset IDs:**
  - Indicador do Boi Gordo CEPEA/B3
  - Indicador do Frango Congelado/Resfriado CEPEA
  - Indicador do Suíno CEPEA
- **Stable URL:** `https://www.cepea.esalq.usp.br/br/consultas-ao-banco-de-dados-do-site.aspx`
- **Geography:** Focused heavily on São Paulo (state average) and major producing regions (e.g., Paraná, Santa Catarina). Does *not* cover all Brazilian states.
- **Frequency:** Daily/Monthly averages
- **Historical Coverage:** Extensive (varies by protein, generally 1990s onward)
- **Unit:** R$/kg or R$/arroba
- **Type:** Price level
- **Revision Behavior:** Finalized monthly, rarely revised.
- **Access Constraints:** CEPEA does not have a modern JSON REST API. Data is distributed via downloadable CSVs or HTML scraping.
- **Suitability Score:** 7/10. It is the gold standard for nominal agricultural prices in Brazil, but the lack of a modern API means ingestion requires web scraping/CSV parsing, and geographical coverage is limited mostly to SP or the South.
