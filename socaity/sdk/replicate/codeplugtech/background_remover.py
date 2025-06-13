from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class background_remover(FastSDK):
    """
    Generated client for codeplugtech/background-remover
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ac005f5c-17c4-4693-a642-24824565c896", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
     