from fastsdk import FastSDK, APISeex
from typing import List, Any, Union


class gte_qwen2_7b_instruct(FastSDK):
    """
    Generated client for cuuupid/gte-qwen2-7b-instruct
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c704672f-cd24-4875-aa3f-300e0639e0f2", api_key=api_key)
    
    def predictions(self, text: Union[str, List[Any]], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Texts to embed
            
        """
        return self.submit_job("/predictions", text=text, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions