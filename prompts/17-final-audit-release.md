# Prompt 17 — Principal Audit, Release Candidate and Demo Readiness

Act as a skeptical principal engineer/reviewer.

Read the complete repository context, ADRs, contracts, methodology and release readiness.

## Audit

### Product
- clear problem;
- understandable core metric;
- explicit MVP boundaries.

### Data
- traceable observations;
- comparable geography/unit/frequency;
- missing/estimated values disclosed;
- licensing/attribution respected.

### Analytics
- formulas correct;
- units correct;
- nominal vs real separated;
- basket/version declared;
- no overclaiming.

### Engineering
- modular boundaries;
- stable contracts;
- migrations;
- fresh setup works;
- tests adequate.

### Security/operations
- no secrets;
- dependencies controlled;
- logs do not leak unnecessary PII;
- health/readiness;
- failure behavior understood.

### UX/accessibility
- keyboard/accessibility basics;
- chart alternatives;
- loading/error/partial states;
- precision appropriate.

## Deliverables

Update:
- `docs/RELEASE_READINESS.md`
- `docs/DEMO_SCRIPT.md`
- `CHANGELOG.md`
- `docs/handoffs/FINAL-AUDIT.md`

Create a prioritized release-blocker list. Fix blockers only when clearly in scope. State exactly what is production-ready, demo-ready only, or unverified due to unavailable infrastructure/external data.
