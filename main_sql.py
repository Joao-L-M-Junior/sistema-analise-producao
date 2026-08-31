import sqlite3
import pandas as pd

# -------------------------------------------------------------
# 1. ESTRUTURA DE DADOS INICIAL
# -------------------------------------------------------------
Produtos = ['Tênis', 'Camiseta', 'Calça']
Turnos = ['Manhã', 'Tarde', 'Noite']

Metas_de_producao = {
    'Tênis': 1000,
    'Camiseta': 2000,
    'Calça': 1500
}

producao_por_turno = {
    'Tênis': {'Manhã': 400, 'Tarde': 350, 'Noite': 250},
    'Camiseta': {'Manhã': 800, 'Tarde': 700, 'Noite': 500},
    'Calça': {'Manhã': 500, 'Tarde': 600, 'Noite': 400}
}

# -------------------------------------------------------------
# 2. FUNÇÕES DE CÁLCULO
# -------------------------------------------------------------
def calcular_producao_total(dados):
    total = {}
    for produto in Produtos:
        total[produto] = sum(dados[produto].values())
    return total

def calcular_eficiencia(total, metas):
    eficiencia = {}
    for produto in Produtos:
        eficiencia[produto] = (total[produto] / metas[produto]) * 100
    return eficiencia

total = calcular_producao_total(producao_por_turno)
eficiencia = calcular_eficiencia(total, Metas_de_producao)

# -------------------------------------------------------------
# 3. PREPARAÇÃO TABULAR (Pandas) E BANCO DE DADOS (SQLite)
# -------------------------------------------------------------
dados_tabela = []

for produto in Produtos:
    meta = Metas_de_producao[produto]
    tot = total[produto]
    efic = eficiencia[produto]
    
    for turno in Turnos:
        qtd_turno = producao_por_turno[produto][turno]
        dados_tabela.append({
            'Produto': produto,
            'Turno': turno,
            'Producao_Turno': qtd_turno,
            'Producao_Total': tot,
            'Meta': meta,
            'Eficiencia_Pct': round(efic, 2)
        })

df_producao = pd.DataFrame(dados_tabela)
df_producao.to_csv('relatorio_producao.csv', index=False, encoding='utf-8-sig')

conn = sqlite3.connect('fabrica.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS metas (
    produto TEXT PRIMARY KEY,
    meta_quantidade INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS producao_diaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    turno TEXT,
    quantidade INTEGER,
    FOREIGN KEY (produto) REFERENCES metas (produto)
)
''')

cursor.execute("DELETE FROM metas")
cursor.execute("DELETE FROM producao_diaria")

for prod, meta_qtd in Metas_de_producao.items():
    cursor.execute("INSERT INTO metas (produto, meta_quantidade) VALUES (?, ?)", (prod, meta_qtd))

for prod, turnos_dict in producao_por_turno.items():
    for tur, qtd in turnos_dict.items():
        cursor.execute("INSERT INTO producao_diaria (produto, turno, quantidade) VALUES (?, ?, ?)", (prod, tur, qtd))

conn.commit()

# -------------------------------------------------------------
# 4. CONSULTA SQL CONSOLIDADORA
# -------------------------------------------------------------
query_sql = '''
SELECT 
    p.produto AS Produto,
    SUM(p.quantidade) AS Producao_Total,
    m.meta_quantidade AS Meta,
    ROUND((CAST(SUM(p.quantidade) AS FLOAT) / m.meta_quantidade) * 100, 2) AS Eficiencia_Porcentagem
FROM producao_diaria p
JOIN metas m ON p.produto = m.produto
GROUP BY p.produto;
'''

df_resultado_sql = pd.read_sql_query(query_sql, conn)
print("\n--- Relatório SQL Consolidado ---")
print(df_resultado_sql.to_string(index=False))

conn.close()