import logging
import os

# Workflow Parameters - Locked
# These constants define the behavior of the workflow and should not be modified
# without approval from the dev-sr role.
WORKFLOW_MAX_RETRIES = 3
WORKFLOW_TIMEOUT_SECONDS = 3600
WORKER_COUNT = 4
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def setup_logging():
    """Configure and return the workflow logger."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger("workflow")