import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    """Executes and monitors workflow runs with SLA tracking."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'duration_seconds': 0,
            'records_processed': 0,
            'errors': 0,
            'latencies': []
        }
    
    def execute(self) -> Dict[str, Any]:
        """Execute the workflow run."""
        logger.info(f"Starting workflow run: {self.config.get('workflow', {}).get('id')}")
        
        self.metrics['start_time'] = datetime.now()
        
        try:
            # Simulate sequential processing
            batch_size = self.config['parameters']['batch_size']
            records_processed = 0
            
            for i in range(batch_size):
                record_id = i
                latency = self._process_record(record_id)
                self.metrics['latencies'].append(latency)
                records_processed += 1
                
                if i % 100 == 0:
                    logger.info(f"Processed {i}/{batch_size} records")
            
            self.metrics['records_processed'] = records_processed
            self.metrics['end_time'] = datetime.now()
            self.metrics['duration_seconds'] = (
                self.metrics['end_time'] - self.metrics['start_time']
            ).total_seconds()
            
            return self._validate_results()
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            self.metrics['errors'] = 1
            return self._validate_results()
    
    def _process_record(self, record_id: int) -> float:
        """Process a single record and return latency."""
        # Simulate processing time
        time.sleep(0.001)  # 1ms per record
        return 0.002  # 2ms average latency
    
    def _validate_results(self) -> Dict[str, Any]:
        """Validate results against SLA thresholds."""
        results = {
            'status': 'success',
            'metrics': self.metrics,
            'sla_compliance': self._check_sla()
        }
        
        if not self._check_sla():
            results['status'] = 'failed'
        
        return results
    
    def _check_sla(self) -> bool:
        """Check if metrics are within SLA thresholds."""
        thresholds = self.config['validation']['metrics_thresholds']
        sla = self.config['validation']['sla']
        
        if not self.metrics['latencies']:
            return False
        
        avg_latency = sum(self.metrics['latencies']) / len(self.metrics['latencies'])
        error_rate = self.metrics['errors'] / self.metrics['records_processed'] if self.metrics['records_processed'] > 0 else 0
        
        checks = [
            ('latency_p99_ms', avg_latency * 1.5 < thresholds['latency_p99_ms']),
            ('error_rate_percent', error_rate < thresholds['error_rate_percent']),
            ('throughput_per_sec', self.metrics['records_processed'] / self.metrics['duration_seconds'] > thresholds['throughput_per_sec'])
        ]
        
        return all(check[1] for check in checks)
    
    def get_logs(self) -> str:
        """Return captured run logs."""
        logs = [
            f"Workflow ID: {self.config.get('workflow', {}).get('id')}",
            f"Start Time: {self.metrics['start_time']}",
            f"End Time: {self.metrics['end_time']}",
            f"Duration: {self.metrics['duration_seconds']:.2f}s",
            f"Records Processed: {self.metrics['records_processed']}",
            f"Errors: {self.metrics['errors']}",
            f"Average Latency: {sum(self.metrics['latencies'])/len(self.metrics['latencies']):.4f}s",
            f"SLA Compliance: {self._check_sla()}",
        ]
        return "\n".join(logs)
