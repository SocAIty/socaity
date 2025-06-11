from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class aura_sr(FastSDK):
    """
    Generated client for aura_sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="caf57c89-14d2-45e4-b7ea-25ac0c48a22c", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], scale_factor: int = 4, max_batch_size: int = 1, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: The input image file to be upscaled.
            
            scale_factor: The factor by which to upscale the image (2, 4, 8, 16, or 32). Defaults to 4.
            
            max_batch_size: Controls the number of image tiles processed simultaneously. Higher values may increase speed but require more GPU memory. Lower values use less memory but may increase processing time. Default is 1 for broad compatibility. Adjust based on your GPU capabilities for optimal performance. Defaults to 1.
            
        """
        return self.submit_job("/predict", image=image, scale_factor=scale_factor, max_batch_size=max_batch_size, **kwargs)
     