from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class real_esrgan_video(FastSDK):
    """
    Generated client for real_esrgan_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="aac0fe73-e4f7-419a-b916-cf771b6d971c", api_key=api_key)
    
    def predict(self, video_path: Union[MediaFile, str, bytes], model: str = 'RealESRGAN_x4plus', resolution: str = 'FHD', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video_path: Input Video
            
            model: Upscaling model Defaults to 'RealESRGAN_x4plus'.
            
            resolution: Output resolution Defaults to 'FHD'.
            
        """
        return self.submit_job("/predict", video_path=video_path, model=model, resolution=resolution, **kwargs)
     