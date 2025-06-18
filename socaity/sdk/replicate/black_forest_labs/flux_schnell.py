from fastsdk import FastSDK, APISeex
from typing import Optional


class flux_schnell(FastSDK):
    """
    Generated client for black-forest-labs/flux-schnell
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="817bca01-a048-4959-84e3-f8be56044f48", api_key=api_key)
    
    def predictions(self, prompt: str, go_fast: bool = True, megapixels: str = '1', num_outputs: int = 1, aspect_ratio: str = '1:1', output_format: str = 'webp', output_quality: int = 80, num_inference_steps: int = 4, disable_safety_checker: bool = False, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt for generated image
            
            go_fast: Run faster predictions with model optimized for speed (currently fp8 quantized); disable to run in original bf16 Defaults to True.
            
            megapixels: Approximate number of megapixels for generated image Defaults to '1'.
            
            num_outputs: Number of outputs to generate Defaults to 1.
            
            aspect_ratio: Aspect ratio for the generated image Defaults to '1:1'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 80.
            
            num_inference_steps: Number of denoising steps. 4 is recommended, and lower number of steps produce lower quality outputs, faster. Defaults to 4.
            
            disable_safety_checker: Disable safety checker for generated images. Defaults to False.
            
            seed: Random seed. Set for reproducible generation Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, go_fast=go_fast, megapixels=megapixels, num_outputs=num_outputs, aspect_ratio=aspect_ratio, output_format=output_format, output_quality=output_quality, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions