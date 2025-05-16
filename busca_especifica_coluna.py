import os
import pandas as pd
import matplotlib.pyplot as plt

"""Gráfico com
Mães menores de idade(com faixa etária) Que mostre a mortalidade entre as faixas e razoes de morte"""

caminho_tabela_vivos2024 = r"dados/2024/dados-de-nascidos-vivos-2024-jun.csv"
tabela_vivos2024 = pd.read_csv(caminho_tabela_vivos2024, sep = ";")

nome_arquivo = os.path.basename(caminho_tabela_vivos2024).split(".")[0]
nome_arquivo = nome_arquivo + ".txt"

caminho_pasta_txts = r"dados_filtrados\dados_especificos\\"

if not os.path.exists(caminho_pasta_txts):
    os.makedirs(caminho_pasta_txts)

caminho_txt = os.path.join(caminho_pasta_txts, nome_arquivo)

# dicionário da planilha retirada do PDF
dicionario_projeto = {
    "pesquisa": {
        "count": "Registro",
        "mean": "Média",
        "std": "Desvio Padrão",
        "min": "Mínimo",
        "25%": "Primeiro Quartil",
        "50%": "Mediana",
        "75%": "Terceiro Quartil",
        "max": "Máximo"
    },
    "locnasc": {
        9: "Ignorado",
        1: "Hospital",
        2: "Outro Estab Saúde",
        3: "Domicílio",
        4: "Outros"
    },
    "estcivmae": {
        1: "Solteira",
        2: "Casada",
        3: "Viúva",
        4: "Separado judicialmente/Divorciado",
        9: "Ignorado"
    },
    "escmae": {
        1: "Nenhuma",
        2: "1 a 3 anos",
        3: "4 a 7 anos",
        4: "8 a 11 anos",
        5: "12 e mais",
        9: "Ignorado"
    },
    "gestacao": {
        9: "Ignorado",
        1: "Menos de 22 semanas",
        2: "22 a 27 semanas",
        3: "28 a 31 semanas",
        4: "32 a 36 semanas",
        5: "37 a 41 semanas",
        6: "42 semanas e mais"
    },
    "gravidez": {
        9: "Ignorado",
        1: "Única",
        2: "Dupla",
        3: "Tripla e mais"
    },
    "parto": {
        9: "Ignorado",
        1: "Vaginal",
        2: "Cesáreo"
    },
    "consultas": {
        1: "Nenhuma",
        2: "de 1 a 3",
        3: "de 4 a 6",
        4: "7 e mais",
        9: "Ignorado"
    },
    "sexo": {
        0: "Ignorado",
        1: "Masculino",
        2: "Feminino"
    },
    "racacor": {
        1: "Branca",
        2: "Preta",
        3: "Amarela",
        4: "Parda",
        5: "Indígena"
    },
    "idanomal": {
        9: "Ignorado",
        1: "Sim",
        2: "Não"
    }
}

"""nomes_dicionarios = [
    "locnasc",
    "estcivmae",
    "escmae",
    "gestacao",
    "gravidez",
    "parto",
    "consultas",
    "sexo",
    "racacor",
    "idanomal"
]"""

while True:
    soma = 0
    coluna = input(
        "--------------------Buscador de Colunas--------------------\n --Caso você deseje sair digite 'parar'\n"
        "Nome da coluna que você deseja pesquisar: ").strip().upper()

    if coluna == "PARAR":
        print("busca fechada")
        break

    busca = int(input("Qual o valor que voce quer "))

    if coluna not in tabela_vivos2024.columns:
        print("tabela não encontrada")
        continue


    coluna1 = tabela_vivos2024[coluna]
    info = coluna1.describe()

    #TODO if que traduza valores não númericos, valores extensos que estão em codigo, tenho o nome dessas pastas em dicionario_projeto



    info.loc["Moda"] = coluna1.mode().iloc[0]
    #metodo novo de contar
    info.loc["Frequencia"] = coluna1.value_counts().get(busca, 0)  #ele pega a contagem do valor buscado se nao existir retorna = 0
    info.loc["maternidade precoce"] = coluna1.value_counts().get(17, 0)

    for i, valor in enumerate(coluna1):  # coluna1 já é a coluna
        if valor < 20:
            soma += 1
    info.loc["maternidade precoce"] = soma

    #retira o cont/registro
    info = info.drop("count", errors="ignore")

    # Substitui o nome das variáveis em vez de ser nomes em inglês, troca pelos em português, deixando na mesma variável
    info1 = info.rename(index=dicionario_projeto["pesquisa"])

    info1 = round(info1, 2)

    info1_str = info1.to_string()

    with open(caminho_txt, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome da coluna: {coluna}\n{info1_str}\n\n\n")

    def cria_grafico():
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Dados sem frequência
        dados_sem_frequencia = info1.drop("Frequencia")
        dados_com_frequencia = info1["Frequencia"]

        # Primeiro eixo Y
        ax1.bar(dados_sem_frequencia.index, dados_sem_frequencia.values, color='steelblue')
        ax1.set_ylabel('Outras Estatísticas')
        ax1.tick_params(axis='x', rotation=45)

        # Segundo eixo Y
        ax2 = ax1.twinx()
        ax2.bar(["Frequencia"], [dados_com_frequencia], color='orange', width=0.4)
        ax2.set_ylabel('Frequência')

        plt.title(f"{coluna}")
        plt.tight_layout()
        plt.show()
        #plt.savefig(f"{coluna}_estatisticas.png", dpi=300)

    cria_grafico()
    print(info1_str)



#metodo antigo de contar
"""    for i, valor in enumerate(coluna1):  # coluna1 já é a coluna
        if valor == busca:
            soma += 1
    info.loc["Frequencia"] = soma"""


