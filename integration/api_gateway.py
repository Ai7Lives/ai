from typing import Dict, Any, Optional, List, Callable
from pydantic import BaseModel
import uuid
from datetime import datetime

class APIRequest(BaseModel):
    """Unified API request format."""
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    payload: Dict[str, Any]

class APIGateway:
    """Universal API gateway for unified system access."""
    
    def __init__(self):
        self.routing_rules: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, int] = {}
        self.auth_tokens: set = set()
        self.api_calls: List[Dict[str, Any]] = []
        self.middleware: List[Callable] = []
    
    def register_endpoint(self, path: str, handler: Callable, methods: List[str] = None) -> None:
        """Register API endpoint."""
        methods = methods or ['GET', 'POST']
        self.routing_rules[path] = {
            'handler': handler,
            'methods': methods
        }
    
    def set_rate_limit(self, endpoint: str, requests_per_minute: int) -> None:
        """Set rate limit for endpoint."""
        self.rate_limits[endpoint] = requests_per_minute
    
    def add_middleware(self, middleware: Callable) -> None:
        """Add request middleware."""
        self.middleware.append(middleware)
    
    def authenticate(self, token: str) -> bool:
        """Validate API token."""
        return token in self.auth_tokens
    
    def issue_token(self, client_id: str) -> str:
        """Issue API token."""
        token = f"{client_id}_{uuid.uuid4().hex}"
        self.auth_tokens.add(token)
        return token
    
    def revoke_token(self, token: str) -> bool:
        """Revoke API token."""
        if token in self.auth_tokens:
            self.auth_tokens.discard(token)
            return True
        return False
    
    def route_request(self, request: APIRequest, token: str) -> Dict[str, Any]:
        """Route unified API request."""
        call_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': request.action,
            'entity_type': request.entity_type,
            'status': 'unknown'
        }
        
        # Authentication
        if not self.authenticate(token):
            call_record['status'] = 'unauthorized'
            self.api_calls.append(call_record)
            return {'error': 'Unauthorized', 'code': 401}
        
        # Apply middleware
        for middleware in self.middleware:
            result = middleware(request)
            if result.get('blocked'):
                call_record['status'] = 'blocked_by_middleware'
                self.api_calls.append(call_record)
                return result
        
        # Route to handler
        path = f"/{request.entity_type}/{request.action}"
        if path not in self.routing_rules:
            call_record['status'] = 'not_found'
            self.api_calls.append(call_record)
            return {'error': f'Endpoint {path} not found', 'code': 404}
        
        handler = self.routing_rules[path]['handler']
        try:
            result = handler(request.payload)
            call_record['status'] = 'success'
            self.api_calls.append(call_record)
            return result
        except Exception as e:
            call_record['status'] = 'error'
            call_record['error'] = str(e)
            self.api_calls.append(call_record)
            return {'error': str(e), 'code': 500}
    
    def get_gateway_status(self) -> Dict[str, Any]:
        """Get API gateway status."""
        successful_calls = sum(1 for c in self.api_calls if c.get('status') == 'success')
        failed_calls = sum(1 for c in self.api_calls if c.get('status') in ['error', 'not_found'])
        
        return {
            'registered_endpoints': len(self.routing_rules),
            'authenticated_clients': len(self.auth_tokens),
            'total_calls': len(self.api_calls),
            'successful_calls': successful_calls,
            'failed_calls': failed_calls,
            'rate_limits': dict(self.rate_limits)
        }
