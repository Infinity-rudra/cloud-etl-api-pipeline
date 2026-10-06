# Cloud ETL & API Data Pipeline

An end-to-end cloud data engineering pipeline that extracts product data from a REST API, transforms and validates the data using Python, detects record-level changes, stores raw and processed data in Google Cloud Storage, and loads analytics-ready data into PostgreSQL.

The project is designed to demonstrate practical **ETL, API integration, data quality, cloud execution, database loading, monitoring, testing, and CI** rather than simply showcasing individual tools.

---

## Project Overview

This project implements a production-style ETL workflow for product data obtained from a REST API.

The pipeline:

1. Extracts paginated data from a REST API
2. Handles request timeouts, retries, and HTTP errors
3. Stores the raw API response as CSV
4. Transforms the dataset using Pandas
5. Performs dataset-level and row-level data quality checks
6. Detects new, changed, unchanged, and deleted records using record hashing
7. Stores raw and processed datasets in Google Cloud Storage
8. Loads validated data into PostgreSQL staging and analytics schemas
9. Records pipeline execution metadata through audit logging
10. Runs automatically in Google Cloud Run Jobs
11. Can be triggered on a schedule using Google Cloud Scheduler
12. Runs automated tests through GitHub Actions

---

## Architecture

```mermaid
flowchart LR

    A[REST API<br/>DummyJSON Products]
    B[Python API Client<br/>Requests]
    C[Raw CSV]
    D[Transformation<br/>Pandas]
    E[Data Quality<br/>Validation]
    F[Change Detection<br/>SHA-256 Hash]
    G[Processed CSV]

    H[(Google Cloud Storage<br/>Raw)]
    I[(Google Cloud Storage<br/>Processed)]

    J[(PostgreSQL<br/>staging.products)]
    K[(PostgreSQL<br/>analytics.products)]

    L[Cloud Run Job]
    M[Cloud Scheduler]
    N[Audit Log]
    O[GitHub Actions<br/>Pytest]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    C --> H
    G --> I
    G --> J
    J --> K

    M --> L
    L --> B
    L --> H
    L --> I
    L --> E
    L --> F

    L --> N
    O --> B