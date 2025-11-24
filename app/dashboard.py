import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import altair as alt
import os

# ------------------------------
# FUNÇÃO PARA CONECTAR AO POSTGRES
# ------------------------------
def conectar_postgres():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "pokemon_db"),
        user=os.getenv("POSTGRES_USER", "pokemon_user"),
        password=os.getenv("POSTGRES_PASSWORD", "pokemon_pass"),
    )
    return conn


# ------------------------------
# CARREGAR TABELA DO BANCO
# ------------------------------
@st.cache_data(ttl=30, show_spinner=False)
def carregar_tabela():
    conn = conectar_postgres()
    query = "SELECT * FROM pokemon_completo;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ------------------------------
# DASHBOARD
# ------------------------------
st.title("📊 Dashboard Pokémon – Intermediário")
st.write("Este dashboard mostra estatísticas simples dos pokémons extraídos da BigQuery + PokeAPI.")

df = carregar_tabela()

st.subheader("📄 Tabela completa")
st.dataframe(df)

# ------------------------------
# FILTRO POR TIPO (CORRIGIDO)
# ------------------------------
def separar_tipos(valor):
    if pd.isna(valor):
        return []
    return [t.strip() for t in valor.split(",")]

# Extrair lista de todos os tipos
todos_tipos = sorted({
    t
    for lista in df["tipos"].dropna().apply(separar_tipos)
    for t in lista
})

tipo_escolhido = st.selectbox("Filtrar por tipo:", ["Todos"] + todos_tipos)

# Aplicar filtro
if tipo_escolhido != "Todos":
    df = df[df["tipos"].apply(lambda x: tipo_escolhido in separar_tipos(x))]

# ------------------------------
# GRÁFICO: Contagem por tipo
# ------------------------------
# === Gráfico: Quantidade de Pokémons por Tipo ===
st.subheader("Quantidade de Pokémons por Tipo")

# Limpeza e explosão dos múltiplos tipos
df_tipos = (
    df.assign(
        tipo=df["tipos"]
        .fillna("desconhecido")
        .apply(lambda x: [t.strip() for t in x.split(",")])
    )
    .explode("tipo")
)

grafico_tipos = (
    alt.Chart(df_tipos)
    .mark_bar()
    .encode(
        x=alt.X("tipo:N", sort="-y", title="Tipo"),
        y=alt.Y("count():Q", title="Quantidade"),
        tooltip=["tipo", "count()"],
    )
)

st.altair_chart(grafico_tipos, use_container_width=True)


# ------------------------------
# GRÁFICO: Altura x Peso
# ------------------------------
st.subheader("⚖️ Altura x Peso dos Pokémons")

scatter = (
    alt.Chart(df)
    .mark_circle(size=80)
    .encode(
        x="altura",
        y="peso",
        tooltip=["nome", "altura", "peso"]
    )
)

st.altair_chart(scatter, use_container_width=True)
