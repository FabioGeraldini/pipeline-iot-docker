# load_data.py
# Script para ler o CSV de leituras IoT e inserir no PostgreSQL

import pandas as pd
from sqlalchemy import create_engine

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
# LEITURA DO CSV
# ============================================================
print("Lendo o arquivo CSV...")
df = pd.read_csv("data/IOT-temp.csv")

print("Primeiras linhas do CSV:")
print(df.head())
print(f"\nTotal de registros: {len(df)}")
print(f"Colunas encontradas: {list(df.columns)}")

# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================
print("\nProcessando os dados...")

# Renomeia as colunas para o padrão da nossa tabela
df = df.rename(columns={
    "noted_date": "noted_date",
    "temp": "temp",
    "out/in": "out_in",
    "room_id/id": "device_id"
})

# Converte a coluna de data para o formato correto
df["noted_date"] = pd.to_datetime(df["noted_date"], dayfirst=True, errors="coerce")

# Remove linhas com data inválida ou temperatura nula
df = df.dropna(subset=["noted_date", "temp"])

# Seleciona apenas as colunas necessárias
df = df[["noted_date", "temp", "out_in", "device_id"]]

print(f"Registros válidos para inserção: {len(df)}")

# ============================================================
# INSERÇÃO NO BANCO DE DADOS
# ============================================================
print("\nInserindo dados no PostgreSQL...")

df.to_sql(
    name="temperature_readings",
    con=engine,
    if_exists="append",
    index=False
)

print("✅ Dados inseridos com sucesso!")