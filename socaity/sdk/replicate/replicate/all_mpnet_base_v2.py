from fastsdk import FastSDK, APISeex
from typing import Optional


class all_mpnet_base_v2(FastSDK):
    """
    Generated client for replicate/all-mpnet-base-v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7dd22be5-46d1-45cb-b217-e0d691806529", api_key=api_key)
    
    def predictions(self, text: Optional[str] = None, text_batch: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            text: A single string to encode. Optional.
            
            text_batch: A JSON-formatted list of strings to encode. Optional.
            
        """
        return self.submit_job("/predictions", text=text, text_batch=text_batch, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions