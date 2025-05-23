import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Substitui o nome das variáveis em vez de ser nomes em inglês, troca pelos em português, deixando na mesma variável
    info1 = info.rename(index=dicionario_projeto["pesquisa"])

    info1 = round(info1, 2)

    info1_str = info1.to_string()

    with open(caminho_txt, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome da coluna: {coluna}\n{info1_str}\n\n\n")

    def dados():
        if coluna == "IDADEMAE":
            tabela_copy = tabela_vivos2024.copy()
            tabela_copy["IDADEMAE"] = pd.to_numeric(tabela_copy["IDADEMAE"], errors="coerce")
            definido = tabela_copy.dropna(subset=["IDADEMAE"])
            bins = list(range(10, 65, 5))
            labels = [f"{i+1}-{i+5}" for i in bins[:-1]]
            definido["faixa_etaria"] = pd.cut(definido["IDADEMAE"], bins=bins, labels=labels, right=True)
            contagem = definido["faixa_etaria"].value_counts().sort_index()
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

        elif coluna == "IDADEPAI":
            tabela = tabela_vivos2024.copy()
            tabela["IDADEPAI"] = pd.to_numeric(tabela["IDADEPAI"], errors="coerce")
            tabela = tabela.dropna(subset=["IDADEPAI"])
            bins = list(range(10, 65, 5))
            labels = [f"{i+1}-{i+5}" for i in bins[:-1]]
            tabela["faixa_etaria"] = pd.cut(tabela["IDADEPAI"], bins=bins, labels=labels, right=True)
            contagem = tabela["faixa_etaria"].value_counts().sort_index()
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

        elif coluna == "PESO":
            tabela = tabela_vivos2024.copy()

            tabela["PESO"] = pd.to_numeric(tabela["PESO"], errors="coerce")
            tabela["PESO"].plot.hist(bins=50, color="salmon", edgecolor="black")
            plt.title("Distribuição do Peso ao Nascer")
            plt.xlabel("Peso (g)")
            plt.ylabel("Frequência")
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)

            plt.show()

        elif coluna == "PARTOSPRENATALCONSULT":
            tabela = tabela_vivos2024.copy()
            #CONVERTE AS TABELAS PARA VALORES NÚMERICOS
            tabela["QTDPARTNOR"] = pd.to_numeric(tabela["QTDPARTNOR"], errors="coerce")
            tabela["QTDPARTCES"] = pd.to_numeric(tabela["QTDPARTCES"], errors="coerce")
            tabela["CONSULTAS"] = pd.to_numeric(tabela["CONSULTAS"], errors="coerce")
            tabela = tabela[tabela["CONSULTAS"].isin([1, 2, 3, 4])]
            tabela["TOTAL_PARTOS"] = tabela["QTDPARTNOR"].fillna(0) + tabela["QTDPARTCES"].fillna(0)
            # Organizada por número de consultas e soma dos partos
            agrupado = tabela.groupby("CONSULTAS")["TOTAL_PARTOS"].sum()

            # Calcula percentual de cada categoria
            percentual = (agrupado / agrupado.sum()) * 100

            #Traduz o código, retira os números pelas as palavras vindas do dicionario do DF
            agrupado.index = agrupado.index.map(dicionario_projeto["consultas"])
            percentual.index = percentual.index.map(dicionario_projeto["consultas"])

            sns.set_style("whitegrid")

            # Plotagem
            plt.figure(figsize=(9, 6))
            bars = plt.bar(agrupado.index, agrupado.values, color="#6699CC", edgecolor="#336699")

            # Rótulos no topo das barras com valor absoluto e percentual
            for bar, val, perc in zip(bars, agrupado.values, percentual.values):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + max(agrupado.values) * 0.02,
                         f"{int(val):,}\n({perc:.1f}%)", ha='center', va='bottom',
                         fontsize=11, fontweight='semibold', color="#003366")

            plt.title("Total de Partos por Número de Consultas Pré-Natal", fontsize=16, weight='bold', color="#003366")
            plt.xlabel("Consultas Pré-Natal", fontsize=13)
            plt.ylabel("Número Total de Partos", fontsize=13)
            plt.ylim(0, max(agrupado.values) * 1.15)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)

            plt.show()

        elif coluna == "HORANASC":
            tabela = tabela_vivos2024.copy()
            tabela["HORANASC"] = pd.to_numeric(tabela["HORANASC"], errors="coerce")
            tabela["HORA"] = (tabela["HORANASC"] // 100).dropna().astype(int)

            tabela["HORA"].value_counts().sort_index().plot(kind="bar", color="mediumorchid")
            plt.title("Nascimentos por Hora do Dia")
            plt.xlabel("Hora")
            plt.ylabel("Número de Nascimentos")
            plt.savefig(f"{os.path.join(caminho_pasta_graficos,coluna)}_grafico.png", dpi=300)

            plt.show()

        elif coluna == "FILHOSMORTOSETARIAMÃE":
            tabela = tabela_vivos2024.copy()
            tabela = tabela.dropna(subset=['IDADEMAE', 'QTDFILMORT'])
            # Converte para numérico e filtra valores válidos
            tabela['IDADEMAE'] = pd.to_numeric(tabela['IDADEMAE'], errors='coerce')
            tabela['QTDFILMORT'] = pd.to_numeric(tabela['QTDFILMORT'], errors='coerce')
            # Define faixas etárias para a mãe
            bins = list(range(10, 70, 5))  # 10-14, 15-19, ..., 65-69
            labels = [f"{i + 1}-{i + 5}" for i in bins[:-1]]
            tabela['faixa_mae'] = pd.cut(tabela['IDADEMAE'], bins=bins, labels=labels, right=True)
            # Agrupa e soma filhos mortos por faixa
            filhos_mortos_faixa = tabela.groupby('faixa_mae')['QTDFILMORT'].sum()

            # Calcula percentual por faixa
            percentual = (filhos_mortos_faixa / filhos_mortos_faixa.sum()) * 100

            # Plot
            sns.set_style('whitegrid')
            plt.figure(figsize=(12, 6))
            bars = plt.bar(filhos_mortos_faixa.index.astype(str), filhos_mortos_faixa.values, color='salmon',
                           edgecolor='darkred')

            plt.title('Quantidade de Filhos Mortos por Faixa Etária da Mãe', fontsize=16, weight='bold')
            plt.xlabel('Faixa Etária da Mãe (anos)', fontsize=12)
            plt.ylabel('Quantidade de Filhos Mortos', fontsize=12)
            plt.xticks(rotation=45)
            plt.ylim(0, filhos_mortos_faixa.max() * 1.15)

            # Adiciona valores absolutos e percentuais nas barras
            for bar, val, perc in zip(bars, filhos_mortos_faixa.values, percentual.values):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + filhos_mortos_faixa.max() * 0.02,
                         f"{int(val)}\n({perc:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()
            plt.show()

        elif coluna == "PARTOS":
            tabela = tabela_vivos2024.copy()
            # Converte a coluna PARTO para numérico
            tabela["PARTO"] = pd.to_numeric(tabela["PARTO"], errors="coerce")

            # Filtra valores válidos (1 = vaginal, 2 = cesáreo)
            #pega as palavras do dicionario
            tabela = tabela[tabela["PARTO"].isin([1, 2])]
            tabela["TIPO_PARTO"] = tabela["PARTO"].map(dicionario_projeto["parto"])
            # Conta os partos e calcula percentual
            contagem = tabela["TIPO_PARTO"].value_counts().sort_index()
            percentual = contagem / contagem.sum() * 100

            # Plotagem
            sns.set_style("whitegrid")
            plt.figure(figsize=(8, 5))
            bars = plt.bar(percentual.index, percentual.values, color=["skyblue", "lightcoral"], edgecolor="black")

            plt.title("Percentual de Partos Vaginais e Cesáreos", fontsize=16, weight="bold")
            plt.ylabel("Percentual (%)")
            plt.ylim(0, percentual.max() * 1.2)

            # Adiciona valores percentuais no topo das barras
            for bar, perc in zip(bars, percentual.values):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f"{perc:.1f}%",
                         ha='center', va='bottom', fontsize=12, fontweight='bold')

            plt.tight_layout()
            plt.show()

        elif coluna == "TIPOSPARTOETARIAMAE":
            tabela = tabela_vivos2024.copy()

            # Converte idade para número (ignora valores inválidos)
            tabela['IDADEMAE'] = pd.to_numeric(tabela['IDADEMAE'], errors='coerce')

            # Cria faixas etárias
            bins = [0, 19, 29, 39, 120]
            labels = ['< 20 anos', '20-29 anos', '30-39 anos', '40+ anos']
            tabela['FAIXA_ETARIA'] = pd.cut(tabela['IDADEMAE'], bins=bins, labels=labels, right=True)

            #info1 = info.rename(index=dicionario_projeto["pesquisa"])
            tabela = tabela[dicionario_projeto["parto"]]

            # Remove partos ignorados, se desejar
            tabela = tabela[tabela['PARTO'] != 'Ignorado']

            contagem = tabela.groupby(['FAIXA_ETARIA', 'PARTO']).size().unstack().fillna(0)

            # Calcula proporções
            proporcao = contagem.div(contagem.sum(axis=1), axis=0) * 100

            # Plotando
            cores = {'Vaginal': 'mediumseagreen', 'Cesáreo': 'tomato'}
            proporcao.plot(kind='bar', stacked=True, color=cores, figsize=(10, 6))

            plt.title('Distribuição Percentual dos Tipos de Parto por Faixa Etária da Mãe', fontsize=14)
            plt.xlabel('Faixa Etária da Mãe')
            plt.ylabel('Proporção (%)')
            plt.legend(title='Tipo de Parto')
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()
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
