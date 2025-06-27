from fastsdk import FastSDK, APISeex
from typing import Optional


class dreamshaper_xl_turbo(FastSDK):
    """
    Generated client for lucataco/dreamshaper-xl-turbo
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="378d5112-177a-4bfe-858f-598bda4c8f57", api_key=api_key)
    
    def predictions(self, width: int = 1024, height: int = 1024, prompt: str = 'An astronaut riding a rainbow unicorn', scheduler: str = 'K_EULER', num_outputs: int = 1, guidance_scale: float = 2.0, apply_watermark: bool = True, negative_prompt: str = '', num_inference_steps: int = 6, disable_safety_checker: bool = False, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'An astronaut riding a rainbow unicorn'.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 2.0.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Input Negative Prompt Defaults to ''.
            
            num_inference_steps: Number of denoising steps Defaults to 6.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions