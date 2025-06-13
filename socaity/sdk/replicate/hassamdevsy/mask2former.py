from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class mask2former(FastSDK):
    """
    Generated client for hassamdevsy/mask2former
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="820f5706-634a-47e0-8412-011655f93527", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
     