from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class latent_sr(FastSDK):
    """
    Generated client for latent_sr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="da7f014d-265e-4a32-8d3f-66022df896d5", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], up_f: int = 4, steps: int = 100, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image
            
            up_f: Upscale factor Defaults to 4.
            
            steps: Sampling steps Defaults to 100.
            
        """
        return self.submit_job("/predict", image=image, up_f=up_f, steps=steps, **kwargs)
     