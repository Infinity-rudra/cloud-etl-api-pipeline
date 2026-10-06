import os

import pandas as pd

from config.config import MINIMUM_ROWS


REJECTED_DIR = "data/rejected"
REJECTED_FILE = os.path.join(
    REJECTED_DIR,
    "products_rejected.csv"
)


def identify_rejected_records(input_file):
    """
    Identify records that fail row-level data-quality rules.

    Returns:
        valid_df
        rejected_df
    """

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Processed file not found: {input_file}"
        )

    df = pd.read_csv(input_file)

    print(
        "\nStarting row-level data quality analysis."
    )

    rejected_mask = pd.Series(
        False,
        index=df.index
    )

    # --------------------------------------------------
    # Required fields
    # --------------------------------------------------

    required_value_columns = [
        "id",
        "title",
        "category",
        "price",
        "stock"
    ]

    for column in required_value_columns:

        if column in df.columns:

            rejected_mask |= (
                df[column].isnull()
                | (
                    df[column].astype(str).str.strip()
                    == ""
                )
            )

    # --------------------------------------------------
    # Price validation
    # --------------------------------------------------

    if "price" in df.columns:

        rejected_mask |= (
            pd.to_numeric(
                df["price"],
                errors="coerce"
            ).isnull()
            | (
                pd.to_numeric(
                    df["price"],
                    errors="coerce"
                ) <= 0
            )
        )

    # --------------------------------------------------
    # Stock validation
    # --------------------------------------------------

    if "stock" in df.columns:

        rejected_mask |= (
            pd.to_numeric(
                df["stock"],
                errors="coerce"
            ).isnull()
            | (
                pd.to_numeric(
                    df["stock"],
                    errors="coerce"
                ) < 0
            )
        )

    # --------------------------------------------------
    # Duplicate ID validation
    # --------------------------------------------------

    if "id" in df.columns:

        rejected_mask |= df["id"].duplicated(
            keep=False
        )

    valid_df = df[
        ~rejected_mask
    ].copy()

    rejected_df = df[
        rejected_mask
    ].copy()

    # --------------------------------------------------
    # Save rejected records
    # --------------------------------------------------

    os.makedirs(
        REJECTED_DIR,
        exist_ok=True
    )

    if not rejected_df.empty:

        rejected_df.to_csv(
            REJECTED_FILE,
            index=False
        )

        print(
            "\nRejected records saved:",
            REJECTED_FILE
        )

    else:

        # Remove an old rejected file if
        # the current run has no rejected records.

        if os.path.exists(REJECTED_FILE):
            os.remove(REJECTED_FILE)

        print(
            "\nNo rejected records found."
        )

    print(
        "Valid records:",
        len(valid_df)
    )

    print(
        "Rejected records:",
        len(rejected_df)
    )

    return valid_df, rejected_df


def validate_data(input_file):

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Processed file not found: {input_file}"
        )

    df = pd.read_csv(input_file)

    print(
        "Processed data loaded for validation."
    )

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    if df.empty:
        print("\nVALIDATION FAILED")
        print("Dataset is empty.")
        return False

    # --------------------------------------------------
    # Row count validation
    # --------------------------------------------------

    row_count_valid = (
        len(df) >= MINIMUM_ROWS
    )

    print(
        "\nRow Count Valid:",
        row_count_valid
    )

    # --------------------------------------------------
    # Required columns
    # --------------------------------------------------

    required_columns = [
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
        "meta"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    print(
        "\nMissing Required Columns:",
        missing_columns
    )

    # --------------------------------------------------
    # Data type validation
    # --------------------------------------------------

    numeric_columns = [
        "id",
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "weight",
        "minimumOrderQuantity"
    ]

    invalid_types = []

    for column in numeric_columns:

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):
            invalid_types.append(column)

    print(
        "\nColumns With Invalid Data Types:",
        invalid_types
    )

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    missing_values = df.isnull().sum()

    print("\nMissing Values:")
    print(missing_values)

    # --------------------------------------------------
    # Duplicate checks
    # --------------------------------------------------

    duplicate_rows = df.duplicated().sum()

    duplicate_ids = df["id"].duplicated().sum()

    print(
        "\nDuplicate Rows:",
        duplicate_rows
    )

    print(
        "Duplicate IDs:",
        duplicate_ids
    )

    # --------------------------------------------------
    # Value checks
    # --------------------------------------------------

    invalid_prices = (
        df["price"] <= 0
    ).sum()

    invalid_stock = (
        df["stock"] < 0
    ).sum()

    print(
        "Invalid Prices:",
        invalid_prices
    )

    print(
        "Invalid Stock:",
        invalid_stock
    )

    # --------------------------------------------------
    # Overall validation
    # --------------------------------------------------

    validation_passed = (
        row_count_valid
        and len(missing_columns) == 0
        and len(invalid_types) == 0
        and duplicate_rows == 0
        and duplicate_ids == 0
        and invalid_prices == 0
        and invalid_stock == 0
    )

    if validation_passed:
        print("\nVALIDATION PASSED")
    else:
        print("\nVALIDATION FAILED")

    return validation_passed