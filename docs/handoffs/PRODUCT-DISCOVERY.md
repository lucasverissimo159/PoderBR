# Handoff: Product Discovery Phase

## Objective
Define the product model, scope, user journeys, and acceptance criteria for the PoderBR MVP (Protein Domain), ensuring honest UX and avoiding overstated welfare claims.

## Decisions Made
- **MVP Scope:** Focused strictly on Protein Basket Affordability.
- **UX Strategy:** Adopted Progressive Disclosure (Shape first, details on demand via tooltips) to keep the dashboard accessible to everyday citizens while providing depth for researchers.
- **Honest UX:** Explicitly rejected terms like "Cost of Living" in favor of "Protein Basket Affordability" to prevent misleading users.
- **Handling Uncertainty:** Missing data will be displayed as explicit gaps; partial data will prevent aggregate calculations rather than relying on silent imputation.

## Evidence/Sources
- Research into data journalism best practices emphasizes progressive disclosure and transparent methodology.
- Accessibility standards (WCAG) require alternative representations of chart data (tabular views) and strict color contrast rules.

## Files Created/Changed
- `docs/PRODUCT_SPEC.md`
- `docs/USER_JOURNEYS.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/FEATURE_MATRIX.md`
- `docs/handoffs/PRODUCT-DISCOVERY.md`

## Interfaces Changed
- N/A (Product definitions only)

## Tests/Checks
- Verified that the defined Acceptence Criteria (AC) map directly to the non-negotiable principles in `AGENTS.md`.

## Limitations
- The exact composition of the protein basket (weights/quantities in kg) is not yet mathematically defined; it requires domain research (Task F1.1).
- The exact API endpoints for nominal prices are pending Data Research (Task F1.3).

## Risks
- Users might still misinterpret the index if they ignore the methodology disclosures. The UI must ensure the title and headline metrics are highly specific.
- Finding reliable, easily queryable APIs for *nominal* protein prices (not just inflation indices) might be challenging.

## Next Tasks
1. `02 Data Research`: Execute F1.1, F1.2, and F1.3 from the Feature Matrix to lock down the data sources and basket composition.
2. `03 Architecture`: Design the database schema based on the findings from Data Research.
