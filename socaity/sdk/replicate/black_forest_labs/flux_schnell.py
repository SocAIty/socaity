from fastsdk import FastClient, APISeex
from typing import Literal


class flux_schnell(FastClient):
    """
    Generated client based on black-forest-labs/flux-schnell format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="817bca01-a048-4959-84e3-f8be56044f48", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = 42, go_fast: bool = True, megapixels: Literal["1", "0.25"] = '1', num_outputs: int = 1, aspect_ratio: Literal["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21"] = '1:1', output_format: Literal["webp", "jpg", "png"] = 'webp', output_quality: int = 80, num_inference_steps: int = 4, disable_safety_checker: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt for generated image
            
            seed: Random seed. Set for reproducible generation Defaults to 42.
            
            go_fast: Run faster predictions with model optimized for speed (currently fp8 quantized); disable to run in original bf16. Note that outputs will not be deterministic when this is enabled, even if you set a seed. Defaults to True.
            
            megapixels: Approximate number of megapixels for generated image Defaults to '1'.
            
            num_outputs: Number of outputs to generate Defaults to 1.
            
            aspect_ratio: Aspect ratio for the generated image Defaults to '1:1'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 80.
            
            num_inference_steps: Number of denoising steps. 4 is recommended, and lower number of steps produce lower quality outputs, faster. Defaults to 4.
            
            disable_safety_checker: Disable safety checker for generated images. Defaults to False.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, go_fast=go_fast, megapixels=megapixels, num_outputs=num_outputs, aspect_ratio=aspect_ratio, output_format=output_format, output_quality=output_quality, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
