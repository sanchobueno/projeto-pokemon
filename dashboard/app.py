import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import altair as alt

# ---------------------------
# Conexão com PostgreSQL
# ---------------------------
def conectar():
    return psycopg2.connect(
        host="postgres",
        database="pokemon_db",
        user="pokemon_user",
        password="pokemon_pass"
    )

@st.cache_data
def carregar_dados():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM pokemon_completo", conn)
    conn.close()
    return df

# ---------------------------
# Interface do Dashboard
# ---------------------------
st.title("Pokémon Dashboard 🐱‍👤")

df = carregar_dados()

st.subheader("📊 Visão geral")
col1, col2, col3 = st.columns(3)

col1.metric("Pokémons únicos", df["nome"].nunique())
col2.metric("Tipos diferentes", df["tipos"].nunique())
col3.metric("Média XP Base", round(df["base_experience"].mean(), 2))

# ---------------------------
# Filtro por tipo
# ---------------------------
st.subheader("🔎 Filtro por tipo")

todos_tipos = sorted({t.strip() for lista in df["tipos"].dropna() for t in lista.split(",")})
tipo_select = st.selectbox("Selecione um tipo", ["Todos"] + todos_tipos)

if tipo_select != "Todos":
    df_filtrado = df[df["tipos"].str.contains(tipo_select, na=False)]
else:
    df_filtrado = df

st.dataframe(df_filtrado)

# ---------------------------
# Gráfico Peso x Altura
# ---------------------------
st.subheader("📈 Altura x Peso")

grafico = alt.Chart(df_filtrado).mark_circle(size=80).encode(
    x="altura:Q",
    y="peso:Q",
    tooltip=["nome", "altura", "peso", "tipos"]
)

st.altair_chart(grafico, use_container_width=True)
