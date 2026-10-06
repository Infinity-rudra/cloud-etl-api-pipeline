import logging
import os
import time
from datetime import datetime, timezone

from src.ingestion.api_client import extract_data
from src.transformation.transform import transform_data
from src.validation.validate import (
    validate_data,
    identify_rejected_records
)
from src.cloud.storage import upload_to_gcs
from src.incremental.change_detector import detect_changes
from src.audit.audit_logger import (
    start_run,
    complete_run
)
from config.config import LOAD_TO_POSTGRES


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

def run_pipeline():

    pipeline_start_time = time.time()

    audit_run = start_run()

    audit_start_time = datetime.now(
        timezone.utc
    )

    logger.info(
        "PIPELINE_STARTED | run_id=%s",
        audit_run["run_id"]
    )

    try:

        # ==================================================
        # 1. EXTRACT DATA FROM API
        # ==================================================

        df = extract_data()

        audit_run["rows_extracted"] = len(df)

        logger.info(
            "EXTRACTION_COMPLETED | rows=%s | columns=%s",
            len(df),
            len(df.columns)
        )

        # ==================================================
        # 2. UPLOAD RAW DATA TO GCS
        # ==================================================

        raw_object = upload_to_gcs(
            "data/raw/products_raw.csv",
            "raw"
        )

        audit_run["raw_gcs_object"] = raw_object

        logger.info(
            "RAW_UPLOAD_COMPLETED | object=%s",
            raw_object
        )

        # ==================================================
        # 3. TRANSFORM DATA
        # ==================================================

        processed_df = transform_data(
            "data/raw/products_raw.csv"
        )

        logger.info(
            "TRANSFORMATION_COMPLETED | rows=%s | columns=%s",
            len(processed_df),
            len(processed_df.columns)
        )

        # ==================================================
        # 4. DATASET-LEVEL VALIDATION
        # ==================================================

        validation_result = validate_data(
            "data/processed/products_processed.csv"
        )

        if not validation_result:

            logger.error(
                "VALIDATION_FAILED"
            )

            raise RuntimeError(
                "Dataset-level validation failed. "
                "Pipeline stopped."
            )

        logger.info(
            "VALIDATION_PASSED"
        )

        # ==================================================
        # 5. ROW-LEVEL DATA QUALITY
        # ==================================================

        valid_df, rejected_df = identify_rejected_records(
            "data/processed/products_processed.csv"
        )

        audit_run["rows_valid"] = len(valid_df)
        audit_run["rows_rejected"] = len(rejected_df)

        logger.info(
            "DATA_QUALITY_COMPLETED | valid=%s | rejected=%s",
            len(valid_df),
            len(rejected_df)
        )

        print(
            "\n========== DATA QUALITY =========="
        )

        print(
            f"Valid records    : {len(valid_df)}"
        )

        print(
            f"Rejected records : {len(rejected_df)}"
        )

        print(
            "==================================\n"
        )

        if not rejected_df.empty:

            logger.warning(
                "REJECTED_RECORDS_FOUND | count=%s",
                len(rejected_df)
            )

        else:

            logger.info(
                "NO_REJECTED_RECORDS"
            )

        # ==================================================
        # 6. CHANGE DETECTION
        # ==================================================

        (
            new_records,
            changed_records,
            unchanged_records,
            deleted_records,
        ) = detect_changes(
            processed_df
        )

        audit_run["rows_new"] = len(
            new_records
        )

        audit_run["rows_changed"] = len(
            changed_records
        )

        audit_run["rows_unchanged"] = len(
            unchanged_records
        )

        audit_run["rows_deleted"] = len(
            deleted_records
        )

        logger.info(
            "CHANGE_DETECTION_COMPLETED | "
            "new=%s | changed=%s | "
            "unchanged=%s | deleted=%s",
            len(new_records),
            len(changed_records),
            len(unchanged_records),
            len(deleted_records)
        )

        print(
            "\n========== CHANGE DETECTION =========="
        )

        print(
            f"New records       : {len(new_records)}"
        )

        print(
            f"Changed records   : {len(changed_records)}"
        )

        print(
            f"Unchanged records : {len(unchanged_records)}"
        )

        print(
            f"Deleted records   : {len(deleted_records)}"
        )

        print(
            "======================================\n"
        )

        # ==================================================
        # 7. UPLOAD PROCESSED DATA TO GCS
        # ==================================================

        processed_object = upload_to_gcs(
            "data/processed/products_processed.csv",
            "processed"
        )

        audit_run["processed_gcs_object"] = (
            processed_object
        )

        logger.info(
            "PROCESSED_UPLOAD_COMPLETED | object=%s",
            processed_object
        )

        # ==================================================
        # 8. LOAD DATA INTO POSTGRESQL
        # ==================================================

        if LOAD_TO_POSTGRES:

            logger.info(
                "POSTGRES_LOAD_STARTED"
            )

            from src.loading.load import load_data

            load_validation_result = load_data(
                "data/processed/products_processed.csv"
            )

            if not load_validation_result:

                logger.error(
                    "POSTGRES_VALIDATION_FAILED"
                )

                raise RuntimeError(
                    "Database validation failed."
                )

            logger.info(
                "POSTGRES_LOAD_COMPLETED"
            )

        else:

            logger.info(
                "POSTGRES_LOAD_SKIPPED"
            )

        # ==================================================
        # 9. COMPLETE AUDIT RECORD
        # ==================================================

        complete_run(
            audit_run,
            audit_start_time,
            status="SUCCESS"
        )

        duration = round(
            time.time() - pipeline_start_time,
            2
        )

        logger.info(
            "PIPELINE_COMPLETED | "
            "run_id=%s | duration_seconds=%s",
            audit_run["run_id"],
            duration
        )

        print(
            "\n========== PIPELINE COMPLETED SUCCESSFULLY ==========\n"
        )

        print(
            f"Run ID: {audit_run['run_id']}"
        )

        print(
            f"Duration: {duration} seconds"
        )

        print()

    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except Exception as error:

        duration = round(
            time.time() - pipeline_start_time,
            2
        )

        error_message = str(error)

        try:

            complete_run(
                audit_run,
                audit_start_time,
                status="FAILED",
                error_message=error_message
            )

        except Exception as audit_error:

            logger.error(
                "AUDIT_WRITE_FAILED | error=%s",
                audit_error
            )

        logger.exception(
            "PIPELINE_FAILED | "
            "run_id=%s | "
            "duration_seconds=%s | "
            "error=%s",
            audit_run["run_id"],
            duration,
            error_message
        )

        print(
            "\n========== PIPELINE FAILED =========="
        )

        print(
            f"Run ID: {audit_run['run_id']}"
        )

        print(
            f"Duration: {duration} seconds"
        )

        print(
            f"Error: {error_message}"
        )

        raise


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    run_pipeline()