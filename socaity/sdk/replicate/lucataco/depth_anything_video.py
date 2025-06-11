from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class depth_anything_video(FastSDK):
    """
    Generated client for depth_anything_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d63ab11a-a4a2-4359-adcc-47dec778c151", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], encoder: str = 'vits', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            encoder: Model type Defaults to 'vits'.
            
        """
        return self.submit_job("/predict", video=video, encoder=encoder, **kwargs)
     