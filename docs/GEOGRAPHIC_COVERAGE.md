# Geographic Coverage Strategy

## 1. The Reality of Brazilian Data
There is a fundamental mismatch in the geographic coverage of our primary data sources:
- **Minimum Wage:** National.
- **Average Income (PNADC):** National, Regional, State (27 UFs).
- **Inflation (IPCA):** National, and 16 Metropolitan Areas / Capitals (e.g., Belém, Fortaleza, Recife, Salvador, Belo Horizonte, Vitória, Rio de Janeiro, São Paulo, Curitiba, Porto Alegre, Brasília, Goiânia, Campo Grande, Rio Branco, São Luís, Aracaju). **It does not cover all 27 states.**
- **Nominal Meat Prices (CEPEA):** Highly fragmented. Beef is usually calculated as State of São Paulo (SP). Chicken and Pork are tracked in major producing states (SP, PR, SC, RS, MG).

## 2. MVP Coverage Decision
Based on the `AGENTS.md` rule "The product can only declare coverage supported by real observations. Do not fill missing UFs by assumption."

**The MVP will only support National and State of São Paulo (SP).**

*Why?*
- We have solid, consistent nominal price data from CEPEA for São Paulo.
- We have PNADC income data for São Paulo.
- We have the National Minimum Wage.
- If we try to expand to all 27 UFs immediately, we will have missing nominal price data for over 20 states, forcing us to either use a single national price (which defeats the purpose of geographic comparison) or interpolate prices, violating our core methodology.

## 3. Future Expansion
To expand to other states, we need to locate a reliable, machine-readable source of nominal retail prices at the state level (like Procon surveys or regional CEASAs), which currently lack the standardization of CEPEA/IBGE.
