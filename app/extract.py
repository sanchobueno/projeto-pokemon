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
        print("❌ Não foi possível extrair dados do BigQuery. Encerrando o script.")
        return

    df_ranking.to_csv("data/ranking_pokemon.csv", index=False)
    print("✅ ranking_pokemon.csv salvo em /app/data")

    print("\n=== ETAPA 2: Coletando informações da PokeAPI ===")
    nomes_pokemons = df_ranking["nome"].unique().tolist()

    df_info = coletar_pokemons_da_api(nomes_pokemons)
    df_info.to_csv("data/info_pokemon.csv", index=False)
    print("✅ info_pokemon.csv salvo em /app/data")

    print("\n=== ETAPA 3: Combinando dados ===")
    df_final = pd.merge(df_ranking, df_info, on="nome", how="left")
    df_final.to_csv("data/pokemon_completo.csv", index=False)

    print("🎉 Processo concluído com sucesso!")
    print("📁 Arquivo final salvo: /app/data/pokemon_completo.csv")
