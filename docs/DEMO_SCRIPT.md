# PoderBR Demo Script (3-Minute Walkthrough)

*This script is designed for a technical recruiter, open-source maintainer, or incoming engineer.*

---

**[0:00 - 0:30] Introduction & The "Why"**
"Welcome to PoderBR. Inflation numbers are often abstract, so this platform answers a very relatable question: *How much of a minimum wage does it take to buy a basic basket of proteins today compared to a year ago?*
We aren't claiming to measure overall welfare or total cost of living. This is a highly specific, statistically honest Purchasing Power Index (PPI) built entirely on public data from IBGE and Ipeadata."

**[0:30 - 1:15] The Architecture & Backend**
"Under the hood, this is a Modular Monolith. The backend is Python and FastAPI, using SQLAlchemy for our PostgreSQL data model.
Notice the separation of concerns: Our data ingestion pipeline is entirely isolated from the synchronous API. We pull data, normalize it, and enforce strict idempotency via SQLite/Postgres `ON CONFLICT` constraints. We wrap these external API calls with `tenacity` for exponential backoffs, ensuring our scheduled jobs don't fail due to intermittent government API timeouts."

**[1:15 - 2:00] Data Quality & Observability**
"Let's look at the `QualityService`. In data journalism, silent data interpolation is dangerous. If a price is missing, our Analytics engine drops the metric for that month entirely.
However, we also look for anomalies. We check the database for data staleness (older than 45 days) or crazy Month-over-Month price spikes (> 50%). We don't delete this data—we just flag it, and expose it via our `/quality/status` API endpoint. You can see this surfaced in the UI inside the Methodology Disclosure panel as a warning badge."

**[2:00 - 2:30] Frontend & Accessibility**
"Moving to the frontend, we are using React, Vite, and Tailwind CSS. We use React Query for caching API calls.
Accessibility is a massive priority. We use Recharts for visual trends, but Recharts outputs SVG, which is terrible for screen readers. So, we built an `AccessibleChart` wrapper. With one click—or keyboard tab—users can swap any visual chart out for a fully semantic HTML `DataTable`."

**[2:30 - 3:00] Testing, CI/CD & Wrap-up**
"Finally, the platform is secure and tested. We have unit tests, Playwright End-to-End tests, and even Property-based fuzzing tests using `hypothesis` to ensure our mathematical engine never crashes with a `ZeroDivisionError` on extreme edge cases. Docker runs as a non-root user, and the API enforces strict Rate-Limiting via `slowapi`."
