# Prompt Operations Guide

## Regra

Os prompts são coordenadores, não substitutos de análise. O agente deve pesquisar, justificar e verificar.

## Ordem

00–04 sequenciais.
05–07 podem ser parcialmente paralelos se os contratos estiverem congelados.
08 depende dos contratos e domínio.
09–10 dependem da API.
11–14 são quality gates e podem ter trabalho paralelo controlado.
15–17 consolidam e auditam.
18–19 servem para evolução contínua.

## Plan approval

Para arquitetura, metodologia, mudança de stack, alteração de schema crítico ou mudança de contrato, exigir revisão do plano antes da execução. O Jules suporta aprovação explícita do plano e a API possui `requirePlanApproval`.

## Environment

Mantenha setup script pequeno, determinístico e executável em VM efêmera. O Jules oferece snapshots de ambiente para reduzir custo de setup.

## Programmatic orchestration

Caso futuramente você automatize o Jules via API, trate cada sessão como uma unidade de trabalho e mantenha o prompt específico. A API permite criar sessões a partir de uma branch/contexto e automatizar PRs.
