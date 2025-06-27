from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class depth_anything_video(FastSDK):
    """
    Generated client for lucataco/depth-anything-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6b9644e4-0161-4dc8-bda5-aa76bf67233b", api_key=api_key)
    
    def predictions(self, video: Union[str, MediaFile, bytes], encoder: str = 'vits', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: Input video
            
            encoder: Model type Defaults to 'vits'.
            
        """
        return self.submit_job("/predictions", video=video, encoder=encoder, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions