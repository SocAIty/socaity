from fastsdk import FastSDK, APISeex
from typing import Optional


class o1_mini(FastSDK):
    """
    Generated client for openai/o1-mini
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9db9fcb1-d35e-4f4e-9130-b55681d04fcc", api_key=api_key)
    
    def predictions(self, max_completion_tokens: int = 4096, prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            max_completion_tokens: Maximum number of completion tokens to generate Defaults to 4096.
            
            prompt: The prompt to send to the model. Do not use if using messages. Optional.
            
        """
        return self.submit_job("/predictions", max_completion_tokens=max_completion_tokens, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions