from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class merge_img(FastSDK):
    """
    Generated client for lucataco/merge-img
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="81ac2500-951a-40f0-bd75-ca22308ea8b2", api_key=api_key)
    
    def predictions(self, background: Optional[Union[str, MediaFile, bytes]] = None, foreground: Optional[Union[str, MediaFile, bytes]] = None, position_x: Optional[int] = None, position_y: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            background: JPG image to be used as background Optional.
            
            foreground: PNG image with transparency to be used as foreground Optional.
            
            position_x: X coordinate for foreground image position (optional, defaults to center) Optional.
            
            position_y: Y coordinate for foreground image position (optional, defaults to center) Optional.
            
        """
        return self.submit_job("/predictions", background=background, foreground=foreground, position_x=position_x, position_y=position_y, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions