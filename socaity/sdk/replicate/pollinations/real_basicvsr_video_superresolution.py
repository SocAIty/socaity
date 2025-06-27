from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class real_basicvsr_video_superresolution(FastSDK):
    """
    Generated client for pollinations/real-basicvsr-video-superresolution
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b901d4ed-734c-4961-9873-121a55ff9ce1", api_key=api_key)
    
    def predictions(self, video: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: input video
            
        """
        return self.submit_job("/predictions", video=video, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions