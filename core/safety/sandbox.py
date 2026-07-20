from typing import Any, Callable, Dict
import sys
import io

class Sandbox:
    """Execution sandbox for untrusted code."""
    
    def __init__(self, timeout_seconds: float = 5.0, memory_limit_mb: int = 100):
        self.timeout = timeout_seconds
        self.memory_limit = memory_limit_mb
        self.restricted_builtins = {
            '__import__': None,
            'open': None,
            'exec': None,
            'eval': None
        }
    
    def execute_safely(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with restrictions."""
        # Capture output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Execute with timeout
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function execution exceeded {self.timeout}s timeout")
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(self.timeout))
            
            result = func(*args, **kwargs)
            
            signal.alarm(0)  # Cancel alarm
            return result
        
        except TimeoutError as e:
            return {'error': str(e), 'status': 'timeout'}
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
