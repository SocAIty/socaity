from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class rembg(FastSDK):
    """
    Generated client for cjwbw/rembg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bd65f429-81ef-432d-a9b6-fcfcd2982bba", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes] = '', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image Defaults to ''.
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions