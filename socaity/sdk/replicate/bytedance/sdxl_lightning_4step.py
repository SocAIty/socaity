from fastsdk import FastSDK, APISeex

class sdxl_lightning_4step(FastSDK):
    """
    Generated client for bytedance/sdxl-lightning-4step
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bfa5b88b-0143-4f31-9466-1db95a18f13b", api_key=api_key)
    
    def predictions(self, seed: int = 0, width: int = 1024, height: int = 1024, prompt: str = 'self-portrait of a woman, lightning in the background', scheduler: str = 'K_EULER', num_outputs: int = 1, guidance_scale: float = 0.0, negative_prompt: str = 'worst quality, low quality', num_inference_steps: int = 4, disable_safety_checker: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            seed: Random seed. Leave blank to randomize the seed Defaults to 0.
            
            width: Width of output image. Recommended 1024 or 1280 Defaults to 1024.
            
            height: Height of output image. Recommended 1024 or 1280 Defaults to 1024.
            
            prompt: Input prompt Defaults to 'self-portrait of a woman, lightning in the background'.
            
            scheduler: scheduler Defaults to 'K_EULER'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 0.0.
            
            negative_prompt: Negative Input prompt Defaults to 'worst quality, low quality'.
            
            num_inference_steps: Number of denoising steps. 4 for best results Defaults to 4.
            
            disable_safety_checker: Disable safety checker for generated images Defaults to False.
            
        """
        return self.submit_job("/predictions", seed=seed, width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions