import hashlib
import os
import pandas as pd


STATE_DIR = "data/state"
STATE_FILE = os.path.join(STATE_DIR, "latest_product_snapshot.csv")


def generate_record_hash(row):
    """
    Generate a stable SHA-256 hash for a product record.
    """

    fields = [
        row.get("id"),
        row.get("title"),
        row.get("description"),
        row.get("category"),
        row.get("price"),
        row.get("discountPercentage"),
        row.get("rating"),
        row.get("stock"),
        row.get("brand"),
        row.get("sku"),
        row.get("weight"),
        row.get("width"),
        row.get("height"),
        row.get("depth"),
        row.get("warrantyInformation"),
        row.get("shippingInformation"),
        row.get("availabilityStatus"),
        row.get("returnPolicy"),
        row.get("minimumOrderQuantity"),
    ]

    normalized = "|".join(
        "" if pd.isna(value) else str(value).strip()
        for value in fields
    )

    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def add_record_hash(df):
    """
    Add a SHA-256 record_hash column to the dataframe.
    """

    df = df.copy()
    df["record_hash"] = df.apply(generate_record_hash, axis=1)

    return df


def detect_changes(current_df):
    """
    Compare the current dataset with the previous snapshot.

    Returns:
        new_records
        changed_records
        unchanged_records
        deleted_records
    """

    current_df = add_record_hash(current_df)

    os.makedirs(STATE_DIR, exist_ok=True)

    if not os.path.exists(STATE_FILE):
        print("\nNo previous snapshot found.")
        print("Treating all records as NEW.")

        new_records = current_df.copy()
        changed_records = current_df.iloc[0:0].copy()
        unchanged_records = current_df.iloc[0:0].copy()
        deleted_records = current_df.iloc[0:0].copy()

        save_snapshot(current_df)

        return (
            new_records,
            changed_records,
            unchanged_records,
            deleted_records,
        )

    previous_df = pd.read_csv(STATE_FILE)

    if "record_hash" not in previous_df.columns:
        previous_df = add_record_hash(previous_df)

    previous_lookup = previous_df.set_index("id")["record_hash"].to_dict()

    current_ids = set(current_df["id"])
    previous_ids = set(previous_df["id"])

    new_records = current_df[
        ~current_df["id"].isin(previous_ids)
    ].copy()

    changed_records = current_df[
        current_df["id"].isin(previous_ids)
        & (
            current_df["id"].map(previous_lookup)
            != current_df["record_hash"]
        )
    ].copy()

    unchanged_records = current_df[
        current_df["id"].isin(previous_ids)
        & (
            current_df["id"].map(previous_lookup)
            == current_df["record_hash"]
        )
    ].copy()

    deleted_records = previous_df[
        ~previous_df["id"].isin(current_ids)
    ].copy()

    save_snapshot(current_df)

    return (
        new_records,
        changed_records,
        unchanged_records,
        deleted_records,
    )


def save_snapshot(df):
    """
    Save the current dataset as the latest state snapshot.
    """

    os.makedirs(STATE_DIR, exist_ok=True)

    df.to_csv(
        STATE_FILE,
        index=False
    )

    print("\nState snapshot updated:")
    print(STATE_FILE)