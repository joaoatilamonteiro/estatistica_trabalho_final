import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re  # Para extrair o ano do nome do arquivo

# Dicionário do projeto (mantido como no original)
dicionario_projeto = {
    "pesquisa": {
        "count": "Contagem", "mean": "Média", "std": "Desvio Padrão", "min": "Mínimo",
        "25%": "Primeiro Quartil", "50%": "Mediana", "75%": "Terceiro Quartil", "max": "Máximo",  # 'Max' para 'max'
        "unique": "Valores Únicos", "top": "Mais Frequente", "freq": "Frequência do Mais Frequente"
    },
    "locnasc": {9: "Ignorado", 1: "Hospital", 2: "Outro Estab Saúde", 3: "Domicílio", 4: "Outros"},
    "estcivmae": {1: "Solteira", 2: "Casada", 3: "Viúva", 4: "Separado judicialmente/Divorciado", 9: "Ignorado"},
    "escmae": {1: "Nenhuma", 2: "1 a 3 anos", 3: "4 a 7 anos", 4: "8 a 11 anos", 5: "12 e mais", 9: "Ignorado"},
    "gestacao": {9: "Ignorado", 1: "Menos de 22 semanas", 2: "22 a 27 semanas", 3: "28 a 31 semanas",
                 4: "32 a 36 semanas", 5: "37 a 41 semanas", 6: "42 semanas e mais"},
    "gravidez": {9: "Ignorado", 1: "Única", 2: "Dupla", 3: "Tripla e mais"},
    "parto": {9: "Ignorado", 1: "Vaginal", 2: "Cesáreo"},
    "consultas": {1: "Nenhuma", 2: "de 1 a 3", 3: "de 4 a 6", 4: "7 e mais", 9: "Ignorado"},
    "sexo": {0: "Ignorado", 1: "Masculino", 2: "Feminino"},
    "racacor": {1: "Branca", 2: "Preta", 3: "Amarela", 4: "Parda", 5: "Indígena"},
    "idanomal": {9: "Ignorado", 1: "Sim", 2: "Não"}
}

# Caminhos para pastas de saída
caminho_pasta_txts = r"dados_filtrados/dados_especificos/notacoes_txt_comparativo/"
caminho_pasta_graficos = r"dados_filtrados/dados_especificos/graficos_comparativo/"

# Cria as pastas de saída se não existirem
if not os.path.exists(caminho_pasta_txts):
    os.makedirs(caminho_pasta_txts)
if not os.path.exists(caminho_pasta_graficos):
    os.makedirs(caminho_pasta_graficos)


def extrair_ano_do_caminho(caminho_arquivo):
    """Extrai o ano de uma string de caminho de arquivo (ex: r'\dados\2020\arquivo.csv')"""
    match = re.search(r'(\d{4})', caminho_arquivo)
    if match:
        return int(match.group(1))
    return None


def carregar_dados_anuais(lista_arquivos_csv):
    """
    Carrega dados de múltiplos arquivos CSV, adiciona uma coluna 'ANO'
    e concatena os DataFrames.
    """
    lista_dfs = []
    for caminho_csv in lista_arquivos_csv:
        try:
            ano = extrair_ano_do_caminho(caminho_csv)
            if ano is None:
                print(f"Não foi possível extrair o ano do caminho: {caminho_csv}. Pulando arquivo.")
                continue

            # Tenta detectar o separador, comum ser ';' ou ','
            try:
                df_temp = pd.read_csv(caminho_csv, sep=";", low_memory=False)
            except pd.errors.ParserError:
                df_temp = pd.read_csv(caminho_csv, sep=",", low_memory=False)
            except Exception as e:  # Captura outros erros de leitura
                print(f"Erro ao ler o arquivo {caminho_csv} com separador ';': {e}")
                try:
                    df_temp = pd.read_csv(caminho_csv, sep=",", low_memory=False)
                    print(f"Arquivo {caminho_csv} lido com sucesso usando separador ','.")
                except Exception as e_comma:
                    print(f"Erro ao ler o arquivo {caminho_csv} com separador ',': {e_comma}. Pulando arquivo.")
                    continue

            df_temp['ANO'] = ano
            lista_dfs.append(df_temp)
            print(f"Arquivo {caminho_csv} (Ano: {ano}) carregado")
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminho_csv}. Pulando.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo {caminho_csv}: {e}. Pulando.")

    if not lista_dfs:
        print("Nenhum DataFrame foi carregado. Verifique os caminhos e os arquivos.")
        return pd.DataFrame()

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    print(f"DataFrame consolidado criado. Shape total: {df_consolidado.shape}")
    print(f"Anos presentes no DataFrame consolidado: {sorted(df_consolidado['ANO'].unique())}")
    return df_consolidado


def mapear_colunas(df, dicionario_map):
    """
    Itera sobre o dicionário de mapeamento e cria novas colunas descritivas no DataFrame.
    Ex: Cria 'LOCNASC_DESC' a partir da coluna 'LOCNASC'.
    """
    print("\nIniciando mapeamento de colunas para descrições textuais...")
    df_mapeado = df.copy()

    # Itera sobre as chaves do dicionário (locnasc, estcivmae, etc.), ignorando 'pesquisa'
    for chave_map in dicionario_map:
        if chave_map == "pesquisa":
            continue

        coluna_original = chave_map.upper()  # Nomes de colunas agora são maiúsculos
        coluna_desc = f"{coluna_original}_DESC"

        if coluna_original in df_mapeado.columns:
            # Converte a coluna original para numérico, tratando erros
            coluna_numerica = pd.to_numeric(df_mapeado[coluna_original], errors='coerce')

            # Aplica o mapeamento usando o dicionário específico
            df_mapeado[coluna_desc] = coluna_numerica.map(dicionario_map[chave_map])

            # Preenche valores que não foram mapeados (NaN) com um texto padrão
            df_mapeado[coluna_desc].fillna('Não Especificado', inplace=True)
            print(f"Coluna '{coluna_desc}' criada a partir de '{coluna_original}'.")
        # else:
        # print(f"Aviso: Coluna '{coluna_original}' para mapeamento não encontrada no DataFrame.")

    return df_mapeado

def analisar_estatisticas_coluna_comparativo(df_consolidado, coluna_base, dicionario_map, pasta_txt, nome_analise):
    """
    Salva estatísticas em TXT. Agora, se uma coluna descritiva existir,
    dará prioridade a ela para estatísticas de contagem.
    """
    if 'ANO' not in df_consolidado.columns:
        print("Erro: Coluna 'ANO' não encontrada.")
        return

    coluna_desc = f"{coluna_base}_DESC"
    coluna_existe_desc = coluna_desc in df_consolidado.columns

    caminho_txt_final = os.path.join(pasta_txt, f"{nome_analise}_{coluna_base}_estatisticas_anuais.txt")

    with open(caminho_txt_final, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Análise Estatística Comparativa Anual da Coluna: {coluna_base}\n")

        anos_presentes = sorted(df_consolidado['ANO'].unique())

        for ano in anos_presentes:
            df_ano = df_consolidado[df_consolidado['ANO'] == ano]
            arquivo.write(f"\n--- Ano: {ano} ---\n")

            if coluna_existe_desc:
                arquivo.write("\nEstatísticas das Descrições (Textos):\n")
                info_desc = df_ano[coluna_desc].describe()  # Describe para dados categóricos
                arquivo.write(f"{info_desc.rename(index=dicionario_map['pesquisa']).to_string()}\n\n")
                arquivo.write("Contagem por Categoria:\n")
                arquivo.write(df_ano[coluna_desc].value_counts().to_string())

            else:  # Se não há coluna descritiva, faz como antes
                arquivo.write("\nEstatísticas dos Códigos Numéricos:\n")
                info_num = pd.to_numeric(df_ano[coluna_base], errors='coerce').describe()
                arquivo.write(f"{round(info_num.rename(index=dicionario_map['pesquisa']), 2).to_string()}")

            arquivo.write("\n")

#analisar_estatisticas_coluna_comparativo
def aecc (df_consolidado, coluna_selecionada, dicionario_map, pasta_txt,
                                             nome_analise):
    """
    Calcula estatísticas descritivas para uma coluna, comparando por ano, e salva em TXT.
    """
    if 'ANO' not in df_consolidado.columns:
        print("Erro: Coluna 'ANO' não encontrada no DataFrame consolidado.")
        return

    # Garante que a coluna selecionada exista no DataFrame
    if coluna_selecionada not in df_consolidado.columns:
        print(f"Coluna '{coluna_selecionada}' não encontrada no DataFrame. Verifique o nome da coluna.")
        return

    caminho_txt_final = os.path.join(pasta_txt, f"{nome_analise}_{coluna_selecionada}_estatisticas_anuais.txt")

    with open(caminho_txt_final, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Análise Estatística Comparativa Anual da Coluna: {coluna_selecionada}\n")

        anos_presentes = sorted(df_consolidado['ANO'].unique())

        for ano in anos_presentes:
            df_ano_especifico = df_consolidado[
                df_consolidado['ANO'] == ano].copy()  # Usar .copy() para evitar SettingWithCopyWarning

            arquivo.write(f"\n--- Ano: {ano} ---\n")

            if coluna_selecionada not in df_ano_especifico.columns:
                arquivo.write(f"Coluna '{coluna_selecionada}' não encontrada para este ano.\n")
                continue

            # Converte para numérico se possível, para estatísticas como média, std, etc.
            # Algumas colunas podem já ser numéricas ou podem ser códigos que não devem ser tratados como números (ex: ID).
            # Para colunas que são códigos e têm mapeamento no dicionário, usamos o describe() em cima dos valores mapeados ou dos códigos originais.

            coluna_data = df_ano_especifico[coluna_selecionada]

            # Tenta converter para numérico para describe() completo
            # Se falhar, usa o describe() para objetos/categorias
            try:
                # Tenta converter para numérico, substituindo não conversíveis por NaN
                coluna_numerica = pd.to_numeric(coluna_data, errors='coerce')

                # Verifica se a conversão resultou em todos NaN (significa que não era numérica)
                if not coluna_numerica.isnull().all():
                    info = coluna_numerica.describe()
                    moda_valores = coluna_numerica.mode()
                    info.loc["Moda"] = moda_valores.iloc[0] if not moda_valores.empty else 'N/A'
                else:  # Se todos foram NaN, trata como categórica
                    info = coluna_data.describe()  # Para colunas não-numéricas (object, category)
                    moda_valores = coluna_data.mode()
                    info.loc["Moda"] = moda_valores.iloc[0] if not moda_valores.empty else 'N/A'

            except Exception:  # Se qualquer outra coisa der errado
                info = coluna_data.describe()  # Fallback para describe de objeto
                moda_valores = coluna_data.mode()
                info.loc["Moda"] = moda_valores.iloc[0] if not moda_valores.empty else 'N/A'

            # Renomeia os índices das estatísticas usando o dicionário_projeto["pesquisa"]
            info_renomeada = info.rename(index=dicionario_map["pesquisa"])

            # Tenta arredondar, tratando exceções se houver dados não numéricos no resultado do describe
            try:
                info_renomeada = round(info_renomeada, 2)
            except TypeError:
                # Se houver tipos mistos que não podem ser arredondados (ex: strings em 'top'), ignora o arredondamento para essa linha
                pass

            arquivo.write(f"{info_renomeada.to_string()}\n")

        arquivo.write("\n\n")
    print(f"Análise estatística comparativa para '{coluna_selecionada}' salva em: {caminho_txt_final}")


#Funções de Plotagem Comparativa (Exemplos Adaptados)

def plot_comparativo_idademae(df, pasta_graficos, nome_analise):
    df_plot = df.copy()
    df_plot["IDADEMAE"] = pd.to_numeric(df_plot["IDADEMAE"], errors="coerce")
    df_plot.dropna(subset=["IDADEMAE", "ANO"], inplace=True)

    if df_plot.empty:
        print(f"Não há dados válidos para '{nome_analise}' após limpeza.")
        return

    bins = list(range(10, 65, 5))  # Faixas de 10-14, 15-19, ..., 60-64
    labels = [f"{i}-{i + 4}" for i in bins[:-1]]  # Ajuste para rótulos corretos
    df_plot["faixa_etaria_mae"] = pd.cut(df_plot["IDADEMAE"], bins=bins, labels=labels, right=False,
                                         include_lowest=True)

    contagem_anual = df_plot.groupby(['ANO', 'faixa_etaria_mae'], observed=False).size().reset_index(
        name='Numero de Nascimentos')

    if contagem_anual.empty:
        print(f"Não há dados para agrupar em '{nome_analise}'.")
        return

    plt.figure(figsize=(14, 8))
    sns.barplot(data=contagem_anual, x="faixa_etaria_mae", y="Numero de Nascimentos", hue="ANO", palette="viridis")
    plt.title("Número de Mães por Faixa Etária (Comparativo Anual)", fontsize=16)
    plt.xlabel("Faixa Etária da Mãe (anos)", fontsize=12)
    plt.ylabel("Número de Nascimentos", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Ano', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, f"{nome_analise}_comparativo_anual_grafico.png"), dpi=300)
    plt.show()
    print(f"Gráfico '{nome_analise}' salvo.")


def plot_comparativo_pesonasc(df, pasta_graficos, nome_analise):
    df_plot = df.copy()
    df_plot["PESO"] = pd.to_numeric(df_plot["PESO"], errors="coerce")
    df_plot.dropna(subset=["PESO", "ANO"], inplace=True)

    if df_plot.empty:
        print(f"Não há dados válidos para '{nome_analise}' após limpeza.")
        return

    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df_plot, x='ANO', y='PESO', palette="pastel")
    # Ou para histogramas sobrepostos:
    # for ano_val in sorted(df_plot['ANO'].unique()):
    #     sns.histplot(df_plot[df_plot['ANO'] == ano_val]['PESO'], label=str(ano_val), kde=True, alpha=0.5, bins=30)
    # plt.legend(title="Ano")

    plt.title("Distribuição Comparativa do Peso ao Nascer por Ano", fontsize=16)
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Peso (g)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, f"{nome_analise}_comparativo_anual_grafico.png"), dpi=300)
    plt.show()
    print(f"Gráfico '{nome_analise}' salvo.")


def plot_comparativo_partos_tipos(df, pasta_graficos, dicionario_map, nome_analise):
    df_plot = df.copy()
    df_plot["PARTO"] = pd.to_numeric(df_plot["PARTO"], errors="coerce")
    # Filtra apenas partos válidos (1 e 2) e remove NaNs em PARTO ou ANO
    df_plot = df_plot[df_plot["PARTO"].isin([1, 2])]
    df_plot.dropna(subset=["PARTO", "ANO"], inplace=True)

    if df_plot.empty:
        print(f"Não há dados válidos para '{nome_analise}' após limpeza.")
        return

    df_plot["TIPO_PARTO_DESC"] = df_plot["PARTO"].map(dicionario_map["parto"])

    # Contagem de tipos de parto por ano
    contagem_partos = df_plot.groupby(['ANO', 'TIPO_PARTO_DESC'], observed=False).size().reset_index(name='Quantidade')

    if contagem_partos.empty:
        print(f"Não há dados para agrupar em '{nome_analise}'.")
        return

    # Para calcular o percentual por ano
    total_por_ano = contagem_partos.groupby('ANO')['Quantidade'].sum().reset_index(name='TotalAnual')
    contagem_partos = pd.merge(contagem_partos, total_por_ano, on='ANO')
    contagem_partos['Percentual'] = (contagem_partos['Quantidade'] / contagem_partos['TotalAnual']) * 100

    plt.figure(figsize=(12, 7))
    sns.barplot(data=contagem_partos, x="ANO", y="Percentual", hue="TIPO_PARTO_DESC",
                palette={"Vaginal": "skyblue", "Cesáreo": "lightcoral"})

    plt.title("Percentual de Tipos de Parto por Ano", fontsize=16)
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Percentual (%)", fontsize=12)
    plt.legend(title="Tipo de Parto", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylim(0, 100)  # Percentual vai de 0 a 100
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, f"{nome_analise}_percentual_comparativo_anual_grafico.png"), dpi=300)
    plt.show()
    print(f"Gráfico '{nome_analise}' salvo.")


def plot_comparativo_tipos_parto_etaria_mae(df, pasta_graficos, dicionario_map, nome_analise):
    df_plot = df.copy()
    df_plot['IDADEMAE'] = pd.to_numeric(df_plot['IDADEMAE'], errors='coerce')
    df_plot['PARTO'] = pd.to_numeric(df_plot['PARTO'], errors='coerce')
    df_plot.dropna(subset=['IDADEMAE', 'PARTO', 'ANO'], inplace=True)
    df_plot = df_plot[df_plot['PARTO'].isin([1, 2])]  # Apenas partos vaginais e cesáreos

    if df_plot.empty:
        print(f"Não há dados válidos para '{nome_analise}' após limpeza.")
        return

    bins_idade = [0, 19, 29, 39, 120]  # Menor que 20, 20-29, 30-39, 40+
    labels_idade = ['<20', '20-29', '30-39', '40+']
    df_plot['FAIXA_ETARIA_MAE'] = pd.cut(df_plot['IDADEMAE'], bins=bins_idade, labels=labels_idade, right=True,
                                         include_lowest=True)
    df_plot['TIPO_PARTO_DESC'] = df_plot['PARTO'].map(dicionario_map["parto"])

    # Agrupa por ANO, FAIXA_ETARIA_MAE e TIPO_PARTO_DESC
    contagem = df_plot.groupby(['ANO', 'FAIXA_ETARIA_MAE', 'TIPO_PARTO_DESC'], observed=False).size().unstack(
        fill_value=0)

    if contagem.empty:
        print(f"Não há dados para agrupar em '{nome_analise}'.")
        return

    # Calcula a proporção para cada ANO e FAIXA_ETARIA_MAE
    proporcao = contagem.apply(lambda x: (x / x.sum()) * 100, axis=1).reset_index()

    # Para plotar com FacetGrid (um gráfico por ano)
    g = sns.catplot(
        data=proporcao.melt(id_vars=['ANO', 'FAIXA_ETARIA_MAE'], value_name='Proporção', var_name='TIPO_PARTO_DESC'),
        x='FAIXA_ETARIA_MAE',
        y='Proporção',
        hue='TIPO_PARTO_DESC',
        col='ANO',  # Cria uma coluna de gráficos para cada ano
        kind='bar',
        palette={"Vaginal": "mediumseagreen", "Cesáreo": "tomato"},
        height=5,
        aspect=1.2
    )

    g.set_axis_labels("Faixa Etária da Mãe", "Proporção (%)")
    g.set_titles("Ano: {col_name}")
    g.fig.suptitle('Distribuição % dos Tipos de Parto por Faixa Etária da Mãe e Ano', fontsize=16, y=1.03)
    g.add_legend(title='Tipo de Parto')

    # Adicionar rótulos de porcentagem nas barras
    for ax in g.axes.flat:
        for c in ax.containers:
            labels = [f'{w:.1f}%' if (w := v.get_height()) > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', fontsize=8, color='white', fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Ajusta para o suptitle
    plt.savefig(os.path.join(pasta_graficos, f"{nome_analise}_comparativo_anual_stacked_grafico.png"), dpi=300)
    plt.show()
    print(f"Gráfico '{nome_analise}' salvo.")


# --- Função Principal ---
def main():
    # Cria as pastas de saída se não existirem
    os.makedirs(caminho_pasta_txts, exist_ok=True)
    os.makedirs(caminho_pasta_graficos, exist_ok=True)

    lista_arquivos = [
        r"dados/2020/dados-de-nascidos-vivos.csv",
        r"dados/2021/dados-de-nascidos-vivos-2021.csv",
        r"dados/2022/dados-de-nascidos-vivos-2022.csv",
        r"dados/2023/dados-de-nascidos-vivos-2023.csv"
    ]

    df_bruto = carregar_dados_anuais(lista_arquivos)

    if df_bruto.empty:
        print("Nenhum dado foi carregado. Encerrando o programa.")
        return

    ### MUDANÇA 3: Chamando a nova função de mapeamento centralizado ###
    df_consolidado = mapear_colunas(df_bruto, dicionario_projeto)

    # Exibe as colunas criadas para verificação
    print("\nColunas no DataFrame final:", df_consolidado.columns.tolist())

    while True:
        print("\n--- Análises Comparativas Anuais Disponíveis ---")
        print("- IDADEMAE, PESO, PARTOS, TIPOSPARTOETARIAMAE")
        print("\nDigite o NOME DE UMA COLUNA (ex: LOCNASC, CONSULTAS, ESCMAE) para análise.")
        coluna_input = input("Digite a análise ou coluna (ou 'PARAR' para sair): ").strip().upper()

        if coluna_input == "PARAR":
            print("--------------------BUSCA ENCERRADA--------------------")
            break

        # --- Lógica de Análise Refatorada ---
        if coluna_input == "IDADEMAE":
            plot_comparativo_idademae(df_consolidado, caminho_pasta_graficos, "IDADEMAE")
            analisar_estatisticas_coluna_comparativo(df_consolidado, "IDADEMAE", dicionario_projeto, caminho_pasta_txts,
                                                     "IDADEMAE")

        elif coluna_input == "PESONASC":  # Assumindo que o nome da coluna no CSV é PESO
            plot_comparativo_pesonasc(df_consolidado, caminho_pasta_graficos, "PESO")
            analisar_estatisticas_coluna_comparativo(df_consolidado, "PESO", dicionario_projeto, caminho_pasta_txts,
                                                     "PESO")

        elif coluna_input == "PARTOS":
            plot_comparativo_partos_tipos(df_consolidado, caminho_pasta_graficos, dicionario_projeto, "PARTOS")
            analisar_estatisticas_coluna_comparativo(df_consolidado, "PARTO", dicionario_projeto, caminho_pasta_txts,
                                                     "PARTOS")

        elif coluna_input == "TIPOSPARTOETARIAMAE":
            plot_comparativo_tipos_parto_etaria_mae(df_consolidado, caminho_pasta_graficos, dicionario_projeto,
                                                    "TIPOSPARTOETARIAMAE")
            print(
                "Gráfico para 'TIPOSPARTOETARIAMAE' gerado. Análise estatística via TXT não é diretamente aplicável para esta combinação.")

        ### MUDANÇA 4: Lógica de análise genérica agora é muito mais inteligente ###
        elif coluna_input in df_consolidado.columns:
            print(f"Analisando a coluna '{coluna_input}'...")

            # 1. Gerar o arquivo de estatísticas
            analisar_estatisticas_coluna_comparativo(df_consolidado, coluna_input, dicionario_projeto,
                                                     caminho_pasta_txts, "COLUNA_DIRETA")

            # 2. Gerar o gráfico
            coluna_para_grafico = coluna_input
            coluna_desc = f"{coluna_input}_DESC"
            if coluna_desc in df_consolidado.columns:
                print(f"Coluna descritiva '{coluna_desc}' encontrada. O gráfico usará as descrições.")
                coluna_para_grafico = coluna_desc

            try:
                plt.figure(figsize=(14, 8))

                # Gráfico de contagem (countplot) é ideal para colunas categóricas ou com códigos
                # Pega as top 10 categorias para evitar poluição visual
                top_n = 10
                categorias_frequentes = df_consolidado[coluna_para_grafico].value_counts().nlargest(top_n).index

                sns.countplot(
                    data=df_consolidado[df_consolidado[coluna_para_grafico].isin(categorias_frequentes)],
                    y=coluna_para_grafico,  # Eixo Y para melhor leitura de rótulos longos
                    hue='ANO',
                    palette="viridis",
                    order=categorias_frequentes
                )

                plt.title(f"Contagem de '{coluna_para_grafico}' por Ano (Top {top_n})", fontsize=16)
                plt.xlabel("Contagem de Nascimentos", fontsize=12)
                plt.ylabel("")  # O nome da coluna já está nos rótulos do eixo Y
                plt.legend(title="Ano")
                plt.tight_layout()
                plt.savefig(os.path.join(caminho_pasta_graficos, f"COLUNA_DIRETA_{coluna_input}_grafico.png"), dpi=300)
                plt.show()
                print(f"Gráfico para '{coluna_input}' salvo.")

            except Exception as e:
                print(f"Não foi possível gerar um gráfico para a coluna '{coluna_input}': {e}")
        else:
            print(f"'{coluna_input}' não é uma análise pré-definida nem uma coluna válida. Tente novamente.")


if __name__ == "__main__":
    # Configurações de plotagem (opcional, mas melhora a aparência)
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)  # Tamanho padrão das figuras
    plt.rcParams['font.size'] = 10  # Tamanho padrão da fonte

    main()
