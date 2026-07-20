from typing import Dict, Any, List
from dataclasses import dataclass
import random

@dataclass
class ComputeNode:
    """Compute node for distributed inference."""
    node_id: str
    location: str
    carbon_intensity_grams_kwh: float
    cpu_utilization_percent: float
    power_available_w: float
    renewable_percent: float

class ComputeRouter:
    """Routes inference to sustainable nodes."""
    
    def __init__(self):
        self.nodes: Dict[str, ComputeNode] = {}
        self.routing_history: List[Dict[str, Any]] = []
    
    def register_node(self, node: ComputeNode) -> None:
        """Register a compute node."""
        self.nodes[node.node_id] = node
    
    def find_sustainable_route(self, workload_type: str, energy_budget_wh: float) -> Optional[ComputeNode]:
        """Find sustainable node for workload."""
        # Filter available nodes
        candidates = [
            n for n in self.nodes.values()
            if n.cpu_utilization_percent < 80 and n.power_available_w * 3600 / 1000 > energy_budget_wh
        ]
        
        if not candidates:
            return None
        
        # Sort by carbon intensity (prefer renewable)
        candidates.sort(key=lambda n: n.carbon_intensity_grams_kwh)
        selected = candidates[0]
        
        self.routing_history.append({
            'workload': workload_type,
            'selected_node': selected.node_id,
            'carbon_grams_kwh': selected.carbon_intensity_grams_kwh,
            'renewable_percent': selected.renewable_percent
        })
        
        return selected
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        if not self.routing_history:
            return {'total_routes': 0, 'average_carbon_grams_kwh': 0}
        
        avg_carbon = sum(r['carbon_grams_kwh'] for r in self.routing_history) / len(self.routing_history)
        avg_renewable = sum(r['renewable_percent'] for r in self.routing_history) / len(self.routing_history)
        
        return {
            'total_routes': len(self.routing_history),
            'average_carbon_grams_kwh': avg_carbon,
            'average_renewable_percent': avg_renewable,
            'active_nodes': len(self.nodes)
        }
