from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class hair_segment(FastSDK):
    """
    Generated client for hair_segment
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f43ee93d-642e-4d86-8c0f-123f7d86d238", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image of a dragon, or notdragon:
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     