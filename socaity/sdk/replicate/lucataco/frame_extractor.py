from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class frame_extractor(FastSDK):
    """
    Generated client for lucataco/frame-extractor
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="75d0bd49-1736-4298-b105-7d3663c3b71a", api_key=api_key)
    
    def predictions(self, video: Union[str, MediaFile, bytes], return_first_frame: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: Input video file
            
            return_first_frame: Toggle to return the first frame instead of the last frame Defaults to False.
            
        """
        return self.submit_job("/predictions", video=video, return_first_frame=return_first_frame, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions