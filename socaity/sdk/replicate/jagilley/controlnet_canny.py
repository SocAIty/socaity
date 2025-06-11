from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_canny(FastSDK):
    """
    Generated client for controlnet_canny
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="72ec1812-88a5-469d-91dc-3c5c3ea9cb0f", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], prompt: str, eta: float = 0.0, scale: float = 9.0, a_prompt: str = 'best quality, extremely detailed', n_prompt: str = 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', ddim_steps: int = 20, num_samples: str = '1', low_threshold: int = 100, high_threshold: int = 200, image_resolution: str = '512', seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
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
        return self.submit_job("/predict", image=image, prompt=prompt, eta=eta, scale=scale, a_prompt=a_prompt, n_prompt=n_prompt, ddim_steps=ddim_steps, num_samples=num_samples, low_threshold=low_threshold, high_threshold=high_threshold, image_resolution=image_resolution, seed=seed, **kwargs)
     