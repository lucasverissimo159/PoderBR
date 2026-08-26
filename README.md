# PoderBR

PoderBR is a public analytics platform designed to explain how income and prices affect purchasing power in Brazil.

## Mission

Our central question is:
> Given a location, period, and income basis, what is the cost of a standardized basket of proteins, how much of the income does it consume, and how has this purchasing power changed over time?

We start with the proteins domain (beef, pork, chicken, eggs) and will evolve to other consumption categories.

## Core Principles

- **Evidence first:** Primary sources, documented provenance.
- **No fabricated observations:** Missing data remains missing unless explicitly imputed by versioned methods.
- **Methodology is product:** Every indicator has a formula, unit, hypothesis, and reference.
- **Reproducibility:** Transformations are deterministic and rerunnable.
- **Privacy by default:** Anonymous user inputs are not persisted.

## For Developers and AI Agents

This repository is designed to be worked on by humans and AI agents (like Jules) collaboratively.

*   Please read `AGENTS.md` for non-negotiable principles and agent protocols.
*   See `docs/PROJECT_CONTEXT.md` for product details.
*   See `docs/ORCHESTRATION.md` for agent roles and execution graphs.
*   See `docs/CONTRIBUTING.md` for local setup and contribution guidelines.

## Local Setup

To set up the repository deterministically:

```bash
./scripts/setup.sh
```

This will set up the Python environment using `uv`, install dependencies, run linters, and execute the test suite.
