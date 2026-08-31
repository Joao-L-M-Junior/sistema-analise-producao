# 📊 Sistema de Análise de Produção Industrial & SQL

Projeto em Python desenvolvido para automação de relatórios de produção por turno, cálculo de métricas de eficiência operacional e integração relacional utilizando **SQLite** e **Pandas**.

## 🚀 Funcionalidades

- **Cálculo de Eficiência Operacional:** Processamento automatizado de metas vs. produção realizada.
- **Estruturação Tabular:** Transformação dos relatórios com a biblioteca Pandas.
- **Modelagem SQL (SQLite):** Persistência dos dados brutos e consultas agregadas em banco relacional.
- **Exportação de Dados:** Geração automática de relatórios em formato CSV.

## 🛠️ Tecnologias Utilizadas

* **Python 3.14** — Regras de negócio e processamento principal.
* **Pandas** — Manipulação e exportação de dados tabulares.
* **SQLite3** — Armazenamento e execução de consultas relacionais.

## 🗄️ Estrutura do Banco de Dados

O banco de dados relacional (`fabrica.db`) utiliza a seguinte consulta SQL para consolidação dos resultados:

```sql
SELECT 
    p.produto AS Produto,
    SUM(p.quantidade) AS Producao_Total,
    m.meta_quantidade AS Meta,
    ROUND((CAST(SUM(p.quantidade) AS FLOAT) / m.meta_quantidade) * 100, 2) AS Eficiencia_Porcentagem
FROM producao_diaria p
JOIN metas m ON p.produto = m.produto
GROUP BY p.produto;