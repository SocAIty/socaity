from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class animesr(FastSDK):
    """
    Generated client for tencentarc/animesr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9d1a68b0-d400-4323-9e29-2a16c828f0e1", api_key=api_key)
    
    def predictions(self, video: Optional[Union[str, MediaFile, bytes]] = None, frames: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: Input video file Optional.
            
            frames: Zip file of frames of a video. Ignored when video is provided. Optional.
            
        """
        return self.submit_job("/predictions", video=video, frames=frames, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions