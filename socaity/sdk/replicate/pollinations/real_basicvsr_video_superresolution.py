from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_basicvsr_video_superresolution(FastSDK):
    """
    Generated client for pollinations/real-basicvsr-video-superresolution
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b901d4ed-734c-4961-9873-121a55ff9ce1", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: input video
            
        """
        return self.submit_job("/predictions", video=video, **kwargs)
     