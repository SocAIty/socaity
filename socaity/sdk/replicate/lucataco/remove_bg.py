from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class remove_bg(FastSDK):
    """
    Generated client for lucataco/remove-bg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0e93b975-3d4b-4ca3-83d1-cc3ea243e443", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Remove background from this image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
     