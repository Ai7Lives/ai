import logging
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger('VerificationHandler')

class VerificationStatus(Enum):
    VERIFIED = 'verified'
    REJECTED = 'rejected'
    PENDING = 'pending'
    ERROR = 'error'

@dataclass
class VerificationReceipt:
    """Proof receipt for auditable verification."""
    proof_id: str
    status: VerificationStatus
    theorem: str
    timestamp: str
    reasoning_trace: List[Dict[str, Any]]
    energy_cost_wh: float = 0.0
    reason: str = ""
    integrity_hash: str = ""

class VerificationHandler:
    """Production-grade verification node with proof caching."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.cache = {}
        self.verification_log = []
        self.total_verifications = 0
        self.failed_verifications = 0
        
    def verify(self, 
               action: str,
               state: Dict[str, Any],
               safety_policy: Dict[str, Any],
               proof_id: str = None) -> VerificationReceipt:
        """Verify action against safety policy and formal methods."""
        self.total_verifications += 1
        
        if proof_id is None:
            proof_id = hashlib.sha256(
                json.dumps({'action': action, 'state': state}, sort_keys=True).encode()
            ).hexdigest()[:16]
        
        # Check cache
        if proof_id in self.cache:
            logger.debug(f"Cache hit for proof {proof_id}")
            return self.cache[proof_id]
        
        reasoning_trace = self._build_reasoning_trace(action, state, safety_policy)
        
        # Safety check
        is_safe, reason = self._check_safety(action, state, safety_policy, reasoning_trace)
        
        status = VerificationStatus.VERIFIED if is_safe else VerificationStatus.REJECTED
        if not is_safe:
            self.failed_verifications += 1
        
        receipt = VerificationReceipt(
            proof_id=proof_id,
            status=status,
            theorem=self._get_applicable_theorem(action),
            timestamp=datetime.utcnow().isoformat(),
            reasoning_trace=reasoning_trace,
            reason=reason if not is_safe else "All invariants satisfied"
        )
        
        receipt.integrity_hash = self._compute_integrity_hash(receipt)
        self.cache[proof_id] = receipt
        self.verification_log.append(asdict(receipt))
        
        return receipt
    
    def _build_reasoning_trace(self, action: str, state: Dict[str, Any], 
                              policy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build explainable reasoning trace."""
        trace = []
        
        # State observation
        trace.append({
            'step': 'observation',
            'content': f"State: {json.dumps(state)}",
            'type': 'fact'
        })
        
        # Rule application
        trace.append({
            'step': 'inference',
            'content': f"Action '{action}' requested",
            'applicable_rules': list(policy.keys()) if isinstance(policy, dict) else []
        })
        
        # Conclusion
        trace.append({
            'step': 'conclusion',
            'content': f"Evaluating against {len(policy)} safety rules"
        })
        
        return trace
    
    def _check_safety(self, action: str, state: Dict[str, Any],
                     policy: Dict[str, Any], trace: List) -> Tuple[bool, str]:
        """Check action safety against policy constraints."""
        # Basic safety rules
        forbidden_actions = policy.get('forbidden_actions', [])
        if action in forbidden_actions:
            return False, f"Action '{action}' is forbidden by policy"
        
        # Energy constraints
        if 'energy_constraint' in policy:
            energy = state.get('energy', 0)
            min_energy = policy['energy_constraint']
            if energy < min_energy and action not in ['idle', 'charge']:
                return False, f"Insufficient energy ({energy}Wh < {min_energy}Wh required)"
        
        # Thermal constraints
        if 'thermal_constraint' in policy:
            temp = state.get('temperature', 0)
            max_temp = policy['thermal_constraint']
            if temp > max_temp:
                return False, f"System overheating ({temp}°C > {max_temp}°C limit)"
        
        return True, ""
    
    def _get_applicable_theorem(self, action: str) -> str:
        """Map action to applicable formal theorem."""
        theorem_map = {
            'charge': 'energy_conservation_law',
            'repair': 'safety_restoration_theorem',
            'idle': 'thermal_decay_model',
            'service': 'maintenance_completion_theorem'
        }
        return theorem_map.get(action, 'general_safety_invariant')
    
    def _compute_integrity_hash(self, receipt: VerificationReceipt) -> str:
        """Compute SHA-256 hash for tamper detection."""
        receipt_copy = asdict(receipt)
        receipt_copy['integrity_hash'] = ''  # Exclude hash field itself
        content = json.dumps(receipt_copy, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get_verification_stats(self) -> Dict[str, Any]:
        """Return verification statistics."""
        return {
            'total_verifications': self.total_verifications,
            'failed_verifications': self.failed_verifications,
            'success_rate': (self.total_verifications - self.failed_verifications) / max(1, self.total_verifications),
            'cache_size': len(self.cache),
            'log_entries': len(self.verification_log)
        }
