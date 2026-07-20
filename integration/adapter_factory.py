from typing import Dict, Any, Callable, Optional
from .integration_hub import SystemAdapter
import json

class AdapterFactory:
    """Factory for creating system adapters."""
    
    _adapter_templates = {
        'REST_API': {
            'transform': lambda data: {**data, 'source': 'REST', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        },
        'DATABASE': {
            'transform': lambda data: {**data, 'source': 'DATABASE', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        },
        'MESSAGE_QUEUE': {
            'transform': lambda data: {**data, 'source': 'QUEUE', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        },
        'FILE_SYSTEM': {
            'transform': lambda data: {**data, 'source': 'FILE', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        },
        'LEGACY_EDI': {
            'transform': lambda data: {**data, 'source': 'EDI', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        },
        'STREAMING': {
            'transform': lambda data: {**data, 'source': 'STREAM', 'normalized': True},
            'reverse': lambda data: {k: v for k, v in data.items() if k not in ['source', 'normalized']}
        }
    }
    
    @classmethod
    def create_adapter(cls, system_name: str, adapter_type: str,
                      custom_transform: Optional[Callable] = None,
                      custom_reverse: Optional[Callable] = None) -> SystemAdapter:
        """Create adapter for system."""
        if adapter_type not in cls._adapter_templates:
            raise ValueError(f"Unknown adapter type: {adapter_type}")
        
        template = cls._adapter_templates[adapter_type]
        transform_func = custom_transform or template['transform']
        reverse_func = custom_reverse or template['reverse']
        
        return SystemAdapter(
            system_name=system_name,
            adapter_type=adapter_type,
            transform_func=transform_func,
            reverse_transform_func=reverse_func
        )
    
    @classmethod
    def list_available_adapters(cls) -> Dict[str, str]:
        """List available adapter types."""
        return {name: f"Adapter for {name}" for name in cls._adapter_templates.keys()}
