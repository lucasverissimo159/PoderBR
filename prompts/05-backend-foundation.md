# Prompt 05 — Backend Domain and Service Layer

Act as the Backend/Domain Agent.

Read `AGENTS.md`, domain model, contracts, architecture, backend and QA contexts.

## Research

For the selected framework, compare practical approaches to validation, dependency injection, repositories, service boundaries, transaction management and error modeling. Prefer the simplest testable design.

## Implement

Create:
- application/domain boundaries;
- typed request/response schemas;
- repositories;
- domain services;
- configuration;
- database session management;
- migrations integration;
- structured errors;
- health/readiness behavior;
- compatibility-aware persistence access.

Business calculations must not live in route handlers.

## Reliability

Define transaction boundaries, idempotency expectations and safe retry semantics for operations that can be retried by an agent or scheduler.

## Tests

Unit tests for services + database integration tests + migration smoke test.

Document design choices and handoff.
