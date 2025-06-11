from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_esrgan(FastSDK):
    """
    Generated client for real_esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0e542d35-0014-45bb-925d-404b56f2b9d2", api_key=api_key)
    
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
        return self.submit_job("/predict", image=image, scale=scale, face_enhance=face_enhance, **kwargs)
     