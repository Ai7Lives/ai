from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime

class AgentState(Enum):
    """Agent lifecycle states."""
    INIT = 'init'
    READY = 'ready'
    EXECUTING = 'executing'
    IDLE = 'idle'
    ERROR = 'error'
    SHUTDOWN = 'shutdown'

@dataclass
class AgentConfig:
    """Agent configuration."""
    agent_id: str
    energy_budget_wh: float
    max_duration_hours: float
    safety_level: str  # 'critical', 'high', 'normal'
    autonomous: bool = True

class AutonomousAgent:
    """Durable autonomous agent with long-duration support."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.state = AgentState.INIT
        self.energy_remaining = config.energy_budget_wh
        self.start_time = datetime.utcnow()
        self.mission_log: List[Dict[str, Any]] = []
        self.checkpoint_frequency_hours = 0.5
    
    async def run(self) -> Dict[str, Any]:
        """Main agent loop."""
        self.state = AgentState.READY
        cycle = 0
        
        try:
            while self.state != AgentState.SHUTDOWN:
                cycle += 1
                
                # Check energy and time constraints
                if self.energy_remaining < 10.0:
                    await self._enter_low_power_mode()
                
                uptime = (datetime.utcnow() - self.start_time).total_seconds() / 3600
                if uptime > self.config.max_duration_hours:
                    await self._graceful_shutdown()
                    break
                
                # Execute cycle
                self.state = AgentState.EXECUTING
                action = await self._decide_next_action()
                await self._execute_action(action)
                
                # Checkpoint periodically
                if cycle % 10 == 0:
                    await self._checkpoint_state()
                
                self.state = AgentState.IDLE
                await asyncio.sleep(1)  # Cycle delay
        
        except Exception as e:
            self.state = AgentState.ERROR
            self.mission_log.append({'error': str(e), 'timestamp': datetime.utcnow().isoformat()})
        
        return self._get_mission_summary()
    
    async def _decide_next_action(self) -> Dict[str, Any]:
        """Use reasoning engine to decide next action."""
        return {
            'action': 'monitor',
            'priority': 'normal',
            'estimated_energy_wh': 0.5
        }
    
    async def _execute_action(self, action: Dict[str, Any]) -> None:
        """Execute planned action."""
        await asyncio.sleep(0.1)
        self.energy_remaining -= action.get('estimated_energy_wh', 0.1)
        self.mission_log.append({
            'action': action,
            'timestamp': datetime.utcnow().isoformat(),
            'energy_remaining': self.energy_remaining
        })
    
    async def _enter_low_power_mode(self) -> None:
        """Reduce power consumption."""
        self.mission_log.append({
            'event': 'low_power_mode_activated',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    async def _checkpoint_state(self) -> None:
        """Save state for recovery."""
        checkpoint = {
            'cycle': len(self.mission_log),
            'energy': self.energy_remaining,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.mission_log.append({'checkpoint': checkpoint})
    
    async def _graceful_shutdown(self) -> None:
        """Shutdown gracefully."""
        self.state = AgentState.SHUTDOWN
        self.mission_log.append({
            'event': 'graceful_shutdown',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def _get_mission_summary(self) -> Dict[str, Any]:
        """Get mission summary."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds() / 3600
        return {
            'agent_id': self.config.agent_id,
            'status': self.state.value,
            'uptime_hours': uptime,
            'energy_remaining': self.energy_remaining,
            'log_entries': len(self.mission_log),
            'success': self.state != AgentState.ERROR
        }
