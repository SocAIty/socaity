from fastsdk import FastSDK, APISeex
from typing import Optional


class kandinsky_2(FastSDK):
    """
    Generated client for ai-forever/kandinsky-2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c88e58ad-8d8d-4331-ad77-eed3e1a92e6b", api_key=api_key)
    
    def predictions(self, width: int = 512, height: int = 512, prompt: str = 'red cat, 4k photo', scheduler: str = 'p_sampler', batch_size: int = 1, prior_steps: str = '5', output_format: str = 'webp', guidance_scale: float = 4.0, output_quality: int = 80, prior_cf_scale: int = 4, num_inference_steps: int = 50, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            width: Choose width. Lower the setting if out of memory. Defaults to 512.
            
            height: Choose height. Lower the setting if out of memory. Defaults to 512.
            
            prompt: Input Prompt Defaults to 'red cat, 4k photo'.
            
            scheduler: Choose a scheduler Defaults to 'p_sampler'.
            
            batch_size: Choose batch size. Lower the setting if out of memory. Defaults to 1.
            
            prior_steps: prior_steps Defaults to '5'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 4.0.
            
            output_quality: Quality of the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Defaults to 80.
            
            prior_cf_scale: prior_cf_scale Defaults to 4.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, batch_size=batch_size, prior_steps=prior_steps, output_format=output_format, guidance_scale=guidance_scale, output_quality=output_quality, prior_cf_scale=prior_cf_scale, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions