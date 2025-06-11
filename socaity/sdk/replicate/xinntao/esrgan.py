from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class esrgan(FastSDK):
    """
    Generated client for esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d3899772-7898-413f-8573-deadf0edd465", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Low-resolution input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     