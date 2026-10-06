import os

import pandas as pd


def transform_data(input_file):

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    try:

        df = pd.read_csv(input_file)

    except pd.errors.EmptyDataError:
        raise RuntimeError(
            "Raw data file is empty."
        )

    except pd.errors.ParserError as error:
        raise RuntimeError(
            f"Could not parse raw CSV file: {error}"
        )

    print("Raw data loaded for transformation.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    columns_to_remove = [
        "thumbnail",
        "images"
    ]

    df = df.drop(
        columns=columns_to_remove,
        errors="ignore"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["stock"] = pd.to_numeric(
        df["stock"],
        errors="coerce"
    ).astype("Int64")

    output_file = (
        "data/processed/"
        "products_processed.csv"
    )

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Data transformation completed."
    )

    print(
        "Processed data saved:",
        output_file
    )

    return df