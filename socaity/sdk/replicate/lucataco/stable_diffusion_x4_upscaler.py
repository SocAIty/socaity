from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class stable_diffusion_x4_upscaler(FastSDK):
    """
    Generated client for lucataco/stable-diffusion-x4-upscaler
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2a64befb-cd6c-46d1-a751-91599ac9ea11", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], scale: int = 4, prompt: str = 'A white cat', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Grayscale input image
            
            scale: Factor to scale image by Defaults to 4.
            
            prompt: Input prompt Defaults to 'A white cat'.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions