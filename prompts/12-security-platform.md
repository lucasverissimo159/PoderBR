# Prompt 12 — Security, Supply Chain, CI/CD and Operations

Act as Security/Platform Agent.

Read architecture, current deployment files and platform context.

## Research

Consult current official guidance for selected frameworks, Docker, GitHub Actions and relevant security standards. Investigate dependency scanning, lockfiles/pinning, secret handling, HTTP headers, CORS, rate limiting, logging/PII, health/readiness, backup/restore and CI supply-chain controls.

## Implement where justified

- `.env.example`;
- secure defaults;
- Docker hardening;
- CI security checks;
- dependency audit;
- structured logging;
- health/readiness;
- bounded rate limiting/cache policy;
- deployment/runbook documentation.

No secrets in repo. Jules itself warns against committing API keys or credentials because its execution environment can access repository code and has network access.

Basic anonymous usage should work without authentication unless product research justifies accounts.

Document protection boundaries and explicit out-of-scope controls.
