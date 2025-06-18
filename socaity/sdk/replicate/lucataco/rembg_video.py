from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class rembg_video(FastSDK):
    """
    Generated client for lucataco/rembg-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="26f1e220-7c28-4bd5-aef1-9ca64b2fe2e2", api_key=api_key)
    
    def predictions(self, video: Union[MediaFile, str, bytes], mode: str = 'Normal', background_color: str = '#FFFFFF', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            video: Grayscale input image
            
            mode: Mode of operation Defaults to 'Normal'.
            
            background_color: Background color in hex format (e.g., '#FFFFFF' for white) Defaults to '#FFFFFF'.
            
        """
        return self.submit_job("/predictions", video=video, mode=mode, background_color=background_color, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions