from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class SystemAdapter:
    """External system adapter."""
    system_name: str
    adapter_type: str
    transform_func: Callable
    reverse_transform_func: Callable

class IntegrationHub:
    """Central hub for system integration across industries."""
    
    def __init__(self):
        self.adapters: Dict[str, SystemAdapter] = {}
        self.data_flows: List[Dict[str, Any]] = []
        self.unified_schema: Dict[str, Any] = self._init_unified_schema()
        self.integration_log: List[Dict[str, Any]] = []
    
    def register_adapter(self, adapter: SystemAdapter) -> bool:
        """Register system adapter."""
        self.adapters[adapter.system_name] = adapter
        self.integration_log.append({
            'event': 'adapter_registered',
            'system': adapter.system_name,
            'type': adapter.adapter_type,
            'timestamp': datetime.utcnow().isoformat()
        })
        return True
    
    def normalize_data(self, system_name: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize external system data to unified schema."""
        if system_name not in self.adapters:
            return raw_data
        
        adapter = self.adapters[system_name]
        try:
            normalized = adapter.transform_func(raw_data)
            
            self.data_flows.append({
                'source': system_name,
                'timestamp': datetime.utcnow().isoformat(),
                'record_count': 1,
                'status': 'success'
            })
            
            return normalized
        except Exception as e:
            self.data_flows.append({
                'source': system_name,
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e),
                'status': 'error'
            })
            return {}
    
    def denormalize_data(self, system_name: str, unified_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert from unified schema to external system format."""
        if system_name not in self.adapters:
            return unified_data
        
        adapter = self.adapters[system_name]
        return adapter.reverse_transform_func(unified_data)
    
    def _init_unified_schema(self) -> Dict[str, Any]:
        """Initialize universal data schema."""
        return {
            'entity_type': None,
            'entity_id': None,
            'attributes': {},
            'relationships': [],
            'metadata': {
                'source_system': None,
                'timestamp': None,
                'version': '1.0'
            }
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status."""
        successful_flows = sum(1 for f in self.data_flows if f.get('status') == 'success')
        failed_flows = sum(1 for f in self.data_flows if f.get('status') == 'error')
        
        return {
            'registered_systems': len(self.adapters),
            'total_data_flows': len(self.data_flows),
            'successful_flows': successful_flows,
            'failed_flows': failed_flows,
            'systems': list(self.adapters.keys())
        }
