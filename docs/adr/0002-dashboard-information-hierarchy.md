# ADR 0002: Dashboard Information Hierarchy

## Status
Accepted

## Context
PoderBR is an analytical platform designed to communicate purchasing power metrics securely and honestly. Prompt 10 requires defining a core hierarchy for the "Analytical Story" on the dashboard that is understandable within seconds while preserving statistical honesty.

We reviewed the candidate hierarchy proposed:
1. location + income
2. basket cost
3. income burden
4. affordability/quantity
5. historical trend
6. protein contribution
7. comparison
8. methodology/data coverage

### Pattern Comparison
**Pattern A: "Executive Summary First"**
- Top bar: Global filters (Location, Date, Income)
- Hero section: High-level KPIs (Cost, Burden, Purchasing Power Index).
- Body section: Detail charts (Historical Trend over time, Composition).
- Footer: Methodology and disclosure.
- *Pros*: Aligns with standard BI tools (Tableau, PowerBI). Users instantly get the "current state" before diving into historical complexities.

**Pattern B: "Narrative Scroll / Scrollytelling"**
- Top to bottom flow revealing insights sequentially.
- *Pros*: Excellent for guiding inexperienced users through complex economic concepts.
- *Cons*: Restrictive for recurring users (journalists/researchers) who want to quickly look up a specific state's index without scrolling through a story.

## Decision
We will adopt **Pattern A (Executive Summary First)** to support the primary personas (citizens, data journalists, policy analysts). We refine the proposed hierarchy into the following layout:

1. **Global Controls Boundary**: Location, Income Basis, and Date selectors pinned at the top.
2. **Current State (KPI Cards)**: The most recent data point displayed as large numbers (Basket Cost, Income Burden, Affordability Ratio). This answers "What is happening now?". Must explicitly show units and baseline.
3. **The 'Why' (Historical Trend)**: A line chart displaying the Purchasing Power Index over time to answer "Is it getting better or worse?".
4. **The 'What' (Protein Contribution)**: A stacked chart decomposing the nominal cost into Beef, Pork, Chicken, and Eggs to answer "What is driving the change?".
5. **Transparency (Methodology)**: The disclosure component at the bottom, explaining the basket weights, sources, and emphasizing that missing data is not interpolated.

For the comparison requirement (point 7), we will introduce a separate **Comparison View** page routed via the App Shell. Comparing two regions side-by-side on the main dashboard can clutter the layout, especially on mobile, violating our readability priority.

## Consequences
- The strict hierarchy forces us to handle missing data gracefully in the KPI section (e.g., if the latest month has no income data, the KPI must clearly state "Missing" rather than silently dropping down to the previous month, as per backend API rules).
- Separating the Comparison view requires robust state management in the URL or router to allow users to share specific comparison states.
