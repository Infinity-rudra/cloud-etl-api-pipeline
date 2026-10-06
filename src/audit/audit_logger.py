import os
import uuid
from datetime import datetime, timezone

import pandas as pd


AUDIT_DIR = "data/audit"
AUDIT_FILE = os.path.join(
    AUDIT_DIR,
    "pipeline_runs.csv"
)


def create_run_id():
    """Generate a unique pipeline run ID."""
    return str(uuid.uuid4())


def start_run():
    """Create metadata for a new pipeline run."""

    return {
        "run_id": create_run_id(),
        "pipeline_name": "cloud-etl-api-pipeline",
        "started_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "completed_at": "",
        "status": "RUNNING",
        "duration_seconds": 0,
        "rows_extracted": 0,
        "rows_valid": 0,
        "rows_rejected": 0,
        "rows_new": 0,
        "rows_changed": 0,
        "rows_unchanged": 0,
        "rows_deleted": 0,
        "raw_gcs_object": "",
        "processed_gcs_object": "",
        "error_message": ""
    }


def complete_run(
    run_metadata,
    start_time,
    status="SUCCESS",
    error_message=""
):
    """Finalize and save pipeline run metadata."""

    end_time = datetime.now(
        timezone.utc
    )

    run_metadata["completed_at"] = (
        end_time.isoformat()
    )

    run_metadata["status"] = status

    run_metadata["duration_seconds"] = round(
        (
            end_time - start_time
        ).total_seconds(),
        2
    )

    run_metadata["error_message"] = (
        error_message
    )

    save_run(run_metadata)


def save_run(run_metadata):
    """Append a pipeline run to the audit CSV."""

    os.makedirs(
        AUDIT_DIR,
        exist_ok=True
    )

    new_record = pd.DataFrame(
        [run_metadata]
    )

    if os.path.exists(AUDIT_FILE):

        existing = pd.read_csv(
            AUDIT_FILE
        )

        combined = pd.concat(
            [
                existing,
                new_record
            ],
            ignore_index=True
        )

    else:

        combined = new_record

    combined.to_csv(
        AUDIT_FILE,
        index=False
    )

    print(
        "\nPipeline audit record saved:"
    )

    print(
        AUDIT_FILE
    )