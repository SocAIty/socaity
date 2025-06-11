from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class stable_diffusion_x4_upscaler(FastSDK):
    """
    Generated client for stable_diffusion_x4_upscaler
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="742c5532-1b3e-466b-b1fa-94d0f3c97140", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], scale: int = 4, prompt: str = 'A white cat', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Grayscale input image
            
            scale: Factor to scale image by Defaults to 4.
            
            prompt: Input prompt Defaults to 'A white cat'.
            
        """
        return self.submit_job("/predict", image=image, scale=scale, prompt=prompt, **kwargs)
     