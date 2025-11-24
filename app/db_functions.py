import psycopg2
import pandas as pd

def conectar_postgres():
    try:
        conn = psycopg2.connect(
            dbname="pokemon_db",
            user="postgres",
            password="postgres",
            host="postgres",
            port=5432
        )
        print("🔌 Conectado ao PostgreSQL!")
        return conn
    except Exception as e:
        print("❌ Erro ao conectar ao PostgreSQL:", e)
        return None


def carregar_csv_para_postgres(csv_path, tabela):
    conn = conectar_postgres()
    if conn is None:
        return

    try:
        df = pd.read_csv(csv_path)
        cursor = conn.cursor()

        # Apaga os dados antigos
        cursor.execute(f"DELETE FROM {tabela};")

        # Insere linha por linha
        for _, linha in df.iterrows():
            cols = ",".join(df.columns)
            valores = "%s," * len(df.columns)
            valores = valores.rstrip(",")

            cursor.execute(
                f"INSERT INTO {tabela} ({cols}) VALUES ({valores});",
                tuple(linha)
            )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ CSV {csv_path} carregado na tabela {tabela}!")

    except Exception as e:
        print(f"❌ Erro ao carregar CSV na tabela {tabela}:", e)
