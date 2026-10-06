import os

import pandas as pd
import psycopg2
from psycopg2 import sql

from config.config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)


STAGING_SCHEMA = "staging"
ANALYTICS_SCHEMA = "analytics"

STAGING_TABLE = "products"
ANALYTICS_TABLE = "products"


def create_tables(cursor):
    """
    Create staging and analytics tables if they do not exist.
    """

    cursor.execute(
        f"""
        CREATE SCHEMA IF NOT EXISTS {STAGING_SCHEMA};

        CREATE SCHEMA IF NOT EXISTS {ANALYTICS_SCHEMA};

        CREATE TABLE IF NOT EXISTS
        {STAGING_SCHEMA}.{STAGING_TABLE} (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            category TEXT,
            price NUMERIC(12,2),
            discountPercentage NUMERIC(8,2),
            rating NUMERIC(8,2),
            stock INTEGER,
            tags TEXT,
            brand TEXT,
            sku TEXT,
            weight NUMERIC(10,2),
            dimensions TEXT,
            warrantyInformation TEXT,
            shippingInformation TEXT,
            availabilityStatus TEXT,
            reviews TEXT,
            returnPolicy TEXT,
            minimumOrderQuantity INTEGER,
            meta TEXT,
            record_hash TEXT
        );

        CREATE TABLE IF NOT EXISTS
        {ANALYTICS_SCHEMA}.{ANALYTICS_TABLE} (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            category TEXT,
            price NUMERIC(12,2),
            discountPercentage NUMERIC(8,2),
            rating NUMERIC(8,2),
            stock INTEGER,
            tags TEXT,
            brand TEXT,
            sku TEXT,
            weight NUMERIC(10,2),
            dimensions TEXT,
            warrantyInformation TEXT,
            shippingInformation TEXT,
            availabilityStatus TEXT,
            reviews TEXT,
            returnPolicy TEXT,
            minimumOrderQuantity INTEGER,
            meta TEXT,
            record_hash TEXT,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


def load_into_staging(cursor, df):
    """
    Load processed data into staging.products.

    Existing records are updated using UPSERT.
    """

    columns = [
        "id",
        "title",
        "description",
        "category",
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "tags",
        "brand",
        "sku",
        "weight",
        "dimensions",
        "warrantyInformation",
        "shippingInformation",
        "availabilityStatus",
        "reviews",
        "returnPolicy",
        "minimumOrderQuantity",
        "meta",
        "record_hash",
    ]

    insert_query = f"""
        INSERT INTO staging.products (
            {", ".join(columns)}
        )
        VALUES (
            {", ".join(["%s"] * len(columns))}
        )
        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            category = EXCLUDED.category,
            price = EXCLUDED.price,
            discountPercentage = EXCLUDED.discountPercentage,
            rating = EXCLUDED.rating,
            stock = EXCLUDED.stock,
            tags = EXCLUDED.tags,
            brand = EXCLUDED.brand,
            sku = EXCLUDED.sku,
            weight = EXCLUDED.weight,
            dimensions = EXCLUDED.dimensions,
            warrantyInformation = EXCLUDED.warrantyInformation,
            shippingInformation = EXCLUDED.shippingInformation,
            availabilityStatus = EXCLUDED.availabilityStatus,
            reviews = EXCLUDED.reviews,
            returnPolicy = EXCLUDED.returnPolicy,
            minimumOrderQuantity = EXCLUDED.minimumOrderQuantity,
            meta = EXCLUDED.meta,
            record_hash = EXCLUDED.record_hash;
    """

    for _, row in df.iterrows():

        values = [
            row.get(column)
            for column in columns
        ]

        cursor.execute(
            insert_query,
            values
        )


def refresh_analytics_table(cursor):
    """
    Refresh the analytics layer from staging.
    """

    cursor.execute(
        """
        INSERT INTO analytics.products (
            id,
            title,
            description,
            category,
            price,
            discountPercentage,
            rating,
            stock,
            tags,
            brand,
            sku,
            weight,
            dimensions,
            warrantyInformation,
            shippingInformation,
            availabilityStatus,
            reviews,
            returnPolicy,
            minimumOrderQuantity,
            meta,
            record_hash,
            loaded_at
        )
        SELECT
            id,
            title,
            description,
            category,
            price,
            discountPercentage,
            rating,
            stock,
            tags,
            brand,
            sku,
            weight,
            dimensions,
            warrantyInformation,
            shippingInformation,
            availabilityStatus,
            reviews,
            returnPolicy,
            minimumOrderQuantity,
            meta,
            record_hash,
            CURRENT_TIMESTAMP
        FROM staging.products
        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            category = EXCLUDED.category,
            price = EXCLUDED.price,
            discountPercentage = EXCLUDED.discountPercentage,
            rating = EXCLUDED.rating,
            stock = EXCLUDED.stock,
            tags = EXCLUDED.tags,
            brand = EXCLUDED.brand,
            sku = EXCLUDED.sku,
            weight = EXCLUDED.weight,
            dimensions = EXCLUDED.dimensions,
            warrantyInformation = EXCLUDED.warrantyInformation,
            shippingInformation = EXCLUDED.shippingInformation,
            availabilityStatus = EXCLUDED.availabilityStatus,
            reviews = EXCLUDED.reviews,
            returnPolicy = EXCLUDED.returnPolicy,
            minimumOrderQuantity = EXCLUDED.minimumOrderQuantity,
            meta = EXCLUDED.meta,
            record_hash = EXCLUDED.record_hash,
            loaded_at = CURRENT_TIMESTAMP;
        """
    )


def load_data(input_file):

    if not os.path.exists(input_file):

        raise FileNotFoundError(
            f"Processed file not found: {input_file}"
        )

    df = pd.read_csv(input_file)

    print(
        "Processed data loaded for PostgreSQL."
    )

    print(
        "Rows:",
        len(df)
    )

    print(
        "Columns:",
        len(df.columns)
    )

    connection = None

    try:

        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )

        cursor = connection.cursor()

        # --------------------------------------------------
        # Create schemas and tables
        # --------------------------------------------------

        create_tables(cursor)

        # --------------------------------------------------
        # Load staging layer
        # --------------------------------------------------

        load_into_staging(
            cursor,
            df
        )

        print(
            "Staging load completed."
        )

        # --------------------------------------------------
        # Refresh analytics layer
        # --------------------------------------------------

        refresh_analytics_table(
            cursor
        )

        print(
            "Analytics layer refreshed."
        )

        # --------------------------------------------------
        # Validate staging row count
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM staging.products;
            """
        )

        staging_count = cursor.fetchone()[0]

        print(
            "Staging row count:",
            staging_count
        )

        # --------------------------------------------------
        # Validate analytics row count
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM analytics.products;
            """
        )

        analytics_count = cursor.fetchone()[0]

        print(
            "Analytics row count:",
            analytics_count
        )

        if staging_count != len(df):

            raise RuntimeError(
                "Staging row count validation failed."
            )

        if analytics_count != staging_count:

            raise RuntimeError(
                "Analytics row count validation failed."
            )

        connection.commit()

        print(
            "PostgreSQL staging and analytics validation passed."
        )

        return True

    except Exception:

        if connection:
            connection.rollback()

        raise

    finally:

        if connection:

            connection.close()

            print(
                "PostgreSQL connection closed."
            )