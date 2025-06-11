from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class modnet(FastSDK):
    """
    Generated client for modnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="65e3d24c-cc08-41b5-af67-e4db9869c82d", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     