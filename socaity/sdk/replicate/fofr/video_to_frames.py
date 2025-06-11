from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class video_to_frames(FastSDK):
    """
    Generated client for video_to_frames
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d49c06f4-ff2c-4cfc-9ae6-73cf0f053755", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], fps: int = 1, extract_all_frames: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Video to split into frames
            
            fps: Number of images per second of video, when not exporting all frames Defaults to 1.
            
            extract_all_frames: Get every frame of the video. Ignores fps. Slow for large videos. Defaults to False.
            
        """
        return self.submit_job("/predict", video=video, fps=fps, extract_all_frames=extract_all_frames, **kwargs)
     