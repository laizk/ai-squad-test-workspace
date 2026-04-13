import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class Monitor:
    """Monitors workflow execution and captures logs."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_buffer = []
    
    def start_monitoring(self, executor: Any) -> None:
        """Start monitoring the workflow execution."""
        logger.info("Monitoring started")
        self.log_buffer.append(f"[{datetime.now()}] Monitoring initialized")
    
    def capture_logs(self, executor: Any) -> str:
        """Capture and return complete run logs."""
        logs = executor.get_logs()
        self.log_buffer.append(f"[{datetime.now()}] Logs captured: {len(logs)} lines")
        return logs
    
    def check_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check if metrics are within defined SLA."""
        metrics = results.get('metrics', {})
        sla_compliance = results.get('sla_compliance', False)
        
        status = {
            'metrics_within_sla': sla_compliance,
            'duration': metrics.get('duration_seconds', 0),
            'records_processed': metrics.get('records_processed', 0),
            'errors': metrics.get('errors', 0),
            'timestamp': datetime.now().isoformat()
        }
        
        if not sla_compliance:
            status['status'] = 'SLA VIOLATION'
            logger.warning("Metrics outside SLA thresholds")
        else:
            status['status'] = 'COMPLIANT'
        
        return status
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a summary report."""
        report = [
            "=" * 60,
            "WORKFLOW VALIDATION REPORT",
            "=" * 60,
            f"Workflow ID: {results.get('workflow_id', 'N/A')}",
            f"Status: {results.get('status', 'N/A')}",
            f"Duration: {results.get('metrics', {}).get('duration_seconds', 0):.2f}s",
            f"Records Processed: {results.get('metrics', {}).get('records_processed', 0)}",
            f"Errors: {results.get('metrics', {}).get('errors', 0)}",
            f"SLA Compliant: {results.get('sla_compliance', False)}",
            "=" * 60,
        ]
        
        return "\n".join(report)
