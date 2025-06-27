from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class remove_bg(FastSDK):
    """
    Generated client for lucataco/remove-bg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0e93b975-3d4b-4ca3-83d1-cc3ea243e443", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Remove background from this image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions