from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class video_background_remover_appender(FastSDK):
    """
    Generated client for tahercoolguy/video-background-remover-appender
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="360e4917-ea74-4b91-98e8-7ba010b0151d", api_key=api_key)
    
    def predictions(self, input_video: Union[MediaFile, str, bytes], fps: int = 0, color: str = '#00FF00', bg_mode: str = 'cover', bg_type: str = 'Color', video_handling: str = 'loop', bg_image: Optional[Union[MediaFile, str, bytes]] = None, bg_video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Input video
            
            fps: Output FPS Defaults to 0.
            
            color: Background Color Defaults to '#00FF00'.
            
            bg_mode: Background Mode Defaults to 'cover'.
            
            bg_type: Background Type Defaults to 'Color'.
            
            video_handling: Video Handling Defaults to 'loop'.
            
            bg_image: Background Image Optional.
            
            bg_video: Background Video Optional.
            
        """
        return self.submit_job("/predictions", input_video=input_video, fps=fps, color=color, bg_mode=bg_mode, bg_type=bg_type, video_handling=video_handling, bg_image=bg_image, bg_video=bg_video, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions