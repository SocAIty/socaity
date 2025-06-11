from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class birefnet(FastSDK):
    """
    Generated client for birefnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="29c8c9fa-af60-4a7b-92be-a6b9c9d4c5f6", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], resolution: str = '', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            resolution: Resolution in WxH format, e.g., '1024x1024' Defaults to ''.
            
        """
        return self.submit_job("/predict", image=image, resolution=resolution, **kwargs)
     