# 🎬 Marapthon Season 2: Content Insights & Viewer Trends

This project analyzes viewer engagement and content performance during **Marapthon Season 2** on YouTube, focusing on identifying trends over time and content strategies that drive higher views.

---

## 🚀 Project Overview

Using the YouTube Data API, this pipeline collects video metadata and performance statistics, stores raw and transformed data in **Google Cloud Storage** and **BigQuery**, and visualizes insights in **Looker Studio**. The pipeline is fully orchestrated with **Apache Airflow**, and infrastructure is provisioned using **Terraform**.

---

## 🧩 Key Features

- 📥 **Batch Data Ingestion**: Automatically fetches daily YouTube data using the YouTube Data API.
- ☁️ **Cloud-native**: Runs on **Google Cloud Platform** with infrastructure as code (IaC) using Terraform.
- 🏗️ **Workflow Orchestration**: Full ETL pipeline built with Apache Airflow (Dockerized).
- 🧮 **Data Warehouse**: Optimized partitioned tables stored in **BigQuery**.
- 🔄 **Transformations**: Performed using **dbt** for clean, modular SQL models.
- 📊 **Visualization**: Looker Studio dashboard showing:
  - Day-of-week viewership trends
  - Top performing videos
  - Audience behavior during the season

---

## 📁 Project Structure

```
.
├── dags/                     # Airflow DAGs
├── dbt/                      # dbt models and configs
├── terraform/                # Terraform infrastructure config
├── creds.json                # GCP credentials (not tracked in Git)
├── docker-compose.yml        # Docker services for Airflow & Terraform
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 💻 How to Use

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-data-analysis.git
cd youtube-data-analysis
```

### 2. Add your Google Cloud credentials

Place your service account key as `creds.json` in the project root (same level as `docker-compose.yml`).

> ⚠️ Be sure to **add `creds.json` to `.gitignore`** and never commit it.

### 3. Provision infrastructure with Terraform

```bash
docker-compose run terraform
```

This will create:
- GCS bucket
- BigQuery dataset
- Service setup for the pipeline

### 4. Build and run Airflow

```bash
docker-compose up --build
```

Airflow web UI will be available at [http://localhost:8080](http://localhost:8080)  
Default login:  
- **Username**: `admin`  
- **Password**: `admin`

### 5. Trigger the DAG

Go to the Airflow UI, enable and trigger the DAG manually or wait for its schedule to kick in.

### 6. View the dashboard

Once your data is in BigQuery and transformed via dbt, view the insights in Looker Studio using your connected project.

---

## 🛠️ Tech Stack

- **GCP**: Google Cloud Storage, BigQuery
- **Apache Airflow** (with Docker)
- **Terraform**
- **dbt (Data Build Tool)**
- **Looker Studio**
- **Python**: `requests`, `pandas`, `google-api-python-client`, `google-cloud-storage`, etc.

---

## 📈 Dashboard Title

> **Marapthon Season 2: Content Insights & Viewer Trends**  
Gain insight into viewer behavior and video performance to optimize future content strategies.

---
