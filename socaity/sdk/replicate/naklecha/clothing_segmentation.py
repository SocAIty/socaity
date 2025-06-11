from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class clothing_segmentation(FastSDK):
    """
    Generated client for clothing_segmentation
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fa272a57-1781-41ed-9cd9-0a4ca46426a7", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], clothing: str = 'topwear', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image to in-paint. The image will be center cropped and resized to size 512*512.
            
            clothing: This value should be one of the following - [topwear, bottomwear] Defaults to 'topwear'.
            
        """
        return self.submit_job("/predict", image=image, clothing=clothing, **kwargs)
     