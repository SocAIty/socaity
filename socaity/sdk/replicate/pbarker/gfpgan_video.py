from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class gfpgan_video(FastSDK):
    """
    Generated client for pbarker/gfpgan-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3454b77b-92fa-4578-9f67-afc287ca389a", api_key=api_key)
    
    def predictions(self, video: Union[MediaFile, str, bytes], scale: float = 2.0, version: str = 'v1.4', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input
            
            scale: Rescaling factor Defaults to 2.0.
            
            version: GFPGAN version. v1.3: better quality. v1.4: more details and better identity. Defaults to 'v1.4'.
            
        """
        return self.submit_job("/predictions", video=video, scale=scale, version=version, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions