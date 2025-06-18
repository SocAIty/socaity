from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class demofusion_enhance(FastSDK):
    """
    Generated client for lucataco/demofusion-enhance
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2690a512-4e72-4970-93c3-da2639c720dd", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], scale: int = 2, sigma: float = 0.8, prompt: str = 'A high resolution photo', stride: int = 64, auto_prompt: bool = False, multi_decoder: bool = False, cosine_scale_1: float = 3.0, cosine_scale_2: float = 1.0, cosine_scale_3: float = 1.0, guidance_scale: float = 8.5, negative_prompt: str = 'blurry, ugly, duplicate, poorly drawn, deformed, mosaic', view_batch_size: int = 16, num_inference_steps: int = 40, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            scale: Scale factor for input image Defaults to 2.
            
            sigma: The standard value of the Gaussian filter Defaults to 0.8.
            
            prompt: Input prompt Defaults to 'A high resolution photo'.
            
            stride: The stride of moving local patches Defaults to 64.
            
            auto_prompt: Select to use auto-generated CLIP prompt instead of using the above custom prompt Defaults to False.
            
            multi_decoder: Use multiple decoders Defaults to False.
            
            cosine_scale_1: Control the strength of skip-residual Defaults to 3.0.
            
            cosine_scale_2: Control the strength of dilated sampling Defaults to 1.0.
            
            cosine_scale_3: Control the strength of the Gaussian filter Defaults to 1.0.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 8.5.
            
            negative_prompt: Input Negative Prompt Defaults to 'blurry, ugly, duplicate, poorly drawn, deformed, mosaic'.
            
            view_batch_size: The batch size for multiple denoising paths Defaults to 16.
            
            num_inference_steps: Number of denoising steps Defaults to 40.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, sigma=sigma, prompt=prompt, stride=stride, auto_prompt=auto_prompt, multi_decoder=multi_decoder, cosine_scale_1=cosine_scale_1, cosine_scale_2=cosine_scale_2, cosine_scale_3=cosine_scale_3, guidance_scale=guidance_scale, negative_prompt=negative_prompt, view_batch_size=view_batch_size, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions