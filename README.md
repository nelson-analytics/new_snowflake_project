# 🚀 End-to-End Data Engineering Project on Snowflake

## 📘 Project Overview
This project demonstrates a **real-world end-to-end data engineering pipeline** using the **Snowflake Data Platform**.  
It involves **extracting JSON data from an API**, ingesting it into **Snowflake (Raw Layer)**, performing **data transformation and cleansing**, modeling the data into a **Star Schema**, and finally **visualizing insights using Streamlit dashboards**.

---

## 🧱 Architecture Overview

**Pipeline Flow:**
1. **Extract** JSON data from a REST API.  
2. **Load** data directly into Snowflake Raw Layer _or_ upload to **AWS S3** for auto-ingestion using Snowpipe.  
3. **Transform & Cleanse** data into curated tables (Star Schema).  
4. **Visualize** insights with **Streamlit dashboards**.

> The architecture diagram (Project Architecture.png) shows how data flows from the API source → S3/Snowflake → Transformation Layer → Visualization.

---

## 🧩 Project Structure

```
snowflake_e2e_project/
│
├── scripts/
│   ├── extract_and_upload_to_s3.py        # Extracts API data and uploads JSON files to S3
│   └── extract_and_load_direct.py         # Directly loads API JSON data into Snowflake RAW layer
│
├── snowflake/
│   └── pipeline_setup.sql                 # SQL script for database, schema, stage, and task setup
│
├── requirements.txt                       # All Python dependencies
└── README.md                              # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/snowflake_e2e_project.git
cd snowflake_e2e_project
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```
# API
API_ENDPOINT=https://api.example.com/data

# AWS
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name

# Snowflake
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PROJ_E2E_DB
SNOWFLAKE_SCHEMA=RAW
```

---

## 🧠 Scripts Description

### 🔹 `extract_and_upload_to_s3.py`
- Extracts JSON data from the API.
- Saves it locally and uploads it to an **S3 bucket**.
- Snowpipe automatically ingests this data into Snowflake’s RAW layer.

### 🔹 `extract_and_load_direct.py`
- Connects directly to Snowflake.
- Inserts JSON data straight into the RAW table for immediate analysis.

---

## 🧾 Snowflake SQL Setup (`pipeline_setup.sql`)

The SQL script performs the following:
- Creates **RAW** and **CLEAN** schemas.  
- Defines **stages**, **tables**, **streams**, and **tasks**.  
- Automates ingestion and transformation using **Snowpipe + Streams + Tasks**.  

Example command to run the setup:
```sql
!snowsql -a <account> -u <user> -f snowflake/pipeline_setup.sql
```

---

## 📊 Streamlit Dashboard

Once data is cleaned and modeled, you can visualize it using **Streamlit**.

Example run command:
```bash
streamlit run app.py
```

Your dashboard will display **real-time insights** from Snowflake’s CLEAN layer.

---

## 🌟 Highlights

✅ Automated ingestion via **Snowpipe**  
✅ Data freshness maintained with **Streams & Tasks**  
✅ Clear separation between **RAW** and **CLEAN** layers  
✅ Interactive visualization using **Streamlit**  

---

## 🧰 Requirements

All dependencies are listed in `requirements.txt`:

```
boto3
requests
snowflake-connector-python
python-dotenv
pandas
streamlit
```

---

## 🏁 Next Steps

- Add unit tests for transformation logic  
- Deploy Streamlit app to **Streamlit Cloud or AWS EC2**  
- Integrate **dbt or Airflow** for pipeline orchestration

---

## 💡 Author

**Nelson Ukaegbu**  
_Data Engineer | Cloud & Analytics Specialist_  

---

## 📜 License

MIT License © 2025 Nelson Ukaegbu
