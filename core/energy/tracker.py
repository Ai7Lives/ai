import time
import functools
from typing import Dict, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger('EnergyTracker')

@dataclass
class EnergyRecord:
    """Record of energy consumption."""
    operation: str
    duration_ms: float
    energy_wh: float
    timestamp: str
    cpu_model: str = "standard_cpu"

class EnergyTracker:
    """Production-grade energy tracking decorator."""
    
    def __init__(self, cpu_tdp_watts: float = 5.0):
        """Initialize with CPU TDP (Thermal Design Power)."""
        self.cpu_tdp = cpu_tdp_watts
        self.total_energy_wh = 0.0
        self.operation_log: list = []
        self.start_time = datetime.utcnow()
    
    def track(self, func: Callable) -> Callable:
        """Decorator to track energy consumption."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[Any, float]:
            op_name = f"{func.__module__}.{func.__name__}"
            start = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration_s = time.time() - start
                energy = self._compute_energy(duration_s)
                
                self.total_energy_wh += energy
                self._log_operation(op_name, duration_s * 1000, energy)
                
                logger.debug(f"[ENERGY] {op_name}: {energy:.4f} Wh ({duration_s*1000:.1f}ms)")
                return result, energy
            except Exception as e:
                logger.error(f"Error in {op_name}: {e}")
                raise
        
        return wrapper
    
    def _compute_energy(self, duration_seconds: float) -> float:
        """Compute energy consumption: E = P * t."""
        # Convert to hours and multiply by TDP
        hours = duration_seconds / 3600.0
        return self.cpu_tdp * hours
    
    def _log_operation(self, op_name: str, duration_ms: float, energy_wh: float) -> None:
        """Log operation to audit trail."""
        record = EnergyRecord(
            operation=op_name,
            duration_ms=duration_ms,
            energy_wh=energy_wh,
            timestamp=datetime.utcnow().isoformat()
        )
        self.operation_log.append(record)
    
    def get_total_energy(self) -> float:
        """Return total energy consumed in Wh."""
        return self.total_energy_wh
    
    def get_energy_report(self) -> Dict[str, Any]:
        """Generate energy consumption report."""
        return {
            'total_energy_wh': self.total_energy_wh,
            'operations_tracked': len(self.operation_log),
            'uptime_seconds': (datetime.utcnow() - self.start_time).total_seconds(),
            'average_power_w': self.cpu_tdp,
            'operation_log': [(r.operation, r.energy_wh) for r in self.operation_log[-10:]]
        }
    
    def reset(self) -> None:
        """Reset tracker."""
        self.total_energy_wh = 0.0
        self.operation_log.clear()
        self.start_time = datetime.utcnow()
