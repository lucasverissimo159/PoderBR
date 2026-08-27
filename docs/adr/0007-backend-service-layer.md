# ADR 0007: Backend Service and Repository Layer

## Context
As PoderBR scales, we need to ensure that the logic for calculating purchasing power (Analytics) does not leak into the HTTP routing layer (FastAPI), nor does it become tightly coupled to the database technology (SQLAlchemy).

## Decision

We have implemented a classic layered architecture internally within the FastAPI backend:
1. **API Routers (`app/api/routes/`)**: Handle HTTP, validate input/output using Pydantic, and inject dependencies. They contain **zero** business logic.
2. **Domain Services (`app/services/`)**: Contain the core business logic (e.g., matching prices to incomes, handling missing data gracefully, calculating burdens). They are purely functional or operate on abstract Repositories.
3. **Repositories (`app/repositories/`)**: Encapsulate SQLAlchemy queries. The Service layer never calls `session.query()` directly.
4. **Exceptions (`app/core/exceptions.py`)**: The Service layer throws `DomainException`s (like `NotFoundException`), which the API layer translates into standard HTTP 4xx/5xx responses using a global exception handler.

## Reliability and Retries
- **Transactions:** The `AnalyticsService` currently only reads data. In the future, ingestion services that *write* data must manage transactions explicitly, ensuring that a batch of `RawObservations` is committed atomically or rolled back entirely to prevent partial state.
- **Idempotency:** Re-running an analytics calculation for the same parameters will always yield the exact same result (pure function), making it entirely safe for frontend clients to retry on network failures.

## Consequences
- Testing the `AnalyticsService` requires mocking the repository, as demonstrated in `tests/unit/test_services.py`. This makes the unit tests blazing fast.
- The FastAPI routes are extremely thin and only require integration testing to ensure Pydantic schemas serialize correctly.
