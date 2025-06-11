from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class zero123plusplus(FastSDK):
    """
    Generated client for zero123plusplus
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6168d70e-d42c-492d-ac01-ec08fd8ba14e", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], remove_background: bool = False, return_intermediate_images: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image. Aspect ratio should be 1:1. Recommended resolution is >= 320x320 pixels.
            
            remove_background: Remove the background of the input image Defaults to False.
            
            return_intermediate_images: Return the intermediate images together with the output images Defaults to False.
            
        """
        return self.submit_job("/predict", image=image, remove_background=remove_background, return_intermediate_images=return_intermediate_images, **kwargs)
     