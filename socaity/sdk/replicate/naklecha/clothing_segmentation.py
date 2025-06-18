from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class clothing_segmentation(FastSDK):
    """
    Generated client for naklecha/clothing-segmentation
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bb3f71e6-4cfa-4d75-a39c-ad86f5816ef2", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], clothing: str = 'topwear', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image to in-paint. The image will be center cropped and resized to size 512*512.
            
            clothing: This value should be one of the following - [topwear, bottomwear] Defaults to 'topwear'.
            
        """
        return self.submit_job("/predictions", image=image, clothing=clothing, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions