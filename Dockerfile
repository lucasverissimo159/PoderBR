# Stage 1: Build dependencies
FROM python:3.12-slim-bookworm AS builder

# Prevent python from writing pyc files and keep stdout unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN groupadd -r poderbr && useradd -r -g poderbr poderbr

WORKDIR /app

# Copy from builder
COPY pyproject.toml .
# Normally we would install from wheels, but for simplicity in this MVP we just pip install directly
# since we have a pure python app mostly. We still use the multi-stage to drop build-essential if it were needed.
# For production, lock files (like requirements.txt generated from uv or pdm) are strongly recommended.
RUN pip install --no-cache-dir -e .

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Set permissions
RUN chown -R poderbr:poderbr /app

USER poderbr

# Expose API port
EXPOSE 8000

# Basic healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
