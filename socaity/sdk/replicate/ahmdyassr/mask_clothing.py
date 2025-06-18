from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class mask_clothing(FastSDK):
    """
    Generated client for ahmdyassr/mask-clothing
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="09115fc3-0100-42e0-b034-3480586c9990", api_key=api_key)
    
    def predictions(self, face_mask: bool = False, adjustment: int = 0, face_adjustment: int = 0, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            face_mask: Mask face found in this image? Defaults to False.
            
            adjustment: Mask adjustment Defaults to 0.
            
            face_adjustment: Face mask adjustment Defaults to 0.
            
            image: Mask clothing found in this image Optional.
            
        """
        return self.submit_job("/predictions", face_mask=face_mask, adjustment=adjustment, face_adjustment=face_adjustment, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions