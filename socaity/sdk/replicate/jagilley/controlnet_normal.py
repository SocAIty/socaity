from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_normal(FastSDK):
    """
    Generated client for jagilley/controlnet-normal
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d5b65bd9-c507-4297-a1aa-e9a885651f7f", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], prompt: str, eta: float = 0.0, scale: float = 9.0, a_prompt: str = 'best quality, extremely detailed', n_prompt: str = 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', ddim_steps: int = 20, num_samples: str = '1', bg_threshold: float = 0.0, image_resolution: str = '512', detect_resolution: int = 512, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            prompt: Prompt for the model
            
            eta: eta (DDIM) Defaults to 0.0.
            
            scale: Guidance Scale Defaults to 9.0.
            
            a_prompt: Added Prompt Defaults to 'best quality, extremely detailed'.
            
            n_prompt: Negative Prompt Defaults to 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            ddim_steps: Steps Defaults to 20.
            
            num_samples: Number of samples (higher values may OOM) Defaults to '1'.
            
            bg_threshold: Background Threshold (only applicable when model type is 'normal') Defaults to 0.0.
            
            image_resolution: Image resolution to be generated Defaults to '512'.
            
            detect_resolution: Resolution for detection) Defaults to 512.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, eta=eta, scale=scale, a_prompt=a_prompt, n_prompt=n_prompt, ddim_steps=ddim_steps, num_samples=num_samples, bg_threshold=bg_threshold, image_resolution=image_resolution, detect_resolution=detect_resolution, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions