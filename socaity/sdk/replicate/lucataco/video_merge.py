from fastsdk import FastSDK, APISeex
from typing import List, Any, Union

from media_toolkit import MediaFile


class video_merge(FastSDK):
    """
    Generated client for lucataco/video-merge
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0a9bb226-1d9f-4252-bff3-7a5de0c58d55", api_key=api_key)
    
    def predictions(self, video_files: Union[str, MediaFile, List[Any], bytes], fps: int = 0, width: int = 0, height: int = 0, keep_audio: bool = True, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video_files: List of video files to concatenate
            
            fps: Output video frame rate. If not specified, uses first video's fps Defaults to 0.
            
            width: Output video width. If not specified, uses first video's width Defaults to 0.
            
            height: Output video height. If not specified, uses first video's height Defaults to 0.
            
            keep_audio: Whether to keep audio in the output video Defaults to True.
            
        """
        return self.submit_job("/predictions", video_files=video_files, fps=fps, width=width, height=height, keep_audio=keep_audio, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions