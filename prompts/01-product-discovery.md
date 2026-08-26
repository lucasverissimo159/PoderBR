# Prompt 01 — Product Discovery, Scope and Acceptance Model

Act as the Product Research Agent. Research first; do not implement a large UI.

Read `AGENTS.md`, `docs/PROJECT_CONTEXT.md`, `docs/ORCHESTRATION.md`, `agent-context/product.md`.

## Mission

Transform the initial idea into a testable product model for **PoderBR**, whose first domain is protein purchasing power.

## Explore

Research credible consumer-economic dashboards and data-journalism products. Investigate:
- useful comparison patterns;
- progressive disclosure;
- uncertainty/coverage communication;
- accessible narrative around economic metrics;
- common UX mistakes that turn an index into an overstated welfare claim.

## Produce

Create/update:
- `docs/PRODUCT_SPEC.md`
- `docs/USER_JOURNEYS.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/FEATURE_MATRIX.md`
- `docs/handoffs/PRODUCT-DISCOVERY.md`

Define:
- target personas;
- jobs-to-be-done;
- primary user questions;
- MVP and explicit non-goals;
- user flows;
- empty/partial/error states;
- accessibility requirements;
- methodology disclosures;
- measurable acceptance criteria.

## Challenge the premise

Identify where the original concept could mislead users. Propose better wording and decomposed metrics. Explicitly distinguish “purchasing power relative to this basket” from general cost of living/welfare.

Do not lock technical choices unless an ADR is warranted.

Finish with a dependency-aware backlog that another agent can implement without rediscovering requirements.
