# Dados para o sistema de produção

Produtos = ['Tênis', 'Camiseta', 'Calça']
Turnos = ['Manhã', 'Tarde', 'Noite']


Funcionarios_da_produçao = ['João', 'Maria', 'Pedro', 'Ana']
Funcionarios_da_embalagem = ['Paulo', 'Mariana', 'Gustavo', 'Luiz']
Funcionarios_da_qualidade = ['José', 'Vitor', 'Simone', 'Luana']
Setores = ['Produção', 'Embalagem', 'Qualidade']
Líder_da_produçao = 'Carlos'
Líder_da_embalagem = 'Fernanda'
Líder_da_qualidade = 'Roberto'
Metas_de_produçao = {
    'Tênis': 1000,
    'Camiseta': 2000,
    'Calça': 1500
}

# Função para calcular a produção total de cada produto
def calcular_producao_total(producao_por_turno):
    producao_total = {}
    for produto in Produtos:
        producao_total[produto] = sum(producao_por_turno[produto].values())
    return producao_total

# Função para calcular a eficiência de cada setor
def calcular_eficiencia(producao_total, metas):
    eficiencia = {}
    for produto in Produtos:
        eficiencia[produto] = (producao_total[produto] / metas[produto]) * 100
    return eficiencia

# Função para gerar relatório de produção
def gerar_relatorio(producao_por_turno, producao_total, eficiencia):
    print("Relatório de Produção")
    print("====================")
    for produto in Produtos:
        print(f"Produto: {produto}")
        for turno in Turnos:
            print(f"  Turno {turno}: {producao_por_turno[produto][turno]} unidades")
        print(f"  Produção Total: {producao_total[produto]} unidades")
        print(f"  Eficiência: {eficiencia[produto]:.2f}%")
        print("--------------------")

# 1. Defina os dados de entrada (produção real por turno)
producao_por_turno = {
    'Tênis': {'Manhã': 400, 'Tarde': 350, 'Noite': 250},
    'Camiseta': {'Manhã': 800, 'Tarde': 700, 'Noite': 500},
    'Calça': {'Manhã': 500, 'Tarde': 600, 'Noite': 400}
}

# 2. Execute as funções passando os dados necessários
total = calcular_producao_total(producao_por_turno)
eficiencia = calcular_eficiencia(total, Metas_de_produçao)

# 3. Gere o relatório final
gerar_relatorio(producao_por_turno, total, eficiencia)