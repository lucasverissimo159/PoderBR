# Acceptance Criteria & Accessibility

## 1. Measurable Acceptance Criteria (MVP)

### Data Accuracy & Provenance
- [ ] AC1: Every data point displayed on the UI must trace back to a specific `source_id`, `provider`, and `retrieval_timestamp` visible in the methodology panel.
- [ ] AC2: The system must successfully calculate the `basket_cost` using only the explicitly defined `basket` items and their respective nominal prices.
- [ ] AC3: If an item in the basket is missing for a given period/location, the aggregate `basket_cost` must explicitly report as `missing` (null), not zero or interpolated.
- [ ] AC4: The `income_burden` must be mathematically verified as `(basket_cost / income) * 100`.

### UI & UX
- [ ] AC5: The dashboard must load the initial national view within 2 seconds.
- [ ] AC6: The user must be able to switch between at least two income bases (e.g., Minimum Wage and a static User Input value) and see the charts update immediately.
- [ ] AC7: The UI must clearly state "Protein Basket Affordability" and avoid terms like "Total Cost of Living."
- [ ] AC8: The exact composition of the basket (weights/quantities) must be visible within one click from the main dashboard.

## 2. Methodology Disclosures
The UI must include a persistent footer or easily accessible "Methodology" section containing:
- The exact definition of the basket (e.g., "Beef: 5kg, Chicken: 3kg...").
- The source of the nominal price data (e.g., "Prices derived from IBGE SNIPC / CEPEA").
- The source of the income data (e.g., "Minimum Wage defined by Federal Decree...").
- A clear disclaimer: *"This index measures the purchasing power specifically for this predefined protein basket and does not represent overall inflation or total cost of living."*

## 3. Accessibility Requirements (a11y)
- **Keyboard Navigation:** All interactive elements (dropdowns, buttons, methodology toggles) must be fully navigable via keyboard (`Tab`, `Enter`, `Space`).
- **Screen Readers:**
  - Charts must have adequate `aria-labels` and `aria-describedby` attributes summarizing the trend (e.g., "Line chart showing protein basket affordability from 2010 to 2024. The trend is generally downward.").
  - An alternative tabular data view must be available for screen reader users to access the raw data points driving the charts.
- **Color Contrast:** All text and chart elements must meet WCAG 2.1 AA contrast ratios (at least 4.5:1 for normal text). Do not rely on color alone to convey information (e.g., use different line styles or markers in addition to color for multiple series).
