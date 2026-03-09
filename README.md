# 🔍 Credit Card Fraud Detection Pipeline

A machine learning pipeline and API for detecting fraudulent credit card transactions in real-time — developed by Shankara Narayana N G.

🌐 **Live Demo:** [https://credit-card-fraud-detection-dua2.onrender.com](https://credit-card-fraud-detection-dua2.onrender.com)

> ⏳ The application is hosted on Render's free tier. It may take approximately **1 minute to wake up** when you first hit the URL. Please be patient!

---

## 📖 Overview

The Fraud Detection Pipeline uses a **Random Forest classifier** to determine whether a given transaction is **fraudulent or legitimate**. It supports two modes of operation — direct file-based training and database-backed training — and exposes a FastAPI endpoint for real-time predictions.

Additionally, a **Kafka-based streaming application** is included for event-driven, real-time transaction processing.

The project is split into two independent applications:

- 🤖 **Fraud Detection API** — Trains the ML model and serves predictions via FastAPI
- 📨 **Fraud Kafka App** — A Kafka consumer/producer application that streams transactions to the prediction API in real time

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| ML Framework | scikit-learn (Random Forest), imbalanced-learn |
| API Framework | FastAPI + Uvicorn |
| Data Processing | Pandas |
| Serialisation | Joblib |
| Config | PyYAML, Pydantic |
| Visualisation | Matplotlib |
| Streaming | Apache Kafka |
| Dependency Management | Poetry |
| Notebook / Experimentation | `frauddetection.ipynb` |

> 📓 Other ML models were also tested and evaluated on the dataset. These experiments are documented in `frauddetection.ipynb`.

---

## 📦 Part 1 — Fraud Detection API

### ⚙️ Prerequisites

- Python 3.11 or above
- [Poetry](https://python-poetry.org/docs/#installation) installed

### Installation

```bash
git clone <repository-url>
cd frauddetectionpipeline
poetry install
```

---

### 🔧 Configuration

Before running, open the config file and set the run type based on your data source:

```yaml
# To read data from a file (default):
run:
  runtype: FILE

# To fetch data from a database:
run:
  runtype: DBRUN
```

- **`FILE`** — Reads training data directly from a local file
- **`DBRUN`** — Connects to the database, fetches the data, stores it as a file, and then trains the model on it

---

### 🤖 Step 1 — Build the ML Model

Train and save the Random Forest model locally before starting the API:

```bash
poetry run python -m mlbuild.main
```

> ⚠️ This step must be completed before running the API. The application depends on the saved model to serve predictions.

---

### ▶️ Step 2 — Run the FastAPI Application

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

---

### 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/predict` | Send a transaction payload to get a fraud or legitimate prediction |

Send your transaction details as a JSON body via Postman or any REST client to `/v1/predict`.

---

## 📨 Part 2 — Fraud Kafka Streaming App

A separate Kafka-based application that streams transactions to the Fraud Detection API in real time.

### ⚙️ Prerequisites

- Apache Kafka installed and available locally
- The **Fraud Detection API** (Part 1) running on `http://127.0.0.1:8000`

---

### 🔧 Kafka Setup (Windows)

Run each of the following in a separate terminal in order:

**1. Start Zookeeper**
```powershell
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

**2. Set Kafka heap options and start Kafka broker**
```powershell
$env:KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

**3. Create the transactions topic**
```powershell
bin\windows\kafka-topics.bat --create --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 🔧 Configure the Backend URL

In the Kafka app config file, set the URL of the running Fraud Detection API:

```yaml
applicationurl:
  API_URL: http://127.0.0.1:8000/v1/predict
```

---

### Installation

```bash
cd Fraudapp
poetry install
```

### ▶️ Run the Kafka Application

Once Kafka is running and the topic is created:

```bash
poetry run python -m app.main
```

---

## 👤 Author

**Shankara Narayana N G**
📧 shankarnarayana92@gmail.com

For further details on setup, configuration, or usage — please contact Shankara directly.

