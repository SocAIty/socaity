from fastsdk import FastClient, APISeex
from typing import Literal


class hidream_l1_dev(FastClient):
    """
    Generated client based on prunaai/hidream-l1-dev format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ee3d7ab3-c7aa-4465-9e93-78f7eb2c5cf5", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = -1, model_type: Literal["dev"] = 'dev', resolution: Literal["1024 × 1024 (Square)", "768 × 1360 (Portrait)", "1360 × 768 (Landscape)", "880 × 1168 (Portrait)", "1168 × 880 (Landscape)", "1248 × 832 (Landscape)", "832 × 1248 (Portrait)"] = '1024 × 1024 (Square)', speed_mode: Literal["Unsqueezed 🍋 (highest quality)", "Lightly Juiced 🍊 (more consistent)", "Juiced 🔥 (more speed)", "Extra Juiced 🚀 (even more speed)"] = 'Lightly Juiced 🍊 (more consistent)', output_format: Literal["png", "jpg", "webp"] = 'webp', output_quality: int = 100, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt
            
            seed: Random seed (-1 for random) Defaults to -1.
            
            model_type: Model type Defaults to 'dev'.
            
            resolution: Output resolution Defaults to '1024 × 1024 (Square)'.
            
            speed_mode: Speed optimization level Defaults to 'Lightly Juiced 🍊 (more consistent)'.
            
            output_format: Output format Defaults to 'webp'.
            
            output_quality: Output quality (for jpg and webp) Defaults to 100.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, model_type=model_type, resolution=resolution, speed_mode=speed_mode, output_format=output_format, output_quality=output_quality, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
