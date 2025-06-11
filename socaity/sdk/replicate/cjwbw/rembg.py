from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class rembg(FastSDK):
    """
    Generated client for rembg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5371ee90-acad-4499-b57d-4aba7aa3ed57", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes] = '', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image Defaults to ''.
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     