from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class latent_sr(FastSDK):
    """
    Generated client for nightmareai/latent-sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3b68cf50-06e3-4b1c-b2bb-aa285d9663b1", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], up_f: int = 4, steps: int = 100, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Image
            
            up_f: Upscale factor Defaults to 4.
            
            steps: Sampling steps Defaults to 100.
            
        """
        return self.submit_job("/predictions", image=image, up_f=up_f, steps=steps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions