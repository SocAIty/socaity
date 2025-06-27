from fastsdk import FastSDK, APISeex

class sdxl_lightning(FastSDK):
    """
    Generated client for prunaai/sdxl-lightning
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="46273539-afd7-4579-8690-cccd1971e722", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = 42, num_images: int = 1, image_width: int = 1024, image_height: int = 1024, output_format: str = 'jpg', guidance_scale: float = 0.0, output_quality: int = 80, num_inference_steps: int = 4, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt
            
            seed: Seed Defaults to 42.
            
            num_images: Number of images to generate Defaults to 1.
            
            image_width: Image width Defaults to 1024.
            
            image_height: Image height Defaults to 1024.
            
            output_format: Output format Defaults to 'jpg'.
            
            guidance_scale: Guidance scale Defaults to 0.0.
            
            output_quality: Output quality (for jpg and webp) Defaults to 80.
            
            num_inference_steps: Number of inference steps Defaults to 4.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, num_images=num_images, image_width=image_width, image_height=image_height, output_format=output_format, guidance_scale=guidance_scale, output_quality=output_quality, num_inference_steps=num_inference_steps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions