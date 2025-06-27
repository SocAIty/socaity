from fastsdk import FastSDK, APISeex

class hidream_l1_full(FastSDK):
    """
    Generated client for prunaai/hidream-l1-full
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="11792ec3-e2d8-4667-bfc2-ea46bfb5b9c7", api_key=api_key)
    
    def predictions(self, prompt: str, seed: int = -1, model_type: str = 'full', resolution: str = '1024 × 1024 (Square)', speed_mode: str = 'Lightly Juiced 🍊 (more consistent)', output_format: str = 'webp', output_quality: int = 100, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt
            
            seed: Random seed (-1 for random) Defaults to -1.
            
            model_type: Model type Defaults to 'full'.
            
            resolution: Output resolution Defaults to '1024 × 1024 (Square)'.
            
            speed_mode: Speed optimization level Defaults to 'Lightly Juiced 🍊 (more consistent)'.
            
            output_format: Output format Defaults to 'webp'.
            
            output_quality: Output quality (for jpg and webp) Defaults to 100.
            
        """
        return self.submit_job("/predictions", prompt=prompt, seed=seed, model_type=model_type, resolution=resolution, speed_mode=speed_mode, output_format=output_format, output_quality=output_quality, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions