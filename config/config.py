import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_URL = os.getenv("API_URL", "https://dummyjson.com/products")
API_LIMIT = int(os.getenv("API_LIMIT", "30"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "etl_pipeline_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Validation Configuration
MINIMUM_ROWS = int(os.getenv("MINIMUM_ROWS", "1"))

# Google Cloud Storage
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Pipeline Configuration
LOAD_TO_POSTGRES = (
    os.getenv("LOAD_TO_POSTGRES", "true").lower() == "true"
)