import os
import pandas as pd

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
        "count": "Contagem",
        "mean": "Média",
        "std": "Desvio Padrão",
        "min": "Mínimo",
        "25%": "Primeiro Quartil",
        "50%": "Mediana",
        "75%": "Terceiro Quartil",
        "Max": "Máximo"
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
    coluna = input(
        "--------------------Buscador de Colunas--------------------\n --Caso você deseje sair digite 'parar'\n"
        "Nome da coluna que você deseja pesquisar: ").strip().upper()
    if coluna == "PARAR":
        print("busca fechada")
        break
    if coluna not in tabela_vivos2024.columns:
        print("tabela não encontrada")
        continue

    coluna1 = tabela_vivos2024[coluna]
    info = coluna1.describe()

    #TODO if que traduza valores não númericos, valores extensos que estão em codigo, tenho o nome dessas pastas em dicionario_projeto

    info.loc["Moda"] = coluna1.mode().iloc[0]

    # Substitui o nome das variáveis em vez de ser nomes em inglês, troca pelos em português, deixando na mesma variável
    info1 = info.rename(index=dicionario_projeto["pesquisa"])
    # arredonda resultado do describe
    info1 = round(info1, 2)

    with open(caminho_txt, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome da coluna: {coluna}\n{info1.to_string()}\n\n\n")

    print(info1.to_string())

