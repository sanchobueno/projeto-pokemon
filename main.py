#importa tabela bravos do bigquery e salva em csv

import os
from functions import extrair_tabela_bigquery

# Caminho absoluto do arquivo da chave
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\lucas\OneDrive\Documentos\programação\projeto teste\chave_teste_dev.json"

def main():
    tabela = "bravo-atlas.teste_dev_bravo.ranking_pokemon"
    df = extrair_tabela_bigquery(tabela)

    if not df.empty:
        df.to_csv("ranking_pokemon.csv", index=False)
        print("✅ Arquivo salvo como ranking_pokemon.csv")

if __name__ == "__main__":
    main()

#puxa dados da pokeapi e compara com bravos

import os
import pandas as pd
from functions import extrair_tabela_bigquery, coletar_pokemons_da_api

# Configuração da chave do Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\lucas\OneDrive\Documentos\programação\projeto teste\chave_teste_dev.json"

def main():
    # === ETAPA 1: BigQuery ===
    tabela = "bravo-atlas.teste_dev_bravo.ranking_pokemon"
    df_ranking = extrair_tabela_bigquery(tabela)
    if not df_ranking.empty:
        df_ranking.to_csv("ranking_pokemon.csv", index=False)
        print("✅ Arquivo salvo como ranking_pokemon.csv")

    # === ETAPA 2: PokeAPI ===
    print("\n=== ETAPA 2: Coletando informações da PokeAPI ===")
    nomes_pokemons = df_ranking["nome"].unique().tolist()  # substitua 'pokemon' pelo nome real da coluna se for diferente
    df_info = coletar_pokemons_da_api(nomes_pokemons)
    df_info.to_csv("info_pokemon.csv", index=False)
    print("✅ Informações salvas como info_pokemon.csv")

if __name__ == "__main__":
    main()
