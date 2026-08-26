# Prompt 00 — Bootstrap PoderBR and the Jules Operating System

Act as the Principal Engineer bootstrapping an empty repository named **PoderBR**. Do not build product features yet.

## Read first

`AGENTS.md`, `docs/PROJECT_CONTEXT.md`, `docs/ORCHESTRATION.md`, `docs/JULES_WORKFLOW.md`.

## Mission

Establish a repository that future Jules agents can understand, validate and extend without losing architectural or methodological context.

## Research before choosing

Use current official documentation to investigate at least two candidates for:
- backend framework;
- frontend framework/toolchain;
- database + migration tool;
- testing strategy;
- charting/accessibility strategy;
- local orchestration;
- CI/CD;
- relevant Brazilian public-data access patterns.

For each non-trivial choice document why the selected approach wins on maintainability, testability, ecosystem maturity, portfolio value and Jules compatibility. Do not choose only because you already know it.

## Create

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/ORCHESTRATION.md`
- `docs/JULES_WORKFLOW.md`
- `docs/adr/0001-initial-architecture.md`
- `docs/adr/0002-data-source-strategy.md`
- `docs/CONTRIBUTING.md`
- `docs/METHODOLOGY.md` skeleton with unverified sections marked
- `docs/AGENT_STATE.md` with current phase, completed gates, active work, blockers and next tasks
- `docs/OWNERSHIP.md` with file/domain ownership and shared-contract ownership
- `docs/handoffs/BOOTSTRAP.md`
- `.gitignore`, `.editorconfig`, license, formatting/lint config
- repository setup script(s) suitable for Jules
- initial GitHub Actions CI where justified
- minimal directory structure for app, data, analytics, tests, docs, scripts

## Jules-specific setup

The setup must be deterministic, lightweight and non-interactive. It should install dependencies, run a cheap validation, lint and test command. Do not start long-running development servers in setup. Document the setup and a clean-room validation command. Jules runs each task in a fresh VM and can reuse a validated environment snapshot, so setup quality is a first-class concern.

## Guardrails

- no authentication yet;
- no fabricated real-world data;
- fixtures must be clearly synthetic;
- no business formulas yet;
- no microservices unless evidence requires them.

## Exit criteria

A new Jules session should be able to clone the repo, read the root context, install dependencies, run checks and understand where each class of logic belongs.

Final output: selected/rejected technologies, official sources consulted, files created, validated commands, unresolved decisions and next three tasks.
