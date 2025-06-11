from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class addwatermark(FastSDK):
    """
    Generated client for addwatermark
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="07cb82a5-6fcc-4a7e-9179-0dcde62bbb3e", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], size: int = 40, watermark: str = 'FULLJOURNEY.AI', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            size: Size of font Defaults to 40.
            
            watermark: Watermark Text Defaults to 'FULLJOURNEY.AI'.
            
        """
        return self.submit_job("/predict", video=video, size=size, watermark=watermark, **kwargs)
     