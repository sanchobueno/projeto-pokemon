import os
import pandas as pd

from bq_functions import extrair_tabela_bigquery
from poke_functions import coletar_pokemons_da_api


def executar_extracao():
    """
    Executa o pipeline completo:
    1. Extrai ranking do BigQuery.
    2. Salva CSV com ranking.
    3. Coleta dados da PokeAPI.
    4. Salva CSV com informações dos pokémons.
    5. Combina tudo e salva pokemon_completo.csv.
    """

    # Caminho da chave dentro do container (/app)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/chave_teste_dev.json"

    # Garantir que a pasta /app/data existe
    os.makedirs("data", exist_ok=True)

    print("=== ETAPA 1: Extraindo dados do BigQuery ===")

    tabela = "bravo-atlas.teste_dev_bravo.ranking_pokemon"
    df_ranking = extrair_tabela_bigquery(tabela)

    if df_ranking.empty:
        print("❌ Não foi possível extrair dados do BigQuery. Encerrando.")
        return

    df_ranking.to_csv("/app/ranking_pokemon.csv", index=False)
    print("✅ ranking_pokemon.csv salvo com sucesso!")

    print("\n=== ETAPA 2: Coletando informações da PokeAPI ===")
    nomes = df_ranking["nome"].unique().tolist()

    df_info = coletar_pokemons_da_api(nomes)
    df_info.to_csv("/app/info_pokemon.csv", index=False)
    print("✅ info_pokemon.csv salvo com sucesso!")

    print("\n=== ETAPA 3: Combinando dados ===")
    df_final = df_ranking.merge(df_info, on="nome", how="left")
    df_final.to_csv("/app/pokemon_completo.csv", index=False)
    print("✅ pokemon_completo.csv salvo com sucesso!")