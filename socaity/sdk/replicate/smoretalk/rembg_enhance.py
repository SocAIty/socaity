from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class rembg_enhance(FastSDK):
    """
    Generated client for smoretalk/rembg-enhance
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1c92d5ca-dab3-4bca-9a54-c361ff454fa0", api_key=api_key)
    
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