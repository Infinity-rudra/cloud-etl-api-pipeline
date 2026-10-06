# Cloud ETL & API Data Pipeline

An end-to-end data engineering project that extracts product data from a REST API, processes and validates the data using Python, and loads analytics-ready data into PostgreSQL.

## Architecture

REST API
    ↓
Python API Ingestion
    ↓
Pagination + Retry Handling
    ↓
Raw CSV
    ↓
Transformation
    ↓
Data Quality Validation
    ↓
PostgreSQL UPSERT
    ↓
Database Validation
    ↓
SQL / Power BI

## Tech Stack

- Python
- REST API
- Requests
- Pandas
- PostgreSQL
- SQL
- Python-dotenv
- Pytest
- Git / GitHub
- Power BI

## Pipeline Features

### API Ingestion

- REST API integration
- Pagination
- Request timeout
- Retry handling
- HTTP error handling
- JSON processing

### Data Transformation

- CSV processing
- Column selection
- Numeric type conversion
- Processed data generation

### Data Quality

The pipeline validates:

- Minimum row count
- Required columns
- Numeric data types
- Duplicate rows
- Duplicate IDs
- Invalid prices
- Invalid stock values
- Missing values visibility

### PostgreSQL Loading

The pipeline uses UPSERT logic:

- New records are inserted
- Existing records are updated
- Duplicate primary keys are prevented

### Load Verification

After loading, the pipeline compares:

Processed records
vs.
PostgreSQL records

The pipeline fails if the counts do not match.

### Security

Database credentials are stored in `.env` and excluded from Git using `.gitignore`.

## Project Structure

```text
cloud-etl-api-pipeline/
│
├── config/
│   └── config.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── archive/
│
├── logs/
│
├── notebooks/
│
├── sql/
│   └── analysis.sql
│
├── src/
│   ├── ingestion/
│   │   └── api_client.py
│   │
│   ├── transformation/
│   │   └── transform.py
│   │
│   ├── validation/
│   │   └── validate.py
│   │
│   └── loading/
│       └── load.py
│
├── tests/
│   ├── __init__.py
│   └── test_validation.py
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt