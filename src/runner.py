import uuid
import logging
from src.config import setup_logging, WORKER_COUNT

logger = setup_logging()

def execute_live_run():
    """Execute a live workflow run, generating a unique ID and activating workers."""
    run_id = str(uuid.uuid4())
    logger.info(f"Starting live run with ID: {run_id}")
    
    # Simulate workers being active
    workers_status = [f"worker_{i}_active" for i in range(WORKER_COUNT)]
    logger.info(f"Workers active: {workers_status}")
    
    return {
        "run_id": run_id,
        "status": "completed",
        "workers": workers_status
    }