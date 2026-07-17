# NYC Taxi End-to-End Azure Data Engineering Project

## Overview
An end-to-end data engineering pipeline built on Azure that ingests 12 months of NYC Taxi trip data, processes it through a medallion architecture (Bronze → Silver → Gold), and serves it for analytics via Power BI.

## Architecture

NYC Taxi Website (source, monthly files)
      ↓  (Azure Data Factory — dynamic pipeline)
Bronze Layer — raw CSV (Azure Data Lake Storage)
      ↓  (Azure Databricks — PySpark transformations)
Silver Layer — cleaned/transformed data (Parquet)
      ↓  (Databricks — Delta Lake write + Delta tables)
Gold Layer — curated data (Delta format)
      ↓  (Spark SQL queries on Delta tables)
Power BI (via Databricks connector + access token)

## Tech Stack
- **Azure Data Factory** — dynamic pipeline for automated ingestion
- **Azure Databricks** — PySpark for transformation, Delta Lake for storage
- **Azure Data Lake Storage Gen2** — Bronze/Silver/Gold layered storage
- **Power BI** — reporting 
- **Source data:** NYC Taxi & Limousine Commission (TLC) trip data(https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Pipeline Flow

### 1. Ingestion (Azure Data Factory)
- Built a **dynamic pipeline** that loops through and downloads 12 months of NYC Taxi trip data directly from the NYC TLC website
- Used parameterization to avoid hardcoding each month's URL/filename
- Landed raw files as **CSV** in the **Bronze layer** of ADLS Gen2

### 2. Transformation (Azure Databricks — Bronze → Silver)
- Read raw CSV data from the Bronze layer into a Spark DataFrame
- Applied **PySpark transformations**: cleaning, type casting, handling nulls/duplicates, and structuring the schema
- Wrote the transformed output to the **Silver layer** in **Parquet** format

### 3. Curation (Azure Databricks — Silver → Gold)
- Read the Silver layer Parquet data into a DataFrame
- Wrote the curated output to the **Gold layer** in **Delta format**
- Created **Delta tables** on top of the Delta files
- Queried and validated the data using **Spark SQL** directly on the Delta tables

### 4. Consumption (Power BI)
- Connected **Power BI to Azure Databricks** using a **personal access token**

## Key Learnings
- Building dynamic, parameterized ADF pipelines to avoid manual/repetitive ingestion steps
- Implementing the medallion (Bronze/Silver/Gold) architecture pattern
- Difference in use cases between CSV → Parquet → Delta formats across each layer
- Using Delta Lake for ACID-compliant, queryable tables on top of data lake files
- Connecting Databricks as a data source for Power BI using token-based authentication

## Related Folders in this Repo
- ADF pipeline export: `adf-export/`
- Databricks notebooks: `databricks-notebooks/`
- Screenshots (storage structure, pipeline runs): `screenshots/`
- Full ADF chapter reference: `../02-azure-data-factory`
- Full Databricks chapter reference: `../04-azure-databricks`
- Synapse reference: `../05-azure-synapse-analytics`
