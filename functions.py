from google.cloud import bigquery
import pandas as pd

def extrair_tabela_bigquery(table_id: str) -> pd.DataFrame:
    """
    Extrai uma tabela do Google BigQuery e retorna como DataFrame.
    table_id: nome completo da tabela (ex: 'bravoatlas.teste_dev_bravo.ranking_pokemon')
    """
    try:
        client = bigquery.Client()
        print(f"Conectando à tabela: {table_id}")
        df = client.list_rows(table_id).to_dataframe()
        print(f"✅ Dados extraídos com sucesso! {len(df)} registros encontrados.")
        return df
    except Exception as e:
        print("❌ Erro ao extrair tabela:", e)
        return pd.DataFrame()

import requests
import pandas as pd
from time import sleep

def buscar_info_pokemon(nome):
    """
    Busca informações detalhadas de um Pokémon na PokeAPI.
    Retorna um dicionário com id, tipos, habilidades, altura, peso, base_experience e geração.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        tipos = [t['type']['name'] for t in data['types']]
        habilidades = [h['ability']['name'] for h in data['abilities']]

        info = {
            "nome": nome,
            "id_pokedex": data["id"],
            "tipos": ", ".join(tipos),
            "habilidades": ", ".join(habilidades),
            "altura": data["height"],
            "peso": data["weight"],
            "base_experience": data["base_experience"]
        }

        return info

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao buscar {nome}: {e}")
        return None


def coletar_pokemons_da_api(lista_nomes):
    """
    Recebe uma lista de nomes de Pokémon, busca na API e retorna um DataFrame.
    """
    dados = []
    for nome in lista_nomes:
        print(f"🔍 Buscando dados de {nome}...")
        info = buscar_info_pokemon(nome)
        if info:
            dados.append(info)
        sleep(0.5)  # pausa pequena para não sobrecarregar a API
    return pd.DataFrame(dados)
