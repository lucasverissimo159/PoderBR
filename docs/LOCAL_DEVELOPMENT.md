# Local Development Guide

This guide outlines the process for setting up a clean-room development environment for PoderBR. Our goal is deterministic, fast, and reliable environment setup.

## Prerequisites

- Python 3.11+
- Node.js 22+
- Git

## Bootstrap

We use `uv` (an extremely fast Python package installer and resolver) to manage dependencies. Our `setup.sh` script automates the process:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
1. Create an isolated virtual environment (`.venv`).
2. Install all backend dependencies including dev tools (pytest, ruff, black).
3. Run the linters to verify a clean state.

## Running the Application

The architecture is split into a FastAPI backend and a Vite/React frontend.

### 1. Start the Backend
Activate the virtual environment and start Uvicorn:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
The API documentation will be available at `http://localhost:8000/docs`.

### 2. Start the Frontend
In a new terminal window, navigate to the frontend directory:

```bash
cd app/frontend
npm install
npm run dev
```
The UI will be available at `http://localhost:5173`. The Vite config automatically proxies `/api` requests to the backend on port 8000.

## Quality Assurance & Testing

Before committing, you must ensure all checks pass. Our CI pipeline enforces strict formatting and typing.

**Backend Checks:**
```bash
source .venv/bin/activate

# Format and Lint
ruff check . --fix
ruff format .

# Run Tests
pytest
```

**Frontend Checks:**
```bash
cd app/frontend

# Type Check and Lint
npm run lint
npm run build

# Run Unit Tests
npm run test

# Run End-to-End Tests (requires backend to be running)
npx playwright test
```

## Database Migrations
When changing SQLAlchemy models in `app/models/core.py`, you must generate a new Alembic migration:

```bash
source .venv/bin/activate
alembic revision --autogenerate -m "description_of_change"
alembic upgrade head
```
