# dashboard.py
# Dashboard interativo para visualização dos dados IoT de temperatura

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Dashboard IoT - Temperaturas",
    page_icon="🌡️",
    layout="wide"
)

# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "iotdb"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ============================================================
# FUNÇÃO PARA CARREGAR DADOS DAS VIEWS
# ============================================================
@st.cache_data
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# ============================================================
# CABEÇALHO
# ============================================================
st.title("🌡️ Dashboard de Temperaturas IoT")
st.markdown("Monitoramento de leituras de sensores de temperatura em ambientes internos e externos.")
st.divider()

# ============================================================
# MÉTRICAS GERAIS
# ============================================================
st.subheader("📊 Visão Geral")

df_geral = pd.read_sql("SELECT COUNT(*) as total, ROUND(AVG(temp)::numeric,2) as media, MAX(temp) as maxima, MIN(temp) as minima FROM temperature_readings", engine)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Leituras", f"{df_geral['total'][0]:,}")
col2.metric("Temperatura Média", f"{df_geral['media'][0]} °C")
col3.metric("Temperatura Máxima", f"{df_geral['maxima'][0]} °C")
col4.metric("Temperatura Mínima", f"{df_geral['minima'][0]} °C")

st.divider()

# ============================================================
# GRÁFICO 1 — Média de temperatura por dispositivo
# ============================================================
st.subheader("📍 Média de Temperatura por Dispositivo")
st.caption("View: avg_temp_por_dispositivo — Mostra a temperatura média registrada por cada sensor/dispositivo.")

df_avg = load_data("avg_temp_por_dispositivo")

fig1 = px.bar(
    df_avg,
    x="device_id",
    y="avg_temp",
    color="avg_temp",
    color_continuous_scale="RdYlBu_r",
    labels={"device_id": "Dispositivo", "avg_temp": "Temperatura Média (°C)"},
    title="Temperatura Média por Dispositivo"
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ============================================================
# GRÁFICO 2 — Leituras por hora do dia
# ============================================================
st.subheader("🕐 Volume de Leituras por Hora do Dia")
st.caption("View: leituras_por_hora — Indica os horários com maior concentração de leituras dos sensores.")

df_hora = load_data("leituras_por_hora")
df_hora["hora"] = df_hora["hora"].astype(int)

fig2 = px.line(
    df_hora,
    x="hora",
    y="contagem",
    markers=True,
    labels={"hora": "Hora do Dia", "contagem": "Quantidade de Leituras"},
    title="Distribuição de Leituras ao Longo do Dia"
)
fig2.update_xaxes(dtick=1)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ============================================================
# GRÁFICO 3 — Temperaturas máximas e mínimas por dia
# ============================================================
st.subheader("📅 Temperaturas Máximas e Mínimas por Dia")
st.caption("View: temp_max_min_por_dia — Permite identificar variações extremas de temperatura ao longo do tempo.")

df_maxmin = load_data("temp_max_min_por_dia")
df_maxmin["data"] = pd.to_datetime(df_maxmin["data"])

fig3 = px.line(
    df_maxmin,
    x="data",
    y=["temp_max", "temp_min"],
    labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Tipo"},
    title="Variação Diária de Temperaturas Máximas e Mínimas",
    color_discrete_map={"temp_max": "red", "temp_min": "blue"}
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ============================================================
# RODAPÉ
# ============================================================
st.caption("Projeto acadêmico — Disruptive Architectures: IoT, Big Data e IA | UniFECAF")