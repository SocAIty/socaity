from fastsdk import FastClient, APISeex
from typing import Optional, Dict, List, Any


class o1_mini(FastClient):
    """
    Generated client based on openai/o1-mini format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9db9fcb1-d35e-4f4e-9130-b55681d04fcc", api_key=api_key)
    
    def predictions(self, messages: List[Dict[str, Any]] = [], max_completion_tokens: int = 4096, prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            messages: A JSON string representing a list of messages. For example: [{"role": "user", "content": "Hello, how are you?"}]. If provided, prompt and system_prompt are ignored. Defaults to [].
            
            max_completion_tokens: Maximum number of completion tokens to generate Defaults to 4096.
            
            prompt: The prompt to send to the model. Do not use if using messages. Optional.
            
        """
        return self.submit_job("/predictions", messages=messages, max_completion_tokens=max_completion_tokens, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
