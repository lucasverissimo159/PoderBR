# User Journeys & States

## 1. Primary User Flow: The Explorer
1. **Landing:** User arrives at the homepage. The main view displays the national average affordability of the protein basket for the current month, compared to a baseline (e.g., Jan 2010 = 100).
2. **Contextualization:** User selects their income basis (e.g., "Minimum Wage") and their location (e.g., "São Paulo").
3. **Analysis:** The dashboard updates:
   - A headline metric shows the current *Income Burden* (e.g., "This basket consumes 15% of the minimum wage in SP").
   - A time-series chart shows the historical trend (Progressive Disclosure: default view is a simple line; hover shows exact values and dates).
4. **Drill-down:** User clicks "View Basket Details" to see the nominal prices of beef, pork, chicken, and eggs that make up the total cost.
5. **Methodology:** User clicks an info icon next to the data to see the exact IBGE/Ipeadata source URL, retrieval date, and formula.

## 2. Edge Cases & States

### Empty / Missing Data States
- **Scenario:** The official source has not published data for a specific State (UF) in a specific month.
- **UX Response:** The chart shows a visible gap. A clear, non-alarming message appears: "Data for [State] in [Month] is not available from [Source]." We do *not* interpolate or guess the value.

### Partial Coverage
- **Scenario:** We have chicken and egg prices, but beef prices are delayed for the current month.
- **UX Response:** The total basket cost cannot be calculated. The UI must state: "Incomplete basket data for this period" and disable the aggregate affordability metric for that specific month, while allowing the user to view the individual available commodities.

### Error States
- **Scenario:** Backend API fails to load data from the database.
- **UX Response:** Display a polite error message indicating a temporary system issue, with a "Retry" button. Never expose raw SQL or stack traces.

### Progressive Disclosure Strategy
- **Layer 1 (The Shape):** The headline metric and a clean trend line. Focus on the *story* (e.g., "Affordability is decreasing").
- **Layer 2 (The Details):** Tooltips on hover showing exact dates, nominal prices, and basket components.
- **Layer 3 (The Provenance):** A dedicated "Methodology & Sources" panel or modal detailing the exact API endpoints, extraction dates, and mathematical formulas used.
