from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import heapq

@dataclass
class ComputeTask:
    """Task for scheduler."""
    task_id: str
    energy_budget_wh: float
    priority: int  # 1=critical, 5=low
    duration_estimate_s: float
    deadline: Optional[datetime] = None
    status: str = "pending"

class SustainableScheduler:
    """Schedules workloads based on renewable energy availability."""
    
    def __init__(self, renewable_enabled: bool = True):
        self.renewable_enabled = renewable_enabled
        self.task_queue: List[ComputeTask] = []
        self.scheduled_tasks: Dict[str, ComputeTask] = {}
        self.carbon_intensity_api = "https://api.electricitymap.org/v3/carbon-intensity/latest"
    
    def submit_task(self, task: ComputeTask) -> bool:
        """Submit task for scheduling."""
        heapq.heappush(self.task_queue, (task.priority, task.task_id, task))
        return True
    
    def schedule_next(self, available_carbon_grams: float, available_energy_wh: float) -> Optional[ComputeTask]:
        """Schedule next task based on energy availability."""
        if not self.task_queue:
            return None
        
        # Get highest priority task
        priority, task_id, task = heapq.heappop(self.task_queue)
        
        # Check if within carbon/energy budget
        if task.energy_budget_wh <= available_energy_wh:
            task.status = "scheduled"
            self.scheduled_tasks[task.task_id] = task
            return task
        else:
            # Requeue task
            heapq.heappush(self.task_queue, (priority, task_id, task))
            return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        return {
            'pending_tasks': len(self.task_queue),
            'scheduled_tasks': len(self.scheduled_tasks),
            'renewable_enabled': self.renewable_enabled
        }
    
    def mark_complete(self, task_id: str) -> bool:
        """Mark task as complete."""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id].status = "complete"
            del self.scheduled_tasks[task_id]
            return True
        return False
