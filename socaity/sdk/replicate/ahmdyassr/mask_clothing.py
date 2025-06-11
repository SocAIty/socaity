from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class mask_clothing(FastSDK):
    """
    Generated client for mask_clothing
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0bc54aae-e507-4695-bd92-d53780b79d13", api_key=api_key)
    
    def predict(self, face_mask: bool = False, adjustment: int = 0, face_adjustment: int = 0, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            face_mask: Mask face found in this image? Defaults to False.
            
            adjustment: Mask adjustment Defaults to 0.
            
            face_adjustment: Face mask adjustment Defaults to 0.
            
            image: Mask clothing found in this image Optional.
            
        """
        return self.submit_job("/predict", face_mask=face_mask, adjustment=adjustment, face_adjustment=face_adjustment, image=image, **kwargs)
     