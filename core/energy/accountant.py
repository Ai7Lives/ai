from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class EnergyBudget:
    """Energy budget allocation."""
    allocated_wh: float
    reserved_wh: float
    consumed_wh: float = 0.0
    
    @property
    def available_wh(self) -> float:
        return self.allocated_wh - self.reserved_wh - self.consumed_wh
    
    @property
    def utilization_percent(self) -> float:
        return (self.consumed_wh / self.allocated_wh) * 100 if self.allocated_wh > 0 else 0

class EnergyAccountant:
    """Energy accounting and budgeting system."""
    
    def __init__(self):
        self.budgets: Dict[str, EnergyBudget] = {}
        self.consumption_history: List[Dict[str, Any]] = []
    
    def allocate_budget(self, entity_id: str, total_wh: float, reserved_percent: float = 10.0) -> EnergyBudget:
        """Allocate energy budget to entity."""
        reserved = (total_wh * reserved_percent) / 100.0
        budget = EnergyBudget(
            allocated_wh=total_wh,
            reserved_wh=reserved
        )
        self.budgets[entity_id] = budget
        return budget
    
    def consume(self, entity_id: str, energy_wh: float) -> bool:
        """Record energy consumption."""
        if entity_id not in self.budgets:
            return False
        
        budget = self.budgets[entity_id]
        if budget.available_wh < energy_wh:
            return False  # Insufficient budget
        
        budget.consumed_wh += energy_wh
        self.consumption_history.append({
            'entity': entity_id,
            'energy_wh': energy_wh,
            'timestamp': datetime.utcnow().isoformat(),
            'remaining_wh': budget.available_wh
        })
        return True
    
    def get_budget_status(self, entity_id: str) -> Dict[str, Any]:
        """Get budget status for entity."""
        if entity_id not in self.budgets:
            return {}
        
        budget = self.budgets[entity_id]
        return {
            'allocated_wh': budget.allocated_wh,
            'consumed_wh': budget.consumed_wh,
            'available_wh': budget.available_wh,
            'utilization_percent': budget.utilization_percent,
            'status': 'healthy' if budget.available_wh > 0 else 'critical'
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive energy report."""
        total_allocated = sum(b.allocated_wh for b in self.budgets.values())
        total_consumed = sum(b.consumed_wh for b in self.budgets.values())
        
        return {
            'total_allocated_wh': total_allocated,
            'total_consumed_wh': total_consumed,
            'global_utilization_percent': (total_consumed / total_allocated * 100) if total_allocated > 0 else 0,
            'entities': {eid: self.get_budget_status(eid) for eid in self.budgets.keys()},
            'recent_consumption': self.consumption_history[-50:]
        }
