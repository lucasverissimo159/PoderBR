# ADR 0005: API Strategy, State, and Caching

## Context
We need to define how the FastAPI backend serves data to the React frontend. The data (prices, income, inflation) updates at most monthly (sometimes quarterly). It is heavily read-optimized.

## Decision

1. **Protocol & Style:** Synchronous REST over HTTP/1.1 via FastAPI. We will use path versioning (e.g., `/api/v1/...`) to ensure future agents can introduce breaking changes without destroying the initial MVP UI.
2. **State & Caching (Backend):** The backend is stateless. Because data updates infrequently (monthly), we will rely heavily on standard HTTP caching mechanisms (e.g., `Cache-Control: public, max-age=86400`). We will not introduce Redis or Memcached initially, relying instead on PostgreSQL query speed and HTTP caching at the edge/browser.
3. **State & Caching (Frontend):** The React frontend will use a data-fetching library like **TanStack Query (React Query)** or **SWR**. This handles local caching, deduping requests, and async UI states out of the box, fulfilling the need for a robust frontend state approach without building complex Redux stores for server state.
4. **Observability:** We will implement structured JSON logging using a library like `structlog`. Every API request must include a `request_id` passed through the log context to trace errors across the system easily.

## Consequences
- FastAPI endpoint functions will be `async def`, but they will rely on `asyncpg` (SQLAlchemy async) for database I/O to maximize throughput.
- Frontend developers/agents must configure React Query `staleTime` appropriately (e.g., 24 hours) to match the low-frequency data updates.
- Background jobs (like fetching new data from IBGE) will be executed via simple scheduled scripts (cron/GitHub Actions) rather than heavy task queues like Celery, given the infrequency of updates.
