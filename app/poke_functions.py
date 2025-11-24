import pandas as pd
import requests
from time import sleep

def buscar_info_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        tipos = [t['type']['name'] for t in data['types']]
        habilidades = [h['ability']['name'] for h in data['abilities']]

        return {
            "nome": nome,
            "id_pokedex": data["id"],
            "tipos": ", ".join(tipos),
            "habilidades": ", ".join(habilidades),
            "altura": data.get("height"),
            "peso": data.get("weight"),
            "base_experience": data.get("base_experience"),
        }

    except Exception as e:
        print(f"⚠️ Erro ao buscar {nome}: {e}")
        return None


def coletar_pokemons_da_api(lista_nomes):
    dados = []
    for nome in lista_nomes:
        print(f"🔍 Buscando dados de {nome}...")
        info = buscar_info_pokemon(nome)
        if info:
            dados.append(info)
        sleep(0.5)
    return pd.DataFrame(dados)
