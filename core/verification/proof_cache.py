import hashlib
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class CachedProof:
    proof_id: str
    content: str
    timestamp: float
    ttl_seconds: float = 3600  # 1 hour default TTL
    access_count: int = 0
    
    def is_valid(self) -> bool:
        return (time.time() - self.timestamp) < self.ttl_seconds

class ProofCache:
    """LRU cache for proof verification results."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, CachedProof] = {}
        self.access_order = []
    
    def get(self, proof_id: str) -> Optional[str]:
        """Retrieve cached proof if valid."""
        if proof_id not in self.cache:
            return None
        
        proof = self.cache[proof_id]
        if not proof.is_valid():
            del self.cache[proof_id]
            self.access_order.remove(proof_id)
            return None
        
        proof.access_count += 1
        self.access_order.remove(proof_id)
        self.access_order.append(proof_id)
        return proof.content
    
    def set(self, proof_id: str, content: str, ttl_seconds: float = 3600) -> None:
        """Cache a proof with TTL."""
        if len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        proof = CachedProof(
            proof_id=proof_id,
            content=content,
            timestamp=time.time(),
            ttl_seconds=ttl_seconds
        )
        self.cache[proof_id] = proof
        self.access_order.append(proof_id)
    
    def is_valid(self, proof_id: str) -> bool:
        """Check if proof is cached and valid."""
        if proof_id not in self.cache:
            return False
        return self.cache[proof_id].is_valid()
    
    def clear(self) -> None:
        """Clear entire cache."""
        self.cache.clear()
        self.access_order.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Cache statistics."""
        return {
            'entries': len(self.cache),
            'max_size': self.max_size,
            'utilization': len(self.cache) / self.max_size
        }
