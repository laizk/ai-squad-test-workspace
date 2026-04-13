import pytest
from src.runner import execute_live_run
from src.validator import validate_output_data

def test_run_id_generated():
    """Verify that a unique run ID is generated during execution."""
    result = execute_live_run()
    assert "run_id" in result
    assert len(result["run_id"]) > 0

def test_workers_active():
    """Verify that workers are marked as active during execution."""
    result = execute_live_run()
    assert result["status"] == "completed"
    assert len(result["workers"]) > 0

def test_validation_passes():
    """Verify that valid data passes integrity checks without regression flags."""
    run_data = {"run_id": "123", "workers": ["w1"]}
    result = validate_output_data(run_data)
    assert result["valid"] is True
    assert result["regression"] is False

def test_validation_fails_missing_data():
    """Verify that missing data triggers integrity failure."""
    run_data = {}
    result = validate_output_data(run_data)
    assert result["valid"] is False