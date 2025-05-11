import os
import pandas as pd

#lista os nomes das tabelas
#for coluna in tabela_vivos2024.columns:
    #print(coluna)


caminho_tabela_vivos2024 = r"dados/2024/dados-de-nascidos-vivos-2024-jun.csv"
tabela_vivos2024 = pd.read_csv(caminho_tabela_vivos2024, sep = ";")

nome_arquivo = os.path.basename(caminho_tabela_vivos2024).split(".")[0]
nome_arquivo = nome_arquivo + ".txt"

caminho_txts = os.path.join(r"\dados_filtrados", nome_arquivo)

if not os.path.exists(caminho_txts):
    os.mkdir(caminho_txts)

print(nome_arquivo)


dicionario = {
    "count": "Contagem",
    "mean": "Média",
     "std": "Desvio Padrão",
    "min": "Mínimo",
    "25%": "Primeiro Quartil",
    "50%": "Mediana",
    "75%": "Terceiro Quartil",
    "Max": "Máximo"
}

coluna = input("Nome das colunas: ").strip().upper()
info = (tabela_vivos2024[coluna].describe())

#Substituiu o nome das variaveis em vez de ser nomes ingles troca pelos em português, deixando na mesma variável
#index é o db, o dicionario que ele vai substituir
info1 = info.rename(index=dicionario)

with open(caminho_txts, "w", encoding="utf-8") as arquivo:
    arquivo.write(info1.to_string())

print(round(info1, 2))