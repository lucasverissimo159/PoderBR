# Product Specification — PoderBR

## 1. Target Personas
- **The Everyday Citizen:** Wants a relatable measure of inflation ("Is my money buying less meat than last year?"). Needs simple, visual, and relatable data without complex economic jargon.
- **The Data Journalist / Researcher:** Needs source transparency, precise methodology, data provenance, and the ability to cite or reproduce the findings. Cares about the specific composition of the basket and the exact formulas used.
- **The Policy Analyst / Student:** Looks for trends across regions and income levels to understand local economic impact.

## 2. Jobs-to-be-Done (JTBD)
- **When** I look at my grocery bill, **I want to** understand if the cost of basic proteins is taking up more of my income than before, **so I can** validate my feeling of lost purchasing power.
- **When** I write an article about regional inequality, **I want to** compare the affordability of a standard basket across different Brazilian states, **so I can** provide a data-backed narrative.
- **When** I see a headline about inflation, **I want to** drill down into the specific prices of beef, chicken, pork, and eggs over the last decade, **so I can** understand the components driving the index.

## 3. Primary User Questions
- "How much does a basic basket of proteins cost right now in my state?"
- "What percentage of the minimum wage (or average regional income) does this basket consume?"
- "Is the situation getting better or worse compared to 1, 5, or 10 years ago?"
- "How does my state compare to the national average or other states?"
- "How much beef could my income buy in 2010 vs. today?"

## 4. MVP Scope and Explicit Non-Goals
**MVP Scope:**
- Domain: Proteins (beef, pork, chicken, eggs).
- Geography: Brazil (National) and State-level (UFs), limited strictly by data availability.
- Income bases: National minimum wage, and regional average income (if reliably available via IBGE).
- Views: Current affordability, historical trend (purchasing power index), and geographical comparison.

**Explicit Non-Goals (Out of Scope):**
- Real-time/crowdsourced price scraping (we use official historical APIs).
- Personal budget tracking or financial advice.
- Extrapolating protein affordability into a general "Cost of Living" or "Welfare" index.
- Estimating data for regions where official sources have gaps.
- User authentication or saving user profiles.

## 5. Challenging the Premise (Honest UX & Avoiding Welfare Claims)
**The Risk:** If the UI says "Purchasing Power dropped 10%", users might interpret this as "Everyone is 10% poorer overall."
**The Mitigation:**
- **Decomposed Metrics:** We must explicitly state: "The purchasing power *for this specific protein basket*."
- **Wording:** Avoid generic terms like "Cost of Living" or "Welfare." Use precise terms like "Protein Basket Affordability" or "Income Burden of Proteins."
- **Transparency:** The basket composition must be immediately accessible. If we assume 5kg of beef, the user must see that, as it heavily skews the result.
- **Uncertainty:** Any delay in official reporting, or changes in IBGE/CEPEA methodology over time, must be visually flagged (e.g., using dashed lines on charts for preliminary data or annotations for methodology breaks).
