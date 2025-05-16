import os
import pandas as pd
import matplotlib.pyplot as plt

"""Gráfico com
Mães menores de idade(com faixa etária) Que mostre a mortalidade entre as faixas e razoes de morte"""

caminho_tabela_vivos2024 = r"dados/2024/dados-de-nascidos-vivos-2024-jun.csv"
tabela_vivos2024 = pd.read_csv(caminho_tabela_vivos2024, sep = ";")

nome_arquivo = os.path.basename(caminho_tabela_vivos2024).split(".")[0]
nome_arquivo = nome_arquivo + ".txt"

caminho_pasta_txts = r"dados_filtrados\dados_especificos\notacoes_txt\\"
caminho_pasta_graficos = r"dados_filtrados\dados_especificos\graficos\\"

if not os.path.exists(caminho_pasta_txts):
    os.makedirs(caminho_pasta_txts)

if not os.path.exists(caminho_pasta_graficos):
    os.makedirs(caminho_pasta_graficos)

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


    if coluna not in tabela_vivos2024.columns:
        print("tabela não encontrada")
        continue


    coluna1 = tabela_vivos2024[coluna]
    info = coluna1.describe()


    info.loc["Moda"] = coluna1.mode().iloc[0]
    #metodo novo de contar

    if coluna == "IDADEMAE":
        info.loc["maternidade precoce"] = (coluna1 < 20).sum()

    # Substitui o nome das variáveis em vez de ser nomes em inglês, troca pelos em português, deixando na mesma variável
    info1 = info.rename(index=dicionario_projeto["pesquisa"])

    info1 = round(info1, 2)

    info1_str = info1.to_string()

    with open(caminho_txt, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome da coluna: {coluna}\n{info1_str}\n\n\n")

    def dados():
        if coluna == "IDADEMAE":
            df = tabela_vivos2024.copy()
            df["IDADEMAE"] = pd.to_numeric(df["IDADEMAE"], errors="coerce")
            df = df.dropna(subset=["IDADEMAE"])
            bins = list(range(10, 65, 5))
            labels = [f"{i+1}-{i+5}" for i in bins[:-1]]
            df["faixa_etaria"] = pd.cut(df["IDADEMAE"], bins=bins, labels=labels, right=True)
            contagem = df["faixa_etaria"].value_counts().sort_index()
            plt.figure(figsize=(10, 6))
            contagem.plot(kind="bar", color="skyblue", edgecolor="black")
            plt.title("Número de Mães por Faixa Etária")
            plt.xlabel("Faixa Etária (anos)")
            plt.ylabel("Número de Nascimentos")
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)
            plt.show()

        if coluna == "IDADEPAI":
            df = tabela_vivos2024.copy()
            df["IDADEPAI"] = pd.to_numeric(df["IDADEPAI"], errors="coerce")
            df = df.dropna(subset=["IDADEPAI"])
            bins = list(range(10, 65, 5))
            labels = [f"{i+1}-{i+5}" for i in bins[:-1]]
            df["faixa_etaria"] = pd.cut(df["IDADEPAI"], bins=bins, labels=labels, right=True)
            contagem = df["faixa_etaria"].value_counts().sort_index()
            plt.figure(figsize=(10, 6))
            contagem.plot(kind="bar", color="skyblue", edgecolor="black")
            plt.title("Número de Pais por Faixa Etária")
            plt.xlabel("Faixa Etária (anos)")
            plt.ylabel("Número de Nascimentos")
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)
            plt.show()

        else:
            fig, ax1 = plt.subplots(figsize=(10, 5))
            dados_sem_frequencia = info1
            ax1.bar(dados_sem_frequencia.index, dados_sem_frequencia.values, color='steelblue')
            ax1.set_ylabel('Estatísticas')
            ax1.tick_params(axis='x', rotation=45)
            plt.title(f"{coluna}")
            plt.tight_layout()
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)
            plt.show()


        with open(caminho_txt, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"Nome da coluna: {coluna}\n{info1.to_string()}\n\n\n")

    dados()
    print(info1_str)
