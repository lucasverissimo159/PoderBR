# Jules Workflow

## Before starting a task

- escolha a branch de origem correta;
- leia o contexto obrigatório;
- confirme dependências com outras tarefas;
- revise o prompt e peça plano para mudanças arquiteturais;
- confira setup/environment.

## During task

- não iniciar processos long-running no setup;
- manter mudanças focadas;
- usar fixtures para fontes externas;
- registrar decisões e bloqueios;
- intervir quando o agente desviar da metodologia.

## After task

- revisar diff;
- revisar testes;
- revisar mudanças de contrato;
- revisar docs/handoff;
- decidir branch/PR;
- integrar somente depois de resolver incompatibilidades.

## Feedback examples

"Releia o ADR de metodologia. A alteração atual mistura preço nominal e índice de inflação. Reestruture a implementação, adicione um teste de unidade e atualize o contrato analítico."

"A cobertura geográfica proposta não é suportada pela fonte. Não impute silenciosamente. Rebaixe os locais sem observação para missing e atualize a disclosure de cobertura."
