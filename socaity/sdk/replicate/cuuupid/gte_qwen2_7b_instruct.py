from fastsdk.fastSDK import FastSDK
from typing import Union, List, Any


class gte_qwen2_7b_instruct(FastSDK):
    """
    Generated client for cuuupid/gte-qwen2-7b-instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c704672f-cd24-4875-aa3f-300e0639e0f2", api_key=api_key)
    
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
        return self.submit_job("/predictions", text=text, **kwargs)
     