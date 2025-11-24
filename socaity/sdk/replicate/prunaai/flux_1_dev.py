from fastsdk import FastClient, APISeex
from typing import Literal


class flux_1_dev(FastClient):
    """
    Generated client based on prunaai/flux-1-dev format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="96ed92a8-4291-46d7-a9d2-2827df0a69c7", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = -1, guidance: float = 3.5, image_size: int = 1024, speed_mode: Literal["Lightly Juiced 🍊 (more consistent)", "Juiced 🔥 (default)", "Extra Juiced 🔥 (more speed)", "Blink of an eye 👁️"] = 'Juiced 🔥 (default)', aspect_ratio: Literal["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21"] = '1:1', output_format: Literal["png", "jpg", "webp"] = 'jpg', output_quality: int = 80, num_inference_steps: int = 28, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt
            
            seed: Seed Defaults to -1.
            
            guidance: Guidance scale Defaults to 3.5.
            
            image_size: Base image size (longest side) Defaults to 1024.
            
            speed_mode: Speed optimization level Defaults to 'Juiced 🔥 (default)'.
            
            aspect_ratio: Aspect ratio of the output image Defaults to '1:1'.
            
            output_format: Output format Defaults to 'jpg'.
            
            output_quality: Output quality (for jpg and webp) Defaults to 80.
            
            num_inference_steps: Number of inference steps Defaults to 28.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, guidance=guidance, image_size=image_size, speed_mode=speed_mode, aspect_ratio=aspect_ratio, output_format=output_format, output_quality=output_quality, num_inference_steps=num_inference_steps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
