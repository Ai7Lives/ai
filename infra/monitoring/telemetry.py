from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class TelemetryEvent:
    """Telemetry event."""
    event_type: str
    component: str
    metrics: Dict[str, Any]
    timestamp: str

class Telemetry:
    """Energy and carbon telemetry."""
    
    def __init__(self):
        self.events: List[TelemetryEvent] = []
        self.carbon_tracker = {}
    
    def record_event(self, event_type: str, component: str, metrics: Dict[str, Any]) -> None:
        """Record telemetry event."""
        event = TelemetryEvent(
            event_type=event_type,
            component=component,
            metrics=metrics,
            timestamp=datetime.utcnow().isoformat()
        )
        self.events.append(event)
    
    def record_carbon_emission(self, source: str, grams_co2: float) -> None:
        """Record carbon emission."""
        if source not in self.carbon_tracker:
            self.carbon_tracker[source] = 0.0
        self.carbon_tracker[source] += grams_co2
    
    def get_carbon_report(self) -> Dict[str, Any]:
        """Generate carbon emission report."""
        total_carbon = sum(self.carbon_tracker.values())
        return {
            'total_grams_co2': total_carbon,
            'sources': self.carbon_tracker,
            'events_recorded': len(self.events)
        }
    
    def export_metrics(self, format: str = 'json') -> str:
        """Export metrics in specified format."""
        if format == 'json':
            events_dict = [{
                'type': e.event_type,
                'component': e.component,
                'metrics': e.metrics,
                'timestamp': e.timestamp
            } for e in self.events]
            return json.dumps(events_dict, indent=2)
        return ""
