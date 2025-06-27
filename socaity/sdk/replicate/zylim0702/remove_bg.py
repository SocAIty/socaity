from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class remove_bg(FastSDK):
    """
    Generated client for zylim0702/remove-bg
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e9d43ee2-ccfe-4282-91c3-00f15b75248b", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions