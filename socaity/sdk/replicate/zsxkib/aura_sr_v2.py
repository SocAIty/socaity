from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class aura_sr_v2(FastSDK):
    """
    Generated client for zsxkib/aura-sr-v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e6bb9747-7fbb-43a8-8045-84b7379084f1", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], output_format: str = 'webp', max_batch_size: int = 8, output_quality: int = 80, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image to upscale
            
            output_format: The image file format of the generated output images Defaults to 'webp'.
            
            max_batch_size: Maximum number of tiles to process in a single batch. Higher values may increase speed but require more GPU memory. Defaults to 8.
            
            output_quality: The image compression quality (for lossy formats like JPEG and WebP). 100 = best quality, 0 = lowest quality. Defaults to 80.
            
        """
        return self.submit_job("/predictions", image=image, output_format=output_format, max_batch_size=max_batch_size, output_quality=output_quality, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions