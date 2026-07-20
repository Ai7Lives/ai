from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class SovereigntyModel(Enum):
    """Sovereignty models."""
    NATIONAL = 'national'
    ENTERPRISE = 'enterprise'
    PRIVATE = 'private'

@dataclass
class SovereignCloudConfig:
    """Sovereign cloud configuration."""
    sovereignty_model: SovereigntyModel
    jurisdiction: str
    data_residency_required: bool
    encryption_standard: str
    audit_enabled: bool
    compliance_frameworks: List[str]

class SovereignCloud:
    """Air-gapped, sovereign compute infrastructure."""
    
    def __init__(self, config: SovereignCloudConfig):
        self.config = config
        self.nodes: Dict[str, Any] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.data_store = {}
    
    def validate_sovereignty(self, data: Dict[str, Any]) -> bool:
        """Validate data residency requirements."""
        if self.config.data_residency_required:
            # Check data origin matches jurisdiction
            return data.get('origin_jurisdiction') == self.config.jurisdiction
        return True
    
    def register_node(self, node_id: str, location: str, jurisdiction: str) -> bool:
        """Register compute node in sovereign cloud."""
        if self.config.data_residency_required and jurisdiction != self.config.jurisdiction:
            return False
        
        self.nodes[node_id] = {
            'location': location,
            'jurisdiction': jurisdiction,
            'registered_at': __import__('datetime').datetime.utcnow().isoformat()
        }
        return True
    
    def audit_operation(self, operation: str, details: Dict[str, Any]) -> None:
        """Log operation for audit trail."""
        self.audit_log.append({
            'operation': operation,
            'details': details,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        })
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Check compliance with regulations."""
        return {
            'sovereignty_model': self.config.sovereignty_model.value,
            'jurisdiction': self.config.jurisdiction,
            'compliance_frameworks': self.config.compliance_frameworks,
            'audit_log_size': len(self.audit_log),
            'registered_nodes': len(self.nodes)
        }
