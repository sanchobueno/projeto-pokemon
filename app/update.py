import os
import pandas as pd
from extract import executar_extracao
import psycopg2
from psycopg2.extras import execute_values

def carregar_csv(path):
    return pd.read_csv(path)

def atualizar_postgres():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "pokemon_db"),
        user=os.getenv("POSTGRES_USER", "pokemon_user"),
        password=os.getenv("POSTGRES_PASSWORD", "pokemon_pass")
    )
    cur = conn.cursor()

    # Limpa tabelas antes de inserir
    cur.execute("TRUNCATE TABLE ranking_pokemon CASCADE;")
    cur.execute("TRUNCATE TABLE info_pokemon CASCADE;")
    cur.execute("TRUNCATE TABLE pokemon_completo CASCADE;")

    # Carrega CSVs
    df_rank = carregar_csv("/app/ranking_pokemon.csv")
    df_info = carregar_csv("/app/info_pokemon.csv")
    df_full = carregar_csv("/app/pokemon_completo.csv")

    # Ranking
    execute_values(cur,
        """
        INSERT INTO ranking_pokemon (nome, posicao, data_referencia)
        VALUES %s
        """,
        df_rank.values.tolist()
    )

    # Info
    execute_values(cur,
        """
        INSERT INTO info_pokemon (nome, id_pokedex, tipos, habilidades, altura, peso, base_experience)
        VALUES %s
        """,
        df_info.values.tolist()
    )

    # Final
    execute_values(cur,
        """
        INSERT INTO pokemon_completo (nome, posicao, data_referencia, id_pokedex, tipos, habilidades, altura, peso, base_experience)
        VALUES %s
        """,
        df_full.values.tolist()
    )

    conn.commit()
    cur.close()
    conn.close()

    print("✨ Banco atualizado com sucesso!")


if __name__ == "__main__":
    print("🔄 Rodando atualização diária...")
    executar_extracao()
    atualizar_postgres()
    print("✔ Atualização concluída!")
