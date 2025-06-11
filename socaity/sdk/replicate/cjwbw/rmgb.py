from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class rmgb(FastSDK):
    """
    Generated client for rmgb
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="56ced991-c449-4341-9e7c-3cd5f7e4aac0", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     