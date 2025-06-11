from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class rembg_video(FastSDK):
    """
    Generated client for rembg_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d16ea450-727e-4fae-8fd1-d3f8fecf7b23", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], mode: str = 'Normal', background_color: str = '#FFFFFF', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Grayscale input image
            
            mode: Mode of operation Defaults to 'Normal'.
            
            background_color: Background color in hex format (e.g., '#FFFFFF' for white) Defaults to '#FFFFFF'.
            
        """
        return self.submit_job("/predict", video=video, mode=mode, background_color=background_color, **kwargs)
     