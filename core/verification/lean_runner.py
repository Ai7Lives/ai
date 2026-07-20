import subprocess
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger('LeanRunner')

@dataclass
class LeanProofResult:
    theorem: str
    success: bool
    output: str = ""
    error: str = ""
    proof_time_ms: float = 0.0

class LeanRunner:
    """Interface to Lean 4 formal verification."""
    
    def __init__(self, lean_path: str = "lean"):
        self.lean_path = lean_path
        self.verified_theorems = set()
    
    def verify_theorem(self, theorem_name: str, proof_file: str) -> LeanProofResult:
        """Verify a Lean theorem."""
        try:
            cmd = [self.lean_path, proof_file]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            if success:
                self.verified_theorems.add(theorem_name)
            
            return LeanProofResult(
                theorem=theorem_name,
                success=success,
                output=result.stdout,
                error=result.stderr if not success else ""
            )
        except subprocess.TimeoutExpired:
            return LeanProofResult(
                theorem=theorem_name,
                success=False,
                error="Proof verification timed out (>30s)"
            )
        except Exception as e:
            logger.error(f"Error verifying {theorem_name}: {e}")
            return LeanProofResult(
                theorem=theorem_name,
                success=False,
                error=str(e)
            )
    
    def verify_invariant(self, invariant: str) -> bool:
        """Quick check if invariant has been proven."""
        return invariant in self.verified_theorems
    
    def get_verified_theorems(self) -> set:
        """Return set of verified theorems."""
        return self.verified_theorems.copy()
