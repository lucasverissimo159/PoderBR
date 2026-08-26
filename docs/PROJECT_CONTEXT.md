# Project Context — PoderBR

## Product

PoderBR é uma plataforma analítica pública para explicar como renda e preços afetam o poder de compra no Brasil.

### MVP

Primeiro domínio: proteínas — beef, pork, chicken, eggs.

Depois: outras categorias de consumo, somente se os dados e o produto justificarem.

## Primary questions

1. Quanto custa uma cesta proteica hoje?
2. Quanto da renda essa cesta consome?
3. Quantas cestas/quantidades a renda compra?
4. O poder de compra aumentou ou caiu em relação a um período-base?
5. Quanto da mudança veio de renda e quanto de preços?
6. Como a situação varia entre locais?

## Methodological boundaries

O produto mede **affordability relative to a defined basket**, não bem-estar econômico total.

Não confundir:
- preço nominal;
- índice de preços;
- renda nominal;
- renda real;
- affordability;
- purchasing power index.

## Basket

A cesta é configurável, versionada e acompanhada da justificativa das quantidades/pesos. Nunca tratá-la como verdade universal de consumo.

## Data maturity

- `source_verified`: observação direta com proveniência.
- `normalized`: observação transformada para schema canônico.
- `estimated`: valor calculado por método documentado.
- `missing`: sem observação defensável.

## User input

O usuário pode fornecer renda sem precisar criar conta. Não persistir esse dado por padrão.

## Geography

Cobertura inicial deve ser estritamente baseada na cobertura da fonte. Preferir menor cobertura defensável a maior cobertura por imputação.
