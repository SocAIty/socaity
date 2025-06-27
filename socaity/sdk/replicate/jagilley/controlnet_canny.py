from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_canny(FastSDK):
    """
    Generated client for jagilley/controlnet-canny
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d3af7abf-aeb2-4d01-9de4-8a7e6ad40c76", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], prompt: str, eta: float = 0.0, scale: float = 9.0, a_prompt: str = 'best quality, extremely detailed', n_prompt: str = 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', ddim_steps: int = 20, num_samples: str = '1', low_threshold: int = 100, high_threshold: int = 200, image_resolution: str = '512', seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            prompt: Prompt for the model
            
            eta: Controls the amount of noise that is added to the input data during the denoising diffusion process. Higher value -> more noise Defaults to 0.0.
            
            scale: Scale for classifier-free guidance Defaults to 9.0.
            
            a_prompt: Additional text to be appended to prompt Defaults to 'best quality, extremely detailed'.
            
            n_prompt: Negative Prompt Defaults to 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            ddim_steps: Steps Defaults to 20.
            
            num_samples: Number of samples (higher values may OOM) Defaults to '1'.
            
            low_threshold: Canny line detection low threshold Defaults to 100.
            
            high_threshold: Canny line detection high threshold Defaults to 200.
            
            image_resolution: Image resolution to be generated Defaults to '512'.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, eta=eta, scale=scale, a_prompt=a_prompt, n_prompt=n_prompt, ddim_steps=ddim_steps, num_samples=num_samples, low_threshold=low_threshold, high_threshold=high_threshold, image_resolution=image_resolution, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions