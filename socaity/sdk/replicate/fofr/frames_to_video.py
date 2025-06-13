from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class frames_to_video(FastSDK):
    """
    Generated client for fofr/frames-to-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e288c787-b473-4e4c-9eff-1073736a7c9b", api_key=api_key)
    
    def predict(self, fps: float = 24.0, frames_zip: Optional[Union[MediaFile, str, bytes]] = None, frames_urls: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            fps: Number of frames per second of video Defaults to 24.0.
            
            frames_zip: ZIP file containing frames Optional.
            
            frames_urls: Newline-separated URLs of frames to combine into a video Optional.
            
        """
        return self.submit_job("/predictions", fps=fps, frames_zip=frames_zip, frames_urls=frames_urls, **kwargs)
     