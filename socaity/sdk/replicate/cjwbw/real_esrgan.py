from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_esrgan(FastSDK):
    """
    Generated client for real_esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="02c7dd0e-1a48-4f57-9a18-6b1c04ebeb49", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], upscale: int = 4, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            upscale: Upscaling factor Defaults to 4.
            
        """
        return self.submit_job("/predict", image=image, upscale=upscale, **kwargs)
     