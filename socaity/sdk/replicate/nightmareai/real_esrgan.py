from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_esrgan(FastSDK):
    """
    Generated client for nightmareai/real-esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f002d550-9af6-4fe1-99f9-26f2bccbad1f", api_key=api_key)
    
    def ready(self, **kwargs):
        """
        None
        
        """
        return self.submit_job("/ready", **kwargs)
    
    def predict(self, image: Union[MediaFile, str, bytes], scale: float = 4.0, face_enhance: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            scale: Factor to scale image by Defaults to 4.0.
            
            face_enhance: Run GFPGAN face enhancement along with upscaling Defaults to False.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, face_enhance=face_enhance, **kwargs)
     