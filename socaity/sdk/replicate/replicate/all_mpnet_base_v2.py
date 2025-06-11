from fastsdk.fastSDK import FastSDK
from typing import Optional


class all_mpnet_base_v2(FastSDK):
    """
    Generated client for all_mpnet_base_v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="aba74c83-5c58-4dc1-80f1-709b8b42ad9b", api_key=api_key)
    
    def predict(self, text: Optional[str] = None, text_batch: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: A single string to encode. Optional.
            
            text_batch: A JSON-formatted list of strings to encode. Optional.
            
        """
        return self.submit_job("/predict", text=text, text_batch=text_batch, **kwargs)
     