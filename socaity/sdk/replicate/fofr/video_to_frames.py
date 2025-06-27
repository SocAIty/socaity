from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class video_to_frames(FastSDK):
    """
    Generated client for fofr/video-to-frames
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="38cdb864-c91c-4e49-8fbf-c4788e3f75bc", api_key=api_key)
    
    def predictions(self, video: Union[str, MediaFile, bytes], fps: int = 1, extract_all_frames: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: Video to split into frames
            
            fps: Number of images per second of video, when not exporting all frames Defaults to 1.
            
            extract_all_frames: Get every frame of the video. Ignores fps. Slow for large videos. Defaults to False.
            
        """
        return self.submit_job("/predictions", video=video, fps=fps, extract_all_frames=extract_all_frames, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions