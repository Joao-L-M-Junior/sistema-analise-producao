import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# 1. ESTRUTURA DE DADOS INICIAL (Cenários variados de produção)
# -------------------------------------------------------------
Produtos = ['Tênis', 'Camiseta', 'Calça']
Turnos = ['Manhã', 'Tarde', 'Noite']

Metas_de_producao = {
    'Tênis': 1000,
    'Camiseta': 2000,
    'Calça': 1500
}

# Volumes variados para simular desempenho real por turno e produto
producao_por_turno = {
    'Tênis': {'Manhã': 420, 'Tarde': 390, 'Noite': 310},     # Total: 1120 (Superou a meta)
    'Camiseta': {'Manhã': 720, 'Tarde': 650, 'Noite': 410},  # Total: 1780 (Abaixo da meta)
    'Calça': {'Manhã': 520, 'Tarde': 580, 'Noite': 400}      # Total: 1500 (Exatamente na meta)
}

# -------------------------------------------------------------
# 2. PERSISTÊNCIA RELACIONAL NO SQLITE
# -------------------------------------------------------------
conn = sqlite3.connect('fabrica.db')
conn.execute("PRAGMA foreign_keys = ON;")
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
    produto TEXT NOT NULL,
    turno TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (produto) REFERENCES metas (produto)
)
''')

# Limpa registros anteriores para reexecução idempotente
cursor.execute("DELETE FROM producao_diaria")
cursor.execute("DELETE FROM metas")

for prod, meta_qtd in Metas_de_producao.items():
    cursor.execute(
        "INSERT INTO metas (produto, meta_quantidade) VALUES (?, ?)",
        (prod, meta_qtd)
    )

for prod, turnos_dict in producao_por_turno.items():
    for tur, qtd in turnos_dict.items():
        cursor.execute(
            "INSERT INTO producao_diaria (produto, turno, quantidade) VALUES (?, ?, ?)",
            (prod, tur, qtd)
        )

conn.commit()

# -------------------------------------------------------------
# 3. EXTRAÇÃO VIA SQL E REGRAS DE NEGÓCIO NO PANDAS
# -------------------------------------------------------------
# O SQLite consolida os volumes; o Python aplica as métricas de negócio
query_consolidada = '''
SELECT 
    p.produto AS Produto,
    SUM(p.quantidade) AS Producao_Total,
    m.meta_quantidade AS Meta
FROM producao_diaria p
JOIN metas m ON p.produto = m.produto
GROUP BY p.produto;
'''

df_consolidado = pd.read_sql_query(query_consolidada, conn)

# Cálculos e classificação feitos no Pandas
df_consolidado['Saldo_Meta'] = df_consolidado['Producao_Total'] - df_consolidado['Meta']
df_consolidado['Eficiencia_Pct'] = (
    (df_consolidado['Producao_Total'] / df_consolidado['Meta']) * 100
).round(2)

def classificar_status(eficiencia):
    if eficiencia > 100:
        return 'Acima da Meta'
    elif eficiencia == 100:
        return 'Meta Atingida'
    return 'Abaixo da Meta'

df_consolidado['Status'] = df_consolidado['Eficiencia_Pct'].apply(classificar_status)
df_consolidado = df_consolidado.sort_values(by='Eficiencia_Pct', ascending=False).reset_index(drop=True)

# Consulta detalhada por turno para exportação e visualização
query_turnos = '''
SELECT 
    p.produto AS Produto,
    p.turno AS Turno,
    p.quantidade AS Quantidade,
    m.meta_quantidade AS Meta_Diaria
FROM producao_diaria p
JOIN metas m ON p.produto = m.produto;
'''
df_turnos = pd.read_sql_query(query_turnos, conn)
conn.close()

# Exportação dos relatórios em CSV
df_consolidado.to_csv('relatorio_consolidado.csv', index=False, encoding='utf-8-sig')
df_turnos.to_csv('relatorio_producao.csv', index=False, encoding='utf-8-sig')

print("\n--- Relatório Consolidado (SQL + Pandas) ---")
print(df_consolidado.to_string(index=False))

# -------------------------------------------------------------
# 4. VISUALIZAÇÃO GRÁFICA (MATPLOTLIB)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Gráfico 1: Produção Realizada vs Meta
x = np.arange(len(df_consolidado['Produto']))
largura = 0.35

barras_real = ax1.bar(x - largura/2, df_consolidado['Producao_Total'], largura, label='Produção Real', color='#1f77b4', edgecolor='black')
barras_meta = ax1.bar(x + largura/2, df_consolidado['Meta'], largura, label='Meta', color='#aec7e8', edgecolor='black')

ax1.bar_label(barras_real, padding=3, fontsize=9, fontweight='bold')
ax1.bar_label(barras_meta, padding=3, fontsize=9)
ax1.set_title('Produção Total vs. Meta por Produto', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(df_consolidado['Produto'])
ax1.set_ylabel('Unidades')
ax1.set_ylim(0, df_consolidado[['Producao_Total', 'Meta']].values.max() * 1.18)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.set_axisbelow(True)
ax1.legend()

# Gráfico 2: Eficiência (%) com linha de referência de 100%
cores_status = {
    'Acima da Meta': '#2ca02c',
    'Meta Atingida': '#1f77b4',
    'Abaixo da Meta': '#d62728'
}
cores_barras = df_consolidado['Status'].map(cores_status)

barras_efic = ax2.bar(df_consolidado['Produto'], df_consolidado['Eficiencia_Pct'], color=cores_barras, edgecolor='black', width=0.5)
ax2.axhline(100, color='black', linestyle='--', linewidth=1.2, label='Meta (100%)')

ax2.bar_label(barras_efic, fmt='%.1f%%', padding=3, fontsize=10, fontweight='bold')
ax2.set_title('Eficiência Operacional (%) por Produto', fontsize=12, fontweight='bold')
ax2.set_ylabel('Eficiência (%)')
ax2.set_ylim(0, df_consolidado['Eficiencia_Pct'].max() * 1.18)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.set_axisbelow(True)
ax2.legend()

plt.tight_layout()
plt.savefig('dashboard_producao.png', dpi=150)
plt.show()