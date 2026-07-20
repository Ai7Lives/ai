from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class ProofStep:
    """Proof derivation step."""
    fact: str
    rule: str
    derived: str
    justification: str = ""

class SymbolicReasoner:
    """Logic-based symbolic reasoner."""
    
    def __init__(self):
        self.knowledge_base = {}
        self.inference_rules = self._setup_rules()
    
    def assert_fact(self, fact: str, category: str = 'general') -> None:
        """Add fact to knowledge base."""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = []
        self.knowledge_base[category].append(fact)
    
    def infer(self, facts: Dict[str, Any]) -> List[ProofStep]:
        """Derive conclusions from facts using inference rules."""
        proof = []
        
        for rule_name, rule_logic in self.inference_rules.items():
            antecedents = rule_logic['antecedents']
            consequent = rule_logic['consequent']
            
            # Check if all antecedents are satisfied
            if all(self._fact_exists(ant, facts) for ant in antecedents):
                proof.append(ProofStep(
                    fact=json.dumps(facts),
                    rule=rule_name,
                    derived=consequent,
                    justification=f"By {rule_name} from {antecedents}"
                ))
        
        return proof
    
    def _fact_exists(self, fact_pattern: str, facts: Dict) -> bool:
        """Check if fact pattern matches known facts."""
        for key, value in facts.items():
            if fact_pattern.lower() in str(key).lower() or \
               fact_pattern.lower() in str(value).lower():
                return True
        return False
    
    def _setup_rules(self) -> Dict[str, Dict[str, Any]]:
        """Setup inference rules."""
        return {
            'maintenance_rule': {
                'antecedents': ['rover', 'damage', 'energy'],
                'consequent': 'Initiate maintenance protocol'
            },
            'power_conservation': {
                'antecedents': ['low_energy', 'sunlight'],
                'consequent': 'Redirect power to charging'
            },
            'safety_override': {
                'antecedents': ['critical_risk', 'safety'],
                'consequent': 'Execute emergency shutdown'
            }
        }
