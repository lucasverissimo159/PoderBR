# AGENTS.md — PoderBR

## 1. Mission

Construir uma plataforma web de inteligência sobre poder de compra e custo de vida no Brasil.

Pergunta central do MVP:
> Dada uma localização, período e base de renda, qual é o custo de uma cesta padronizada de proteínas, quanto da renda ela consome e como essa capacidade de compra mudou ao longo do tempo?

Proteínas são o primeiro domínio. O domínio deve evoluir para outras categorias sem redefinir o núcleo analítico.

## 2. Non-negotiable principles

1. **Evidence first.** Preferir fontes primárias e documentar provider, dataset/series/table, URL, retrieval time, unidade, frequência, geografia, transformações e cobertura.
2. **No fabricated observations.** Dados ausentes permanecem ausentes, salvo método explícito e versionado de estimativa/imputação.
3. **Methodology is product.** Todo indicador público tem fórmula, unidade, hipótese, versão e referência de fonte.
4. **Source != indicator.** Nunca tratar índice de preços como preço nominal nem vice-versa.
5. **Separation of concerns.** Raw ingestion, normalization, domain analytics, API, UI e presentation permanecem separados.
6. **Reproducibility.** Transformações devem ser determinísticas e rerunáveis a partir de snapshots/fixtures quando possível.
7. **Data provenance.** Toda observação analítica deve ser rastreável.
8. **Quality gates.** Mudanças de dados, schemas, APIs ou fórmulas exigem testes e validação.
9. **Version everything important.** Metodologia, basket, adapters e contratos devem possuir estratégia de versionamento compatível com evolução.
10. **Privacy by default.** Inputs anônimos do usuário não devem ser persistidos sem necessidade clara.
11. **No premature complexity.** Preferir modular monolith a microservices até existir evidência operacional.
12. **Honest UX.** Não transformar mudança do índice em afirmação genérica de bem-estar.

## 3. Product vocabulary

- `income_basis`: minimum_wage | regional_average_income | household_per_capita_income | user_income.
- `protein`: beef | pork | chicken | eggs, extensível.
- `basket`: conjunto versionado de itens, quantidade e unidade.
- `basket_cost`: custo da cesta em local/data.
- `income_burden`: basket_cost / income.
- `affordability_ratio`: income / basket_cost.
- `quantity_purchasable`: income / unit_price.
- `purchasing_power_index`: affordability normalizada contra base declarada.
- `nominal`: valor monetário do próprio período.
- `real`: valor ajustado por deflator declarado.
- `observation_status`: source_verified | normalized | estimated | missing.
- `methodology_version`: versão da definição usada para um indicador.

## 4. Default stack — hypotheses only

Começar investigando:
- Python + FastAPI ou Flask;
- pandas/polars quando justificado;
- PostgreSQL + Alembic;
- React + TypeScript ou alternativa fundamentada;
- Playwright/Vitest/pytest ou equivalentes;
- Docker + Compose;
- GitHub Actions;
- chart library moderna com acessibilidade adequada.

A stack não é imutável. Antes de trocá-la, pesquisar documentação oficial, maturidade, manutenção, testabilidade, deployment e compatibilidade com Jules; registrar decisão em ADR.

## 5. Research protocol

Para qualquer framework, biblioteca, API, fonte estatística, padrão ou serviço externo:
1. consultar documentação oficial atual;
2. preferir fontes primárias;
3. comparar alternativas quando a decisão for relevante;
4. registrar trade-offs;
5. não aceitar uma única fonte secundária como autoridade factual;
6. distinguir disponibilidade pública, licença, termos e estabilidade do endpoint.

## 6. Geography rules

O produto só pode declarar cobertura suportada pelas observações reais. Se a fonte cobre capitais/áreas de pesquisa, a UI deve dizer isso. Não preencher UFs faltantes por suposição.

Guardar no mínimo: country, region, state_uf, city_area, source_geo_id, source_geo_label.

## 7. Data source rules

Cada adapter deve fornecer: provider, dataset/table/series id, stable URL/reference, retrieval timestamp, unit, frequency, geography, methodology notes, snapshot/checksum quando possível, revision semantics e licensing/access notes.

Raw data, normalized observations e analytical outputs devem permanecer identificáveis.

## 8. Agent protocol

Todo agente deve:
1. ler `AGENTS.md`;
2. ler `docs/ORCHESTRATION.md`;
3. ler `docs/PROJECT_CONTEXT.md`;
4. ler `docs/AGENT_STATE.md` e `docs/OWNERSHIP.md` quando existirem;
5. ler seu `agent-context/*.md`;
6. inspecionar git status, branch, estrutura, ADRs e handoffs;
7. escrever um plano com hipóteses, dependências e arquivos previstos antes de grandes mudanças;
8. pesquisar quando o prompt pedir exploração;
9. evitar tocar superfícies fora do escopo;
10. executar testes relevantes;
11. atualizar docs/ADRs/handoff quando a mudança criar conhecimento durável;
12. finalizar com resumo, testes, riscos, decisões, limitações e próximo passo.

## 9. Cross-agent contract

Antes de alterar um contrato compartilhado, localizar o artefato canônico em `docs/contracts/` ou `docs/API_CONTRACTS.md`.

Não mudar nomes de campos, unidades, datas, enums, endpoints ou fórmulas compartilhadas silenciosamente.

Se a alteração é necessária:
- documentar a mudança;
- atualizar testes de contrato;
- considerar compatibilidade/backward compatibility;
- atualizar consumidores afetados;
- registrar ADR se for uma decisão arquitetural/metodológica.

## 10. Branch policy

- `research/<topic>` para pesquisa.
- `feature/<domain>-<objective>` para implementação.
- `fix/<issue>` para correção.
- `chore/<objective>` para manutenção.
- `audit/<scope>` para auditoria.

Cada sessão deve ter um objetivo lógico. Nunca force-reset/rewrite outra branch. Se conflito revelar problema estrutural, parar e propor ADR.

## 11. Quality gates

Antes de considerar uma tarefa concluída, verificar quando aplicável:
- unit tests;
- integration tests;
- contract tests;
- static/type checks;
- lint/format;
- frontend build;
- migration checks;
- data quality checks;
- accessibility smoke;
- security checks;
- reproducibility/local setup.

## 12. Definition of Done

Uma tarefa só está pronta quando:
- implementação/decisão existe;
- testes relevantes existem e passam;
- documentação necessária foi atualizada;
- nenhum claim estatístico sem suporte foi criado;
- interfaces compartilhadas estão consistentes;
- handoff registra decisões, arquivos, testes, riscos e próximos passos.
