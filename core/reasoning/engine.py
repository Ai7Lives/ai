from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

@dataclass
class ReasoningStep:
    """Single step in reasoning trace."""
    observation: str
    rule: str
    conclusion: str
    confidence: float = 1.0
    proof_id: Optional[str] = None

class ExplainableReasoner:
    """Neurosymbolic reasoner with explainable traces."""
    
    def __init__(self, rules: Dict[str, Any] = None):
        self.rules = rules or self._default_rules()
        self.reasoning_history = []
    
    def reason(self, observation: str, context: Dict[str, Any] = None) -> List[ReasoningStep]:
        """Generate explainable reasoning trace."""
        steps = []
        context = context or {}
        
        # Initial observation
        steps.append(ReasoningStep(
            observation=observation,
            rule='observation_axiom',
            conclusion=observation
        ))
        
        # Apply rules
        for rule_name, rule_logic in self.rules.items():
            if self._rule_applies(rule_name, observation, context):
                conclusion = rule_logic.get('conclusion', observation)
                confidence = rule_logic.get('confidence', 0.8)
                
                steps.append(ReasoningStep(
                    observation=observation,
                    rule=rule_name,
                    conclusion=conclusion,
                    confidence=confidence
                ))
        
        self.reasoning_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'observation': observation,
            'steps': [asdict(s) for s in steps]
        })
        
        return steps
    
    def _rule_applies(self, rule_name: str, observation: str, context: Dict) -> bool:
        """Check if rule applies to current observation."""
        rule = self.rules.get(rule_name, {})
        preconditions = rule.get('preconditions', [])
        
        for precond in preconditions:
            if precond not in observation and precond not in str(context):
                return False
        
        return True
    
    def _default_rules(self) -> Dict[str, Any]:
        """Default reasoning rules."""
        return {
            'energy_conservation': {
                'preconditions': ['energy', 'charge'],
                'conclusion': 'Energy budget updated',
                'confidence': 0.95
            },
            'thermal_management': {
                'preconditions': ['temperature', 'heat'],
                'conclusion': 'Thermal management activated',
                'confidence': 0.9
            },
            'safety_first': {
                'preconditions': ['safety', 'risk'],
                'conclusion': 'Safety protocol engaged',
                'confidence': 0.99
            }
        }
    
    def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Return reasoning history."""
        return self.reasoning_history.copy()
