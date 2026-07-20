from typing import Dict, Any
from dataclasses import dataclass, field
from collections import defaultdict
import time

@dataclass
class MetricValue:
    """Single metric value."""
    value: float
    timestamp: float
    unit: str

class MetricsCollector:
    """Prometheus-style metrics collection."""
    
    def __init__(self):
        self.metrics: Dict[str, list] = defaultdict(list)
        self.start_time = time.time()
    
    def counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None) -> None:
        """Record counter metric."""
        metric_key = f"{name}:{json.dumps(labels or {})}"
        self.metrics[metric_key].append(MetricValue(
            value=value,
            timestamp=time.time(),
            unit='count'
        ))
    
    def gauge(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """Record gauge metric."""
        metric_key = f"{name}:{json.dumps(labels or {})}"
        self.metrics[metric_key].append(MetricValue(
            value=value,
            timestamp=time.time(),
            unit='value'
        ))
    
    def histogram(self, name: str, value: float, buckets: list = None, labels: Dict[str, str] = None) -> None:
        """Record histogram metric."""
        metric_key = f"{name}:{json.dumps(labels or {})}"
        self.metrics[metric_key].append(MetricValue(
            value=value,
            timestamp=time.time(),
            unit='histogram'
        ))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return {
            'uptime_seconds': time.time() - self.start_time,
            'metrics_count': len(self.metrics),
            'sample_count': sum(len(v) for v in self.metrics.values())
        }
    
    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        for metric_key, values in self.metrics.items():
            if values:
                latest = values[-1]
                lines.append(f"{metric_key} {latest.value}")
        return "\n".join(lines)

import json
