# PoderBR — Jules Agent Prompt Pack

Este pacote transforma o Jules em uma equipe coordenada para construir o **PoderBR**, uma plataforma de inteligência sobre poder de compra e custo de vida no Brasil.

O MVP começa com um domínio de proteínas (carne bovina, suína, frango e ovos), mas a arquitetura deve permitir adicionar outras categorias de consumo sem reescrever o núcleo.

## Princípios

- pesquisa antes de decisões técnicas;
- fontes primárias e rastreabilidade;
- nenhuma observação histórica inventada;
- contratos explícitos entre agentes;
- um agente = um objetivo lógico;
- branches/PRs para trabalho independente;
- ADRs para decisões arquiteturais ou metodológicas duráveis;
- testes obrigatórios para cálculos, ingestão e contratos;
- qualidade de dados como parte do produto;
- metodologia versionada;
- transparência sobre cobertura, estimativas e lacunas.

## Sequência principal

`00 Bootstrap → 01 Product → 02 Data Research → 03 Architecture → 04 Data Model → 05 Backend → 06 Ingestion → 07 Analytics → 08 API → 09 Frontend → 10 Dashboard → 11 QA → 12 Security/Platform → 13 Data Quality → 14 Performance/Reliability → 15 Docs/Portfolio → 16 Integration → 17 Release Audit`

Depois do release, use `18-agent-router.md` e `19-maintenance.md` para novas tarefas.

## Paralelização

Podem rodar em paralelo, quando não houver sobreposição de arquivos/contratos:

- 01 Product Research
- 02 Data Research
- pesquisas de UX e QA sem alteração de produção

Após os contratos principais, alguns agentes de implementação também podem ser paralelizados. O agente de integração sempre reconcilia o resultado.

## Uso com Jules

1. Crie o repositório GitHub.
2. Rode `00-bootstrap-repository.md` primeiro.
3. Revise e aprove o plano do Jules antes da execução em tarefas de arquitetura/metodologia.
4. Configure o ambiente do repositório no Jules e valide o setup/snapshot.
5. Para tarefas paralelas, use branches independentes.
6. Nunca presuma que alterações não commitadas de uma sessão existem em outra sessão.
7. Ao integrar, use o agente 16.

O Jules cria sessões de trabalho isoladas, suporta revisão de plano, branches/PRs e múltiplas tarefas simultâneas; `AGENTS.md` é lido automaticamente quando presente no root do repositório. O ambiente pode ser preparado por setup script e snapshot.

## Estrutura

- `AGENTS.md` — contrato operacional permanente.
- `agent-context/` — contexto especializado por papel.
- `prompts/` — tarefas executáveis por fase.
- `docs/` — arquitetura, produto, metodologia, qualidade e handoffs.
- `.github/ISSUE_TEMPLATE/` — formato para futuras tarefas do Jules.
