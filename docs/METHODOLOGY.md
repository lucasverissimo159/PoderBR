# Methodology - PoderBR

This document outlines the core economic and statistical methodologies for calculating the Purchasing Power Index and related metrics within PoderBR.

## 1. Caveat: Product Scenario vs. Universal Truth

**The baskets defined in this platform represent specific *product scenarios*, not universal truths about Brazilian consumption.**

When we define a "Protein Basket," we are fixing a static set of goods (e.g., 5kg of Beef, 3kg of Chicken) to measure how the affordability of *that specific scenario* changes over time. Real-world consumers substitute goods when prices change (e.g., buying less beef and more chicken). Our fixed-basket approach intentionally ignores substitution effects to isolate the loss or gain of purchasing power relative to a baseline standard of living.

## 2. Core Metrics and Formulas

### 2.1 Basket Cost ($C_t$)
The total nominal cost of the configured basket for a specific geography and time period $t$.
- **Formula:** $C_t = \sum (Q_i \times P_{i,t})$
  - $Q_i$: Quantity of item $i$ in the basket (e.g., kg or dozen).
  - $P_{i,t}$: Normalized nominal price of item $i$ at time $t$ in BRL.
- **Unit:** BRL (R$)
- **Interpretation:** The absolute monetary amount required to buy the basket.

### 2.2 Income Burden ($B_t$)
The percentage of the specified income consumed by the basket cost.
- **Formula:** $B_t = (C_t / I_t) \times 100$
  - $I_t$: Nominal income at time $t$ in BRL.
- **Unit:** Percentage (%)
- **Interpretation:** "This basket consumes X% of a minimum wage worker's income."

### 2.3 Affordability Ratio ($A_t$)
How many times the income can buy the basket. This is the inverse of the income burden and serves as the raw measure of purchasing power.
- **Formula:** $A_t = I_t / C_t$
- **Unit:** Decimal (Count)
- **Interpretation:** "The income buys X baskets."

### 2.4 Purchasing Power Index ($PPI_t$)
The affordability normalized against a declared base period ($t_0$), making it easy to see relative changes over time.
- **Formula:** $PPI_t = (A_t / A_{t_0}) \times 100$
- **Unit:** Index (Base 100)
- **Interpretation:** If the index is 90, purchasing power for this specific basket has fallen by 10% compared to the base period.

## 3. Data Handling and Invalid Cases

- **Nominal vs Real:** All calculations use **nominal** prices and **nominal** income from the exact same period $t$. We do *not* deflate or inflate historical prices using the IPCA, ensuring we measure actual affordability at the time the transaction occurred.
- **Missing Data:** If the price for *any single item* in the basket is missing for period $t$, the total basket cost cannot be calculated. The entire period $t$ is marked as `partial` and returns `null` for aggregate metrics. We do not substitute with zero or interpolate missing months.
- **Zero Income:** If income is zero or missing, $B_t$, $A_t$, and $PPI_t$ are mathematically undefined and will return `null`.
