import time
import psutil
import os
from typing import Dict, Callable, Any
from functools import wraps
from .utils import setup_logging
from .config import Config


def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor the performance of a function.
    Measures execution time and memory usage.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = setup_logging(Config.LOG_LEVEL)

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Record start time
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Record end time
        end_time = time.time()
        execution_time = end_time - start_time

        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory

        logger.info(f"{func.__name__} executed in {execution_time:.2f}s, memory change: {memory_used:.2f}MB")

        return result

    return wrapper


class PerformanceMonitor:
    """
    A class to monitor performance metrics during pipeline execution.
    """

    def __init__(self):
        self.logger = setup_logging(Config.LOG_LEVEL)
        self.process = psutil.Process(os.getpid())
        self.metrics = {}

    def start_monitoring(self, operation_name: str):
        """
        Start monitoring for a specific operation.

        Args:
            operation_name: Name of the operation being monitored
        """
        start_time = time.time()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        # Store start metrics
        self.metrics[operation_name] = {
            'start_time': start_time,
            'start_memory': start_memory
        }

    def stop_monitoring(self, operation_name: str) -> Dict[str, float]:
        """
        Stop monitoring for a specific operation and return metrics.

        Args:
            operation_name: Name of the operation to stop monitoring

        Returns:
            Dictionary with performance metrics
        """
        if operation_name not in self.metrics:
            self.logger.warning(f"No start metrics found for operation: {operation_name}")
            return {}

        # Get end metrics
        end_time = time.time()
        end_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        # Calculate metrics
        start_time = self.metrics[operation_name]['start_time']
        start_memory = self.metrics[operation_name]['start_memory']

        execution_time = end_time - start_time
        memory_used = end_memory - start_memory

        # Log metrics
        self.logger.info(
            f"{operation_name} completed in {execution_time:.2f}s, "
            f"memory used: {memory_used:.2f}MB"
        )

        # Return metrics
        metrics = {
            'execution_time': execution_time,
            'memory_used': memory_used,
            'start_memory': start_memory,
            'end_memory': end_memory
        }

        return metrics

    def get_system_metrics(self) -> Dict[str, float]:
        """
        Get current system metrics.

        Returns:
            Dictionary with system metrics
        """
        cpu_percent = self.process.cpu_percent()
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024

        return {
            'cpu_percent': cpu_percent,
            'memory_mb': memory_mb,
            'memory_percent': self.process.memory_percent()
        }

    def check_limits(self, max_memory_mb: float = 1000.0) -> bool:
        """
        Check if current memory usage is within limits.

        Args:
            max_memory_mb: Maximum allowed memory usage in MB

        Returns:
            True if within limits, False otherwise
        """
        current_memory = self.process.memory_info().rss / 1024 / 1024
        if current_memory > max_memory_mb:
            self.logger.warning(f"Memory usage ({current_memory:.2f}MB) exceeds limit ({max_memory_mb}MB)")
            return False
        return True