# ADR 0003: Data Source Selection and Historical Strategy

## Context
To calculate the "Protein Basket Affordability" index over time, we need to compare income against the cost of a basket (Beef, Pork, Chicken, Eggs). We need to decide how to handle historical prices and geographic coverage, given the fragmented nature of Brazilian public data.

## Alternative Strategies Evaluated

**Strategy 1: Direct Nominal Price Levels (The Gold Standard)**
- Find nominal R$/kg prices for all proteins, in all states, for all months.
- *Problem:* This data does not exist in a single unified API. CEPEA has SP/South data. IBGE SNIPC has IPCA sub-items, but they only publish the *index variation* via API (Table 7060), not the raw nominal price in R$.

**Strategy 2: Source Price Levels + Explicit Official Inflation Adjustment**
- Take a nominal price today (e.g., from a retail survey or CEPEA) and calculate historical prices by applying the IPCA index backward.
- *Problem:* This violates the core methodological principle "Source != indicator. Never treat a price index as a nominal price." Inflation indexes measure a fixed basket's variation, not the absolute shelf price of a commodity. Deflating a current price backward creates fabricated historical observations.

**Strategy 3: Mixed-Source Strategy with Documented Limitations**
- Use **Ipeadata (MTE12_SALMIN12)** for National Minimum Wage.
- Use **IBGE SIDRA (10280)** for Average Income (National and State).
- Use **CEPEA/ESALQ** for nominal protein prices (R$/kg).
- Restrict geographic scope strictly to areas where CEPEA provides nominal data (Primarily National Average and São Paulo).

## Decision
We select **Strategy 3: Mixed-Source Strategy**.

We refuse to use IPCA backward-extrapolation (Strategy 2) because it creates fake historical prices. If we want to know what a worker paid for beef in 2012, we must find the nominal price recorded in 2012.

Because CEPEA is the only reliable, publicly accessible source of historical nominal agricultural prices, our geographic scope for the MVP is strictly limited to **National** and **São Paulo (SP)**. We will not claim state-level coverage for the other 26 UFs until reliable nominal price data for them is secured.

## Consequences
- The MVP dashboard will default to National and SP views.
- The data ingestion agent must build a specialized adapter to fetch/parse CEPEA data, as they lack a modern REST/OData API like IBGE.
- Income data (IBGE PNADC) is quarterly, while Minimum Wage and CEPEA prices are monthly. The analytics engine must handle this frequency mismatch (e.g., by joining monthly prices to the prevailing quarterly average income).
