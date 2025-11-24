from google.cloud import bigquery
import pandas as pd

def extrair_tabela_bigquery(table_id: str) -> pd.DataFrame:
    try:
        client = bigquery.Client()
        print(f"Conectando à tabela: {table_id}")
        df = client.list_rows(table_id).to_dataframe()
        print(f"✅ Dados extraídos com sucesso! {len(df)} registros encontrados.")
        return df
    except Exception as e:
        print("❌ Erro ao extrair tabela:", e)
        return pd.DataFrame()
