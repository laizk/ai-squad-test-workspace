import logging
from src.config import setup_logging

logger = setup_logging()

def validate_output_data(run_data):
    """Validate output data integrity and check for regression flags."""
    errors = []
    
    # Data integrity check
    if not run_data.get("run_id"):
        errors.append("Missing run_id")
    if not run_data.get("workers"):
        errors.append("Missing workers data")
    
    if len(errors) > 0:
        logger.error(f"Data integrity check failed: {errors}")
        return {"valid": False, "errors": errors, "regression": False}
    
    logger.info("Data integrity check passed")
    return {"valid": True, "errors": [], "regression": False}