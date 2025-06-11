from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class inspyrenet(FastSDK):
    """
    Generated client for inspyrenet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="60cf274d-5198-4c12-a9f9-08e21853005a", api_key=api_key)
    
    def predict(self, image_path: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_path: RGB input image
            
        """
        return self.submit_job("/predict", image_path=image_path, **kwargs)
     