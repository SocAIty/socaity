from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class video_split(FastSDK):
    """
    Generated client for lucataco/video-split
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c51c85bb-b396-4089-84a5-3a706c8e8756", api_key=api_key)
    
    def predictions(self, input_video: Union[str, MediaFile, bytes], target_fps: int = 30, target_width: int = 848, target_height: int = 480, create_captions: bool = False, target_duration: float = 2.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            input_video: Input video file (MP4 or MOV)
            
            target_fps: Target FPS for each segment Defaults to 30.
            
            target_width: Target width for each segment Defaults to 848.
            
            target_height: Target height for each segment Defaults to 480.
            
            create_captions: Create empty caption files for each segment Defaults to False.
            
            target_duration: Target duration for each segment in seconds Defaults to 2.0.
            
        """
        return self.submit_job("/predictions", input_video=input_video, target_fps=target_fps, target_width=target_width, target_height=target_height, create_captions=create_captions, target_duration=target_duration, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions