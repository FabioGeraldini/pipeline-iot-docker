# 🌡️ Pipeline de Dados com IoT e Docker

Projeto acadêmico da disciplina **Disruptive Architectures: IoT, Big Data e IA** — UniFECAF.

Pipeline completo de dados que processa leituras de temperatura de dispositivos IoT, armazena em PostgreSQL via Docker e visualiza em um dashboard interativo com Streamlit.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| Python 3.10+ | Linguagem principal |
| Docker | Containerização do banco de dados |
| PostgreSQL | Armazenamento dos dados |
| pandas | Leitura e tratamento do CSV |
| SQLAlchemy | Conexão Python ↔ PostgreSQL |
| Streamlit | Dashboard interativo web |
| Plotly | Gráficos interativos |

---

## 📁 Estrutura do Projeto

```
pipeline-iot-docker/
├── src/
│   ├── load_data.py       # Script de ingestão dos dados
│   └── dashboard.py       # Dashboard Streamlit
├── data/
│   └── IOT-temp.csv       # Dataset (baixar do Kaggle)
├── docs/
│   └── documentacao.pdf   # Documentação teórica
├── docker-compose.yml     # Configuração Docker
└── README.md
```

---

## ⚙️ Como Executar

### 1. Pré-requisitos
- [Python 3.10+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### 2. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/pipeline-iot-docker.git
cd pipeline-iot-docker
```

### 3. Baixe o dataset
Acesse o [Kaggle - Temperature Readings IoT Devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices), faça o download e coloque o arquivo `IOT-temp.csv` dentro da pasta `/data`.

### 4. Crie o ambiente virtual e instale as dependências
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install pandas psycopg2-binary sqlalchemy streamlit plotly
```

### 5. Suba o container PostgreSQL
```bash
docker-compose up -d
```
> ⚠️ Se a porta 5432 já estiver em uso, altere para 5433 no `docker-compose.yml` e nos arquivos `.py`.

### 6. Execute o script de ingestão
```bash
python src/load_data.py
```
Saída esperada:
```
✅ Dados inseridos com sucesso! (97.606 registros)
```

### 7. Execute o dashboard
```bash
streamlit run src/dashboard.py
```
Acesse em: [http://localhost:8501](http://localhost:8501)

---

## 🗄️ Views SQL

Três views foram criadas no PostgreSQL para análise dos dados:

### View 1 — `avg_temp_por_dispositivo`
Temperatura média por sensor/dispositivo.
```sql
CREATE VIEW avg_temp_por_dispositivo AS
SELECT device_id, ROUND(AVG(temp)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY device_id;
```

### View 2 — `leituras_por_hora`
Volume de leituras por hora do dia.
```sql
CREATE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM noted_date) AS hora, COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora ORDER BY hora;
```

### View 3 — `temp_max_min_por_dia`
Temperatura máxima e mínima por dia.
```sql
CREATE VIEW temp_max_min_por_dia AS
SELECT DATE(noted_date) AS data, MAX(temp) AS temp_max, MIN(temp) AS temp_min
FROM temperature_readings
GROUP BY data ORDER BY data;
```

---

## 📊 Dashboard

O dashboard apresenta:
- **Métricas gerais:** total de leituras, temperatura média, máxima e mínima
- **Gráfico 1:** Média de temperatura por dispositivo (barras)
- **Gráfico 2:** Volume de leituras por hora do dia (linha)
- **Gráfico 3:** Temperaturas máximas e mínimas por dia (linha)

---

## 💡 Principais Insights

- **Pico às 14h:** maior volume de leituras, indicando horário de maior calor/ocupação
- **Salto térmico em setembro/2018:** temperaturas máximas subiram de ~35°C para ~50°C
- **Temperatura média de 35,05°C:** sugere monitoramento de ambientes industriais ou de servidores
- **Amplitude térmica diária:** variação de até 30°C entre máxima e mínima no mesmo dia

---

## 📋 Comandos Git Utilizados

```bash
git init
git add .
git commit -m "mensagem"
git remote add origin URL
git push -u origin main
git pull
```

---

## 📚 Dataset

- **Nome:** Temperature Readings: IoT Devices
- **Fonte:** [Kaggle](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
- **Registros:** 97.606 leituras
- **Período:** Agosto a Novembro de 2018

---

*Projeto acadêmico — Disruptive Architectures: IoT, Big Data e IA | UniFECAF | 2025*
