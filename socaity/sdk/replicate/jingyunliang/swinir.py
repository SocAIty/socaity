from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class swinir(FastSDK):
    """
    Generated client for jingyunliang/swinir
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a38caf79-16b9-494d-a212-5191e6e72799", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], jpeg: int = 40, noise: int = 15, task_type: str = 'Real-World Image Super-Resolution-Large', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: input image
            
            jpeg: scale factor, activated for JPEG Compression Artifact Reduction. Leave it as default or arbitrary if other tasks are selected Defaults to 40.
            
            noise: noise level, activated for Grayscale Image Denoising and Color Image Denoising. Leave it as default or arbitrary if other tasks are selected Defaults to 15.
            
            task_type: Choose a task Defaults to 'Real-World Image Super-Resolution-Large'.
            
        """
        return self.submit_job("/predictions", image=image, jpeg=jpeg, noise=noise, task_type=task_type, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions