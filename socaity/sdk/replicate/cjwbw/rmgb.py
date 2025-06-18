from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class rmgb(FastSDK):
    """
    Generated client for cjwbw/rmgb
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2cde0481-d448-4332-a3c6-4759c60c2253", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions