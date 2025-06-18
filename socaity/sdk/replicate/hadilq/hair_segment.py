from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class hair_segment(FastSDK):
    """
    Generated client for hadilq/hair-segment
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="50f5a01a-d6e4-4338-ba86-a99c6d26ebdb", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image of a dragon, or notdragon:
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions