from typing import Dict, Any, List, Optional
from enum import Enum
import json

class PolicyLevel(Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

class PolicyEngine:
    """Policy-aware decision making."""
    
    def __init__(self):
        self.policies: Dict[str, Dict[str, Any]] = {}
        self.violations: List[Dict[str, Any]] = []
    
    def register_policy(self, policy_name: str, rules: Dict[str, Any], level: PolicyLevel = PolicyLevel.MEDIUM) -> None:
        """Register a named policy."""
        self.policies[policy_name] = {
            'rules': rules,
            'level': level,
            'violations': 0
        }
    
    def check_compliance(self, action: str, context: Dict[str, Any], policy_name: str) -> tuple[bool, Optional[str]]:
        """Check if action complies with policy."""
        if policy_name not in self.policies:
            return True, None  # No policy, allow
        
        policy = self.policies[policy_name]
        rules = policy['rules']
        
        # Check forbidden actions
        if 'forbidden_actions' in rules:
            if action in rules['forbidden_actions']:
                violation_msg = f"Action '{action}' forbidden by {policy_name}"
                self._record_violation(policy_name, violation_msg, PolicyLevel.CRITICAL)
                return False, violation_msg
        
        # Check required context
        if 'required_context' in rules:
            for req in rules['required_context']:
                if req not in context or context[req] is None:
                    violation_msg = f"Missing required context: {req}"
                    self._record_violation(policy_name, violation_msg, policy['level'])
                    return False, violation_msg
        
        # Check constraints
        if 'constraints' in rules:
            for constraint_name, constraint_func in rules['constraints'].items():
                if callable(constraint_func):
                    if not constraint_func(context):
                        violation_msg = f"Constraint violation: {constraint_name}"
                        self._record_violation(policy_name, violation_msg, policy['level'])
                        return False, violation_msg
        
        return True, None
    
    def _record_violation(self, policy_name: str, message: str, level: PolicyLevel) -> None:
        """Record policy violation."""
        self.violations.append({
            'policy': policy_name,
            'message': message,
            'level': level.value,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        })
        self.policies[policy_name]['violations'] += 1
    
    def get_violations(self) -> List[Dict[str, Any]]:
        """Get violation history."""
        return self.violations.copy()
    
    def get_policy_stats(self) -> Dict[str, Any]:
        """Get policy statistics."""
        return {
            'total_policies': len(self.policies),
            'total_violations': len(self.violations),
            'policy_details': {name: {'violations': p['violations'], 'level': p['level'].value} 
                             for name, p in self.policies.items()}
        }
