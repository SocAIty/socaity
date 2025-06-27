from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class esrgan(FastSDK):
    """
    Generated client for xinntao/esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="cef8d20a-b136-4564-b551-74d7ee336de4", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Low-resolution input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions