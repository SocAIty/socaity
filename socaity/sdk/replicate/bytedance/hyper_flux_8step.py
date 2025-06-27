from fastsdk import FastSDK, APISeex

class hyper_flux_8step(FastSDK):
    """
    Generated client for bytedance/hyper-flux-8step
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="4014c2a2-a4fc-4cc4-a2e9-b6ff08d5a618", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = 0, width: int = 848, height: int = 848, num_outputs: int = 1, aspect_ratio: str = '1:1', output_format: str = 'webp', guidance_scale: float = 3.5, output_quality: int = 80, num_inference_steps: int = 8, disable_safety_checker: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt for generated image
            
            seed: Random seed. Set for reproducible generation Defaults to 0.
            
            width: Width of the generated image. Optional, only used when aspect_ratio=custom. Must be a multiple of 16 (if it's not, it will be rounded to nearest multiple of 16) Defaults to 848.
            
            height: Height of the generated image. Optional, only used when aspect_ratio=custom. Must be a multiple of 16 (if it's not, it will be rounded to nearest multiple of 16) Defaults to 848.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            aspect_ratio: Aspect ratio for the generated image. The size will always be 1 megapixel, i.e. 1024x1024 if aspect ratio is 1:1. To use arbitrary width and height, set aspect ratio to 'custom'. Defaults to '1:1'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            guidance_scale: Guidance scale for the diffusion process Defaults to 3.5.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 80.
            
            num_inference_steps: Number of inference steps Defaults to 8.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, width=width, height=height, num_outputs=num_outputs, aspect_ratio=aspect_ratio, output_format=output_format, guidance_scale=guidance_scale, output_quality=output_quality, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions