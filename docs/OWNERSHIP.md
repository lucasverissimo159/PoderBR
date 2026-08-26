# Agent Ownership

| Surface | Primary owner | Shared? | Notes |
|---|---|---:|---|
| Product specs | Product | No | Changes require product review |
| ADRs | Architecture | Yes | Any agent may propose; Architecture integrates |
| Data contracts | Data Engineering | Yes | Consumers must be checked |
| Analytics contract | Analytics | Yes | Formula changes require QA |
| API contract | API/Backend | Yes | Frontend consumer must be checked |
| Frontend | Frontend | No | Shared design primitives require review |
| Data quality | Data Quality | No | May request ingestion fixes |
| Security/CI | Platform | No | Shared CI changes require integration |
| Release readiness | Integration/Release | Yes | Final authority after audit |

When ownership changes, update this file in the same change as the related ADR or contract.
