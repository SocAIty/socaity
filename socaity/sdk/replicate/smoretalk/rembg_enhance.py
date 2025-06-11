from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class rembg_enhance(FastSDK):
    """
    Generated client for rembg_enhance
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="37d4c095-5d53-4de9-a39a-e28aec7858f4", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     