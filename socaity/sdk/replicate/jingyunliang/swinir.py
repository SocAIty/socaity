from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class swinir(FastSDK):
    """
    Generated client for swinir
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="30382029-d4d8-4ffe-acdd-d2b1b747194d", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], jpeg: int = 40, noise: int = 15, task_type: str = 'Real-World Image Super-Resolution-Large', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: input image
            
            jpeg: scale factor, activated for JPEG Compression Artifact Reduction. Leave it as default or arbitrary if other tasks are selected Defaults to 40.
            
            noise: noise level, activated for Grayscale Image Denoising and Color Image Denoising. Leave it as default or arbitrary if other tasks are selected Defaults to 15.
            
            task_type: Choose a task Defaults to 'Real-World Image Super-Resolution-Large'.
            
        """
        return self.submit_job("/predict", image=image, jpeg=jpeg, noise=noise, task_type=task_type, **kwargs)
     