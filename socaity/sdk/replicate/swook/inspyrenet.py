from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class inspyrenet(FastSDK):
    """
    Generated client for swook/inspyrenet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="53b61825-79f2-4503-bfd0-a5538c7d3610", api_key=api_key)
    
    def predict(self, image_path: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_path: RGB input image
            
        """
        return self.submit_job("/predictions", image_path=image_path, **kwargs)
     