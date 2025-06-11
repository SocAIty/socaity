from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class background_remover(FastSDK):
    """
    Generated client for background_remover
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a69ebba9-516c-4401-b01f-5a42e8f8c041", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     