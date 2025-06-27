from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class mvsep_mdx23_music_separation(FastSDK):
    """
    Generated client for lucataco/mvsep-mdx23-music-separation
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="dfc95e7b-bf4d-4f6b-ac10-fc8ee5177287", api_key=api_key)
    
    def predictions(self, audio: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            audio: Input Audio File
            
        """
        return self.submit_job("/predictions", audio=audio, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions