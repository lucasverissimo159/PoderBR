# Prompt 03 — Architecture, Domain Boundaries and Contracts

Act as the Architecture Agent.

Read product/data outputs, all ADRs, `AGENTS.md`, `docs/ORCHESTRATION.md`.

## Mission

Design an architecture future agents can implement without guessing where responsibilities belong.

## Research

Use official documentation for the chosen stack and compare:
- modular monolith vs services;
- synchronous API vs async/scheduled jobs;
- repository/service/domain patterns;
- relational schema strategy;
- API versioning;
- frontend query/state approach;
- caching;
- observability.

## Produce

- `docs/ARCHITECTURE.md`
- `docs/DOMAIN_MODEL.md`
- `docs/API_CONTRACTS.md`
- `docs/contracts/API_CONTRACT.md`
- `docs/contracts/DATA_CONTRACT.md`
- `docs/contracts/ANALYTICS_CONTRACT.md`
- `docs/contracts/FRONTEND_BACKEND_CONTRACT.md`
- `docs/adr/0004-domain-boundaries.md`
- `docs/adr/0005-api-strategy.md`
- `docs/handoffs/ARCHITECTURE.md`

Explicit modules should include, as justified: geography, source/provenance, observations, income, protein prices, baskets, analytics, API and presentation.

Prefer a modular monolith unless evidence proves otherwise. Do not implement full features here.
