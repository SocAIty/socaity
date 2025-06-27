from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class hcflow_sr(FastSDK):
    """
    Generated client for jingyunliang/hcflow-sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="df7f6d61-85a1-44a9-a3f6-4f997f3da1d5", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], model_type: str = 'celeb', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Low resolution image
            
            model_type: celeb photo or general image Defaults to 'celeb'.
            
        """
        return self.submit_job("/predictions", image=image, model_type=model_type, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions