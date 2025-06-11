from fastsdk.fastSDK import FastSDK
from typing import List, Union, Any


class gte_qwen2_7b_instruct(FastSDK):
    """
    Generated client for gte_qwen2_7b_instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0ad20abd-f6fd-4e57-8e5e-508a025857f3", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, text: Union[List[Any], str], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Texts to embed
            
        """
        return self.submit_job("/predict", text=text, **kwargs)
     