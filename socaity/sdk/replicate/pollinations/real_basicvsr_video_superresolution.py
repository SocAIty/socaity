from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_basicvsr_video_superresolution(FastSDK):
    """
    Generated client for real_basicvsr_video_superresolution
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="852c24f4-21f9-4830-9fd7-e75b3a720147", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: input video
            
        """
        return self.submit_job("/predict", video=video, **kwargs)
     