# System Architecture

```mermaid
flowchart LR

    API["REST API<br/>DummyJSON Products"]

    INGEST["Python API Ingestion<br/>Requests"]

    RAW["Raw Dataset<br/>CSV"]

    TRANSFORM["Transformation<br/>Pandas"]

    VALIDATE["Data Quality<br/>Validation"]

    CHANGE["Incremental Change Detection<br/>SHA-256 Hash"]

    PROCESSED["Processed Dataset<br/>CSV"]

    GCS_RAW[("Google Cloud Storage<br/>Raw")]

    GCS_PROCESSED[("Google Cloud Storage<br/>Processed")]

    STAGING[("PostgreSQL<br/>staging.products")]

    ANALYTICS[("PostgreSQL<br/>analytics.products")]

    SCHEDULER["Cloud Scheduler"]

    RUN["Cloud Run Job"]

    AUDIT["Audit Logging"]

    CI["GitHub Actions<br/>Pytest"]

    API --> INGEST
    INGEST --> RAW
    RAW --> TRANSFORM
    TRANSFORM --> VALIDATE
    VALIDATE --> CHANGE
    CHANGE --> PROCESSED

    RAW --> GCS_RAW
    PROCESSED --> GCS_PROCESSED

    PROCESSED --> STAGING
    STAGING --> ANALYTICS

    SCHEDULER --> RUN
    RUN --> INGEST
    RUN --> GCS_RAW
    RUN --> GCS_PROCESSED
    RUN --> VALIDATE
    RUN --> CHANGE
    RUN --> AUDIT

    CI --> INGEST
    CI --> TRANSFORM
    CI --> VALIDATE