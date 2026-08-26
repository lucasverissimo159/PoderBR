# Methodology - PoderBR

This document outlines the core methodologies for calculating the purchasing power index and related metrics.

## 1. The Core Metrics

*   `basket_cost`: The total cost of the configured basket for a specific geography and time period.
*   `income_burden`: The percentage of income consumed by the basket cost (`basket_cost / income`).
*   `affordability_ratio`: How many times the income can buy the basket (`income / basket_cost`).
*   `purchasing_power_index`: The affordability normalized against a specific base period (e.g., Index = 100 for January 2010).

## 2. Basket Definition (UNVERIFIED)

*   **Status**: Initial hypothesis, pending domain expert review.
*   **Composition (Proteins)**:
    *   Beef: X kg
    *   Pork: Y kg
    *   Chicken: Z kg
    *   Eggs: W dozen
*   **Rationale**: To be determined. We need to find official sources (like POF - Pesquisa de Orçamentos Familiares from IBGE) to define a representative basket.

## 3. Data Sources and Handling (UNVERIFIED)

*   **Prices**: Sourced from [Source Name, e.g., IPCA/SNIPC/CEPEA]. Must use actual nominal prices, not index variations, to calculate basket cost.
*   **Income**: Sourced from [Source Name, e.g., PNAD Continua].
*   **Missing Data**: Missing data points will not be imputed in the raw data layer. Imputation strategies (if any) must be explicitly defined and versioned here.

## 4. Geography Handling

Data is only presented at the geographic level it was collected. If a source only provides state-level data, we do not infer city-level data.
