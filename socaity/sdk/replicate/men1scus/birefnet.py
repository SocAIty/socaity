from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class birefnet(FastSDK):
    """
    Generated client for men1scus/birefnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="08229d1e-901a-45bb-97e5-6291fe34fd3d", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], resolution: str = '', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            resolution: Resolution in WxH format, e.g., '1024x1024' Defaults to ''.
            
        """
        return self.submit_job("/predictions", image=image, resolution=resolution, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions