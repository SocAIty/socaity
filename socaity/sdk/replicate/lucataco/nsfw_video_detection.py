from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class nsfw_video_detection(FastSDK):
    """
    Generated client for lucataco/nsfw-video-detection
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9a2797ac-5ee0-4cff-baea-a9d2f65ac18d", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], safety_tolerance: int = 2, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video
            
            safety_tolerance: Safety tolerance, 1 is most strict and 6 is most permissive Defaults to 2.
            
        """
        return self.submit_job("/predictions", video=video, safety_tolerance=safety_tolerance, **kwargs)
     