from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class remove_bg(FastSDK):
    """
    Generated client for remove_bg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a58d7993-36f7-497f-8f73-e28b4d13024e", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Remove background from this image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     