from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class modnet(FastSDK):
    """
    Generated client for pollinations/modnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9b5f38fa-b406-42e7-82b5-246613525bf1", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
     