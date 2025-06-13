from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class addwatermark(FastSDK):
    """
    Generated client for charlesmccarthy/addwatermark
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1f2e4a2e-b421-4a6e-8021-79ffb4fca4b3", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], size: int = 40, watermark: str = 'FULLJOURNEY.AI', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            size: Size of font Defaults to 40.
            
            watermark: Watermark Text Defaults to 'FULLJOURNEY.AI'.
            
        """
        return self.submit_job("/predictions", video=video, size=size, watermark=watermark, **kwargs)
     