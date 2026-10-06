from src.audit.audit_logger import start_run


def test_start_run_creates_valid_metadata():

    run = start_run()

    assert "run_id" in run
    assert run["run_id"]
    
    assert run["pipeline_name"] == (
        "cloud-etl-api-pipeline"
    )

    assert run["status"] == "RUNNING"

    assert run["rows_extracted"] == 0
    assert run["rows_valid"] == 0
    assert run["rows_rejected"] == 0