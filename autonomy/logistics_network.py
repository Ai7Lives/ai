from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import heapq

@dataclass
class LogisticsTask:
    """Logistics task."""
    task_id: str
    location: tuple  # (x, y)
    priority: int
    deadline: Optional[float]
    resources_required: Dict[str, float]
    status: str = "pending"

class LogisticsNetwork:
    """Autonomous logistics and fulfillment network."""
    
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}  # agent_id -> state
        self.tasks: List[LogisticsTask] = []
        self.completed_tasks: List[LogisticsTask] = []
        self.routing_cache: Dict[str, List[tuple]] = {}
    
    def register_agent(self, agent_id: str, location: tuple, capacity: Dict[str, float]) -> None:
        """Register logistics agent."""
        self.agents[agent_id] = {
            'location': location,
            'capacity': capacity,
            'current_load': {},
            'assigned_tasks': []
        }
    
    def submit_task(self, task: LogisticsTask) -> bool:
        """Submit logistics task."""
        heapq.heappush(self.tasks, (task.priority, task.task_id, task))
        return True
    
    def allocate_task(self, agent_id: str, task: LogisticsTask) -> bool:
        """Allocate task to agent."""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # Check capacity
        for resource, required in task.resources_required.items():
            available = agent['capacity'].get(resource, 0) - sum(
                lt.resources_required.get(resource, 0) for lt in agent['assigned_tasks']
            )
            if available < required:
                return False
        
        task.status = "assigned"
        agent['assigned_tasks'].append(task)
        return True
    
    def compute_route(self, start: tuple, waypoints: List[tuple]) -> List[tuple]:
        """Compute optimal route."""
        # Simple nearest-neighbor for demo
        remaining = list(waypoints)
        route = [start]
        current = start
        
        while remaining:
            nearest = min(remaining, key=lambda p: self._distance(current, p))
            route.append(nearest)
            remaining.remove(nearest)
            current = nearest
        
        return route
    
    def _distance(self, p1: tuple, p2: tuple) -> float:
        """Euclidean distance."""
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get logistics network status."""
        return {
            'active_agents': len(self.agents),
            'pending_tasks': len(self.tasks),
            'completed_tasks': len(self.completed_tasks),
            'total_capacity': sum(a['capacity'].get('cargo_kg', 0) for a in self.agents.values())
        }
