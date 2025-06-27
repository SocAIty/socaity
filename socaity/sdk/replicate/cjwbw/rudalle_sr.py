from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class rudalle_sr(FastSDK):
    """
    Generated client for cjwbw/rudalle-sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ae44cda0-15db-4eee-be00-27a5b56446af", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], scale: int = 4, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            scale: Choose up-scaling factor Defaults to 4.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions