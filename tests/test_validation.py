import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from workflow_executor import WorkflowExecutor
from monitor import Monitor


class TestWorkflowExecutor:
    """Test cases for workflow executor."""
    
    @pytest.fixture
    def config(self):
        """Provide test configuration."""
        return {
            'workflow': {
                'id': '07fef1c3',
                'name': 'full_sequential_validation'
            },
            'parameters': {
                'batch_size': 100,
                'timeout_seconds': 3600,
                'retry_count': 3,
                'parallelism': 4
            },
            'validation': {
                'baseline_version': 'v2.1.0',
                'metrics_thresholds': {
                    'latency_p99_ms': 500,
                    'error_rate_percent': 0.1,
                    'throughput_per_sec': 100
                },
                'sla': {
                    'max_duration_minutes': 60,
                    'min_throughput': 50,
                    'max_latency_ms': 1000
                }
            }
        }
    
    def test_executor_initialization(self, config):
        """Test that executor initializes correctly."""
        executor = WorkflowExecutor(config)
        assert executor.config == config
        assert executor.metrics['start_time'] is None
        assert executor.metrics['errors'] == 0
    
    def test_execute_workflow(self, config):
        """Test workflow execution completes successfully."""
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        assert results['status'] == 'success'
        assert results['metrics']['records_processed'] > 0
        assert results['metrics']['errors'] == 0
    
    def test_sla_compliance(self, config):
        """Test that results are SLA compliant."""
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        assert results['sla_compliance'] is True
        assert results['status'] == 'success'
    
    def test_metrics_collection(self, config):
        """Test that metrics are properly collected."""
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        metrics = results['metrics']
        assert 'start_time' in metrics
        assert 'end_time' in metrics
        assert 'duration_seconds' in metrics
        assert 'records_processed' in metrics
        assert 'latencies' in metrics
    
    def test_logs_generation(self, config):
        """Test that logs are generated correctly."""
        executor = WorkflowExecutor(config)
        results = executor.execute()
        logs = executor.get_logs()
        
        assert 'Workflow ID' in logs
        assert 'Start Time' in logs
        assert 'End Time' in logs
        assert 'Duration' in logs
        assert 'Records Processed' in logs
        assert 'Errors' in logs
        assert 'SLA Compliance' in logs


class TestMonitor:
    """Test cases for monitor."""
    
    @pytest.fixture
    def config(self):
        """Provide test configuration."""
        return {
            'workflow': {
                'id': '07fef1c3',
                'name': 'full_sequential_validation'
            },
            'parameters': {
                'batch_size': 100,
                'timeout_seconds': 3600,
                'retry_count': 3,
                'parallelism': 4
            },
            'validation': {
                'baseline_version': 'v2.1.0',
                'metrics_thresholds': {
                    'latency_p99_ms': 500,
                    'error_rate_percent': 0.1,
                    'throughput_per_sec': 100
                },
                'sla': {
                    'max_duration_minutes': 60,
                    'min_throughput': 50,
                    'max_latency_ms': 1000
                }
            }
        }
    
    def test_monitor_initialization(self, config):
        """Test that monitor initializes correctly."""
        monitor = Monitor(config)
        assert monitor.config == config
        assert monitor.log_buffer == []
    
    def test_start_monitoring(self, config):
        """Test that monitoring can be started."""
        monitor = Monitor(config)
        monitor.start_monitoring(None)
        
        assert len(monitor.log_buffer) == 1
        assert 'Monitoring initialized' in monitor.log_buffer[0]
    
    def test_capture_logs(self, config):
        """Test that logs can be captured."""
        monitor = Monitor(config)
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        logs = monitor.capture_logs(executor)
        
        assert 'Workflow ID' in logs
        assert 'Start Time' in logs
        assert 'End Time' in logs
    
    def test_check_metrics(self, config):
        """Test that metrics are checked against SLA."""
        monitor = Monitor(config)
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        status = monitor.check_metrics(results)
        
        assert 'metrics_within_sla' in status
        assert 'duration' in status
        assert 'records_processed' in status
        assert 'errors' in status
        assert 'timestamp' in status
    
    def test_generate_report(self, config):
        """Test that a report can be generated."""
        monitor = Monitor(config)
        executor = WorkflowExecutor(config)
        results = executor.execute()
        
        report = monitor.generate_report(results)
        
        assert 'WORKFLOW VALIDATION REPORT' in report
        assert 'Workflow ID' in report
        assert 'Status' in report
        assert 'Duration' in report
        assert 'Records Processed' in report
        assert 'SLA Compliant' in report
