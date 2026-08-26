# Agent Orchestration

## Objective

Usar Jules como uma equipe de agentes especializados, com memória persistida em arquivos, contratos compartilhados e handoffs.

## Source of truth hierarchy

1. `AGENTS.md`
2. ADRs em `docs/adr/`
3. contratos canônicos em `docs/contracts/`
4. `docs/AGENT_STATE.md` e `docs/OWNERSHIP.md`
5. `docs/PROJECT_CONTEXT.md`
5. product/methodology specs
6. specialist contexts
7. task prompts
8. assumptions locais do agente

## Roles

- Product Research
- Data Research
- Architecture
- Data Engineering
- Backend/Domain
- Data Ingestion
- Analytics
- API
- Frontend
- Dashboard/Visualization
- QA
- Security/Platform
- Data Quality/Observability
- Performance/Reliability
- Documentation/Portfolio
- Integration
- Release Audit
- Agent Router/Maintenance

## Execution graph

```text
00 Bootstrap
  ├── 01 Product Research
  └── 02 Data Research
          ↓
       03 Architecture
          ↓
       04 Data Model/ETL
          ↓
   ┌──────┼────────┬─────────┐
   ↓      ↓        ↓         ↓
05 BE   06 Data 07 Analytics 12 Platform*
   └──────┼────────┴─────────┘
          ↓
        08 API
          ↓
   ┌──────┴──────┐
   ↓             ↓
09 Frontend   11 QA*
   ↓             ↓
10 Dashboard    13 Data Quality
   └──────┬──────┘
          ↓
14 Performance
          ↓
15 Documentation
          ↓
16 Integration
          ↓
17 Release Audit
```

`*` podem rodar em paralelo quando suas superfícies não colidem.

## Safe parallelism

Seguro:
- product vs data research;
- research vs documentation research;
- independent test planning;
- security review sem alterar o mesmo código de feature.

Evitar:
- múltiplas migrações simultâneas;
- backend e frontend redefinindo API simultaneamente;
- dois agentes alterando a mesma fórmula;
- dois agentes editando o mesmo arquivo de configuração central.

## Handoff

Todo agente deve preencher `docs/handoffs/<task-id>.md` usando `docs/handoffs/TEMPLATE.md`.

Campos mínimos:
- objective;
- decisions;
- evidence/sources;
- files changed;
- interfaces changed;
- tests/checks;
- limitations;
- risks;
- next tasks.

## Conflict protocol

Se duas abordagens divergirem:
1. não escolher silenciosamente;
2. comparar evidências;
3. criar/atualizar ADR;
4. escolher explicitamente;
5. atualizar consumidores e testes.

## Jules-specific operations

Jules roda cada tarefa em VM isolada, pode executar múltiplas tarefas e permite revisão do plano antes da execução. O repositório deve ter setup determinístico e leve; o ambiente pode ser validado e salvo como snapshot.
