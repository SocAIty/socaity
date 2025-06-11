from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class animesr(FastSDK):
    """
    Generated client for animesr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="45b93c4d-9208-4d92-80c5-dfc2d6b0f130", api_key=api_key)
    
    def predict(self, video: Optional[Union[MediaFile, str, bytes]] = None, frames: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video file Optional.
            
            frames: Zip file of frames of a video. Ignored when video is provided. Optional.
            
        """
        return self.submit_job("/predict", video=video, frames=frames, **kwargs)
     