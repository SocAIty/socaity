from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_hough(FastSDK):
    """
    Generated client for controlnet_hough
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a5474c59-aa6b-449b-ab84-6177f131b3a8", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], prompt: str, eta: float = 0.0, scale: float = 9.0, a_prompt: str = 'best quality, extremely detailed', n_prompt: str = 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', ddim_steps: int = 20, num_samples: str = '1', value_threshold: float = 0.1, image_resolution: str = '512', detect_resolution: int = 512, distance_threshold: float = 0.1, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            prompt: Prompt for the model
            
            eta: eta (DDIM) Defaults to 0.0.
            
            scale: Guidance Scale Defaults to 9.0.
            
            a_prompt: Added Prompt Defaults to 'best quality, extremely detailed'.
            
            n_prompt: Negative Prompt Defaults to 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            ddim_steps: Steps Defaults to 20.
            
            num_samples: Number of samples (higher values may OOM) Defaults to '1'.
            
            value_threshold: Value Threshold (only applicable when model type is 'MLSD') Defaults to 0.1.
            
            image_resolution: Image resolution to be generated Defaults to '512'.
            
            detect_resolution: Resolution for detection (only applicable when model type is 'HED', 'Segmentation', or 'MLSD') Defaults to 512.
            
            distance_threshold: Distance Threshold (only applicable when model type is 'MLSD') Defaults to 0.1.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predict", image=image, prompt=prompt, eta=eta, scale=scale, a_prompt=a_prompt, n_prompt=n_prompt, ddim_steps=ddim_steps, num_samples=num_samples, value_threshold=value_threshold, image_resolution=image_resolution, detect_resolution=detect_resolution, distance_threshold=distance_threshold, seed=seed, **kwargs)
     