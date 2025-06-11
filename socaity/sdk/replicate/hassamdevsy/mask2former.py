from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class mask2former(FastSDK):
    """
    Generated client for mask2former
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6a65c454-cbfd-41d3-a746-a6d9dba39f28", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     