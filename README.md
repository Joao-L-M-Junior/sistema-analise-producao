# 📊 Sistema de Análise de Produção Industrial & SQL

Pipeline de ETL e análise de dados em Python desenvolvido para consolidação de produção industrial por turno, persistência relacional em **SQLite**, cálculo de indicadores de eficiência com **Pandas** e geração automatizada de relatórios e gráficos.

## 🚀 Funcionalidades

- **Modelagem Relacional (SQLite):** Armazenamento normalizado entre metas e registros diários de produção por turno com integridade referencial (`FOREIGN KEY`).
- **Consolidação SQL + Regras de Negócio em Python:** Agregação de volumes no banco de dados e cálculo de saldo de meta, eficiência percentual e status operacional via Pandas.
- **Visualização Executiva:** Geração automática de painel comparativo (`dashboard_producao.png`) confrontando produção realizada, metas e eficiência.
- **Exportação Tabular:** Geração dos relatórios `relatorio_consolidado.csv` e `relatorio_producao.csv`.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x** — Orquestração do pipeline e regras de negócio.
* **SQLite3** — Banco de dados relacional e consultas agregadas.
* **Pandas** — Transformação de dados, classificação de indicadores e exportação CSV.
* **Matplotlib** — Criação de gráficos comparativos.

## 🗄️ Consulta SQL de Consolidação

O banco de dados (`fabrica.db`) realiza a agregação inicial da produção antes do processamento analítico no Pandas:

```sql
SELECT 
    p.produto AS Produto,
    SUM(p.quantidade) AS Producao_Total,
    m.meta_quantidade AS Meta
FROM producao_diaria p
JOIN metas m ON p.produto = m.produto
GROUP BY p.produto;
```
