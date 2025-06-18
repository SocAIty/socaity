from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class zero123plusplus(FastSDK):
    """
    Generated client for jd7h/zero123plusplus
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e54c61c8-e627-4ef8-b561-7680d07b7635", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], remove_background: bool = False, return_intermediate_images: bool = False, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image. Aspect ratio should be 1:1. Recommended resolution is >= 320x320 pixels.
            
            remove_background: Remove the background of the input image Defaults to False.
            
            return_intermediate_images: Return the intermediate images together with the output images Defaults to False.
            
        """
        return self.submit_job("/predictions", image=image, remove_background=remove_background, return_intermediate_images=return_intermediate_images, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions