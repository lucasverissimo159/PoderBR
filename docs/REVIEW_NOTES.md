# Revision Notes — Jules Prompt Pack

This revision was made after reviewing the previous prompt pack for gaps that could cause context drift or unreliable implementation.

## Main improvements

1. Expanded from 17 to 20 executable prompts.
2. Added persistent project state (`docs/AGENT_STATE.md`).
3. Added explicit domain/file ownership (`docs/OWNERSHIP.md`).
4. Added canonical cross-layer contracts under `docs/contracts/`.
5. Added data-quality/freshness/anomaly monitoring task.
6. Added performance/reliability baseline and resilience task.
7. Added task-router agent for future Jules requests.
8. Strengthened licensing/access constraints in source research.
9. Strengthened migration, idempotency, revision/vintage and rollback concerns.
10. Added formal accessibility considerations.
11. Added security/supply-chain controls and external-provider failure behavior.
12. Added explicit Jules setup/snapshot and plan-approval guidance.
13. Renamed product context to **PoderBR** while keeping proteins as the first domain.

## Deliberately not included

- Authentication as an MVP requirement.
- Microservices by default.
- Live external API dependencies inside CI tests.
- Synthetic real-world numbers presented as production data.
- Automatic deletion of anomalous observations.
