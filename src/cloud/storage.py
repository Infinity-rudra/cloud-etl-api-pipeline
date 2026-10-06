import os
from datetime import datetime, timezone

from google.cloud import storage

from config.config import GCS_BUCKET_NAME


def upload_to_gcs(local_file, folder):
    """Upload a local CSV file to Google Cloud Storage."""

    if not GCS_BUCKET_NAME:
        raise ValueError(
            "GCS_BUCKET_NAME is missing from the .env file."
        )

    if not os.path.exists(local_file):
        raise FileNotFoundError(
            f"Local file not found: {local_file}"
        )

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)

    timestamp = datetime.now(timezone.utc)

    object_name = (
        f"{folder}/"
        f"{timestamp.strftime('%Y/%m/%d')}/"
        f"{timestamp.strftime('%Y%m%d_%H%M%S')}_"
        f"{os.path.basename(local_file)}"
    )

    blob = bucket.blob(object_name)

    blob.upload_from_filename(
        local_file,
        content_type="text/csv"
    )

    print("\nGoogle Cloud Storage upload successful.")
    print("Bucket:", GCS_BUCKET_NAME)
    print("Object:", object_name)

    return object_name