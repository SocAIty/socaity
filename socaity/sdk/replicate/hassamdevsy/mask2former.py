from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class mask2former(FastSDK):
    """
    Generated client for hassamdevsy/mask2former
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="820f5706-634a-47e0-8412-011655f93527", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions