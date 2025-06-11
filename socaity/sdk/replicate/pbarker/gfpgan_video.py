from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class gfpgan_video(FastSDK):
    """
    Generated client for gfpgan_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6f12db04-5d60-407d-974f-0357f8f8beba", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], scale: float = 2.0, version: str = 'v1.4', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input
            
            scale: Rescaling factor Defaults to 2.0.
            
            version: GFPGAN version. v1.3: better quality. v1.4: more details and better identity. Defaults to 'v1.4'.
            
        """
        return self.submit_job("/predict", video=video, scale=scale, version=version, **kwargs)
     