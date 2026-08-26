# Jules Workflow

## Before starting a task

- Escolha a branch de origem correta;
- Leia o contexto obrigatório (`AGENTS.md`, `docs/PROJECT_CONTEXT.md`, etc);
- Confirme dependências com outras tarefas em `docs/AGENT_STATE.md`;
- Revise o prompt e peça plano para mudanças arquiteturais;
- Confira setup/environment rodando `./scripts/setup.sh`.

## During task

- Não iniciar processos long-running no setup;
- Manter mudanças focadas;
- Usar fixtures para fontes externas;
- Registrar decisões em `docs/adr/` e bloqueios em `docs/AGENT_STATE.md`;
- Intervir (humanos) quando o agente desviar da metodologia.

## After task

- Revisar diff;
- Revisar testes executando `uv run pytest`;
- Revisar mudanças de contrato em `docs/OWNERSHIP.md` e schemas;
- Preencher `docs/handoffs/<task-id>.md` baseado no `docs/handoffs/BOOTSTRAP.md` template;
- Decidir branch/PR;
- Integrar somente depois de resolver incompatibilidades.

## Feedback examples

"Releia o ADR de metodologia. A alteração atual mistura preço nominal e índice de inflação. Reestruture a implementação, adicione um teste de unidade e atualize o contrato analítico."

"A cobertura geográfica proposta não é suportada pela fonte. Não impute silenciosamente. Rebaixe os locais sem observação para missing e atualize a disclosure de cobertura."
