
# 📊 YouTube Data Pipeline – ETL & BI Project

## 🚀 Overview

This project implements a complete **ETL (Extract – Transform – Load) pipeline** to collect, process, and analyze YouTube data using the **YouTube Data API v3**.

The pipeline extracts raw data from YouTube, transforms it into a structured analytical dataset using Python, and visualizes insights in **Power BI**.

It simulates a real-world **Data Engineering workflow**, including automation and scalability improvements.

---

## 🎯 Objectives

- Interact with a REST API and process JSON data  
- Build an automated data ingestion pipeline  
- Handle API constraints (pagination, quotas, batching)  
- Transform raw data into an analytical dataset  
- Create business insights using Power BI  
- Apply Data Engineering best practices  

---

## 🧱 Pipeline Architecture

```

YouTube API
↓
Python Ingestion Script
↓
Raw Data Storage (JSON)
↓
Data Transformation (Pandas)
↓
Structured Dataset (CSV)
↓
Power BI Dashboard

```

---

## ⚙️ Tech Stack

- **Python** (requests, pandas, json, dotenv)
- **YouTube Data API v3**
- **Power BI**
- **Docker** 🐳 (Bonus)
- **Apache Airflow** 🔁 (Bonus)
- **Git & GitHub**

---

## 📁 Project Structure

```

youtube-etl-pipeline/
│
├── data/
│   ├── raw/                # Raw JSON data
│   └── processed/          # Cleaned dataset (CSV)
│
├── src/
│   ├── extract.py          # API extraction logic
│   ├── transform.py        # Data cleaning & transformation
│   ├── load.py             # Save dataset
│   └── pipeline.py         # Main ETL pipeline
│
├── config/
│   └── .env                # Environment variables (API key)
│
├── airflow/                # DAG configuration (Bonus)
├── docker/                 # Docker setup (Bonus)
│
├── dashboard/
│   └── youtube.pbix        # Power BI dashboard
│
├── requirements.txt
├── Dockerfile
└── README.md

````

---

## 🔐 Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/youtube-etl-pipeline.git
cd youtube-etl-pipeline
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
YOUTUBE_API_KEY=your_api_key_here
```

---

## 📡 Data Extraction

* Extracts channel playlists
* Retrieves video IDs using pagination
* Fetches video details in batches (max 50 IDs/request)

### Key challenges handled:

* ✅ Pagination (`nextPageToken`)
* ✅ API quota limits
* ✅ Batch processing

---

## 🧹 Data Transformation

* Convert JSON → Pandas DataFrame
* Normalize fields:

  * Dates → datetime format
  * Duration → seconds
  * Metrics → numeric types
* Handle missing values
* Create analytical features

---

## 💾 Data Storage

* Raw data → JSON
* Processed data → CSV
* Organized into `/data/raw` and `/data/processed`

---

## 📊 Power BI Dashboard

The dashboard provides:

* 📈 Video performance over time
* 👍 Engagement analysis (likes, comments)
* 🔥 Most popular videos
* ⏱️ Impact of duration on performance
* 📊 Content trends

---

## 🐳 Bonus 1: Docker

* Containerized the pipeline
* Ensures reproducibility and portability

Run with:

```bash
docker build -t youtube-pipeline .
docker run youtube-pipeline
```

---

## 🔁 Bonus 2: Airflow Orchestration

* Implemented DAG for pipeline automation
* Scheduled execution (daily runs)

### Workflow:

* Extract
* Transform
* Load

---

## 🧠 Key Learnings

* API integration and data ingestion
* ETL pipeline design
* Data cleaning and transformation
* Automation with Airflow
* Containerization with Docker
* Data storytelling with Power BI

---

## ⚠️ Limitations

* API quota restrictions
* Limited historical data availability
* Missing engagement metrics on some videos
* No real-time streaming (batch processing only)

---

## 📌 Future Improvements

* Add a **data warehouse** (PostgreSQL / BigQuery)
* Switch to **ELT architecture**
* Implement **monitoring & logging**
* Add **incremental data loading**
* Deploy pipeline to cloud (GCP / AWS)

---

## 👤 Author

**Omar Hitar**
Data Analyst / Data Engineering

---

## 📎 Deliverables

* ✅ Python ETL Pipeline
* ✅ Clean dataset
* ✅ Power BI dashboard
* ✅ Docker container
* ✅ Airflow DAG
* ✅ GitHub repository

```
"# YouTube-Data-Pipeline-ETL-Data-Engineering-Project" 
