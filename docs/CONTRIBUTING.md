# Contributing to PoderBR

Welcome to PoderBR! We use Jules as our primary AI agent collaborator, but human contributions and reviews are essential.

## How to Contribute

1.  **Read the Context**: Before making any changes, please read the documentation in `docs/` and the `AGENTS.md` file in the root.
2.  **Branching Strategy**: Use feature branches with the format `feature/<domain>-<objective>`, e.g., `feature/proteins-beef-ingestion`.
3.  **Local Setup**: Run `./scripts/setup.sh` to initialize your local environment and run the test suite.
4.  **Testing**: All new features and bug fixes must have accompanying unit and/or integration tests. Run tests via `uv run pytest`.
5.  **Linting**: The codebase is formatted with `black` and linted with `ruff`. Ensure these pass before committing. The setup script will run them for you.
6.  **ADRs**: If you are making an architectural or significant methodological decision, create an ADR in `docs/adr/`.
7.  **Pull Requests**: Open a pull request against the `main` branch. Ensure the CI pipeline passes.

## AI Agent Workflow

If you are a Jules agent working on this repository, strictly adhere to the `docs/JULES_WORKFLOW.md` and the roles defined in `docs/ORCHESTRATION.md`. Update `docs/AGENT_STATE.md` and `docs/handoffs/` when completing a task.
