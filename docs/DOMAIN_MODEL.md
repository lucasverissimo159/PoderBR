# Domain Model

This document outlines the core domain concepts in PoderBR.

## 1. Geography (`app/domain/geography`)
Handles canonical representations of Brazilian territories.
- **Concepts:** `Country`, `State (UF)`, `MetropolitanArea`.
- **Rules:** The system uses IBGE's canonical state codes (e.g., '35' for São Paulo) and UF acronyms ('SP').

## 2. Baskets (`app/domain/baskets`)
Defines the versioned methodology of what constitutes the "Cost of Living" for a specific sector.
- **Concepts:** `BasketDefinition`, `BasketItem`.
- **Rules:** A basket has a `version_id`. The MVP basket (e.g., 'protein_v1') is immutable. To change the composition, a new version (e.g., 'protein_v2') must be created.

## 3. Observations (`app/domain/observations`)
The raw, untrusted data layer.
- **Concepts:** `RawObservation`.
- **Rules:** Every observation must link to a `source_url`, `provider`, and `retrieval_timestamp`.

## 4. Normalization (`app/domain/normalization`)
- **Concepts:** `NormalizedIncome`, `NormalizedPrice`.
- **Rules:** Handles the conversion of raw observations into a standardized format. E.g., if CEPEA provides beef prices in R$/arroba (15kg), this domain converts it to R$/kg before passing it to Analytics.

## 5. Analytics (`app/domain/analytics`)
The core business logic.
- **Concepts:** `BasketCost`, `IncomeBurden`, `PurchasingPowerIndex`.
- **Rules:**
  - `basket_cost = SUM(item_price * item_quantity)`
  - `income_burden = (basket_cost / income) * 100`
  - Calculates the final output exposed to the API. Requires explicitly defined methodologies to handle temporal mismatches (e.g., applying monthly prices against quarterly income).
