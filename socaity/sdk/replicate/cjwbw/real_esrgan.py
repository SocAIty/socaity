from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class real_esrgan(FastSDK):
    """
    Generated client for cjwbw/real-esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fd658ede-ab56-4be3-a1ca-9f458b5ee831", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], upscale: int = 4, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            upscale: Upscaling factor Defaults to 4.
            
        """
        return self.submit_job("/predictions", image=image, upscale=upscale, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions