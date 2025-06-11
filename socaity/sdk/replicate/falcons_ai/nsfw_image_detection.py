from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class nsfw_image_detection(FastSDK):
    """
    Generated client for nsfw_image_detection
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b25d339f-552a-4b0c-9110-4471690346e3", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predict", image=image, **kwargs)
     