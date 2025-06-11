from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class video_split(FastSDK):
    """
    Generated client for video_split
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f371859e-92e1-4f52-b8a8-d39e857134a7", api_key=api_key)
    
    def predict(self, input_video: Union[MediaFile, str, bytes], target_fps: int = 30, target_width: int = 848, target_height: int = 480, create_captions: bool = False, target_duration: float = 2.0, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Input video file (MP4 or MOV)
            
            target_fps: Target FPS for each segment Defaults to 30.
            
            target_width: Target width for each segment Defaults to 848.
            
            target_height: Target height for each segment Defaults to 480.
            
            create_captions: Create empty caption files for each segment Defaults to False.
            
            target_duration: Target duration for each segment in seconds Defaults to 2.0.
            
        """
        return self.submit_job("/predict", input_video=input_video, target_fps=target_fps, target_width=target_width, target_height=target_height, create_captions=create_captions, target_duration=target_duration, **kwargs)
     