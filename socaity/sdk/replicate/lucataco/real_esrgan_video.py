from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class real_esrgan_video(FastSDK):
    """
    Generated client for lucataco/real-esrgan-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f7b0ed6f-3794-4b3f-a273-f2d96d2b699a", api_key=api_key)
    
    def predictions(self, video_path: Union[str, MediaFile, bytes], model: str = 'RealESRGAN_x4plus', resolution: str = 'FHD', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video_path: Input Video
            
            model: Upscaling model Defaults to 'RealESRGAN_x4plus'.
            
            resolution: Output resolution Defaults to 'FHD'.
            
        """
        return self.submit_job("/predictions", video_path=video_path, model=model, resolution=resolution, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions