from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_hed(FastSDK):
    """
    Generated client for controlnet_hed
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="83065bd3-4333-4f82-ba9a-f2789b7e082f", api_key=api_key)
    
    def predict(self, prompt: str, input_image: Union[MediaFile, str, bytes], eta: float = 0.0, scale: float = 9.0, a_prompt: str = 'best quality, extremely detailed', n_prompt: str = 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', ddim_steps: int = 20, num_samples: str = '1', image_resolution: str = '512', detect_resolution: int = 512, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt for the model
            
            input_image: Input image
            
            eta: eta (DDIM) Defaults to 0.0.
            
            scale: Guidance Scale Defaults to 9.0.
            
            a_prompt: Added Prompt Defaults to 'best quality, extremely detailed'.
            
            n_prompt: Negative Prompt Defaults to 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            ddim_steps: Steps Defaults to 20.
            
            num_samples: Number of samples (higher values may OOM) Defaults to '1'.
            
            image_resolution: Image resolution to be generated Defaults to '512'.
            
            detect_resolution: Resolution for detection (only applicable when model type is 'HED') Defaults to 512.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, input_image=input_image, eta=eta, scale=scale, a_prompt=a_prompt, n_prompt=n_prompt, ddim_steps=ddim_steps, num_samples=num_samples, image_resolution=image_resolution, detect_resolution=detect_resolution, seed=seed, **kwargs)
     