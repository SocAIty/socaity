from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class esrgan(FastSDK):
    """
    Generated client for xinntao/esrgan
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="cef8d20a-b136-4564-b551-74d7ee336de4", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Low-resolution input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
     