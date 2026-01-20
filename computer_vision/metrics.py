"""
Performance metrics tracking for CV operations.

Tracks and reports key performance indicators for barcode detection,
decode success rates, and processing times.
"""

import time
from collections import defaultdict
from datetime import datetime


class MetricsCollector:
    """
    Collects and aggregates performance metrics for CV operations.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.decode_times = []
        self.capture_times = []
        self.success_count = 0
        self.failure_count = 0
        self.quality_failures = defaultdict(int)
        self.start_time = datetime.now()
    
    def record_decode_time(self, duration):
        """
        Record barcode decode operation time.
        
        Args:
            duration: Time taken in seconds
        """
        self.decode_times.append(duration)
    
    def record_capture_time(self, duration):
        """
        Record image capture operation time.
        
        Args:
            duration: Time taken in seconds
        """
        self.capture_times.append(duration)
    
    def record_success(self):
        """Record successful barcode decode."""
        self.success_count += 1
    
    def record_failure(self, reason=None):
        """
        Record failed barcode decode.
        
        Args:
            reason: Optional failure reason category
        """
        self.failure_count += 1
        if reason:
            self.quality_failures[reason] += 1
    
    def get_statistics(self):
        """
        Get current performance statistics.
        
        Returns:
            Dictionary containing performance metrics
        """
        total_operations = self.success_count + self.failure_count
        success_rate = (self.success_count / total_operations * 100) if total_operations > 0 else 0
        
        return {
            'total_operations': total_operations,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate': f"{success_rate:.2f}%",
            'avg_decode_time': sum(self.decode_times) / len(self.decode_times) if self.decode_times else 0,
            'avg_capture_time': sum(self.capture_times) / len(self.capture_times) if self.capture_times else 0,
            'uptime': str(datetime.now() - self.start_time),
            'quality_failures': dict(self.quality_failures)
        }
    
    def reset(self):
        """Reset all metrics."""
        self.__init__()


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, metrics_collector=None, operation_type='decode'):
        """
        Initialize timer.
        
        Args:
            metrics_collector: Optional MetricsCollector instance
            operation_type: Type of operation ('decode' or 'capture')
        """
        self.metrics_collector = metrics_collector
        self.operation_type = operation_type
        self.start_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        
        if self.metrics_collector:
            if self.operation_type == 'decode':
                self.metrics_collector.record_decode_time(self.duration)
            elif self.operation_type == 'capture':
                self.metrics_collector.record_capture_time(self.duration)
