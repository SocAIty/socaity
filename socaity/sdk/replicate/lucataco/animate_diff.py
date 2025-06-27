from fastsdk import FastSDK, APISeex
from typing import Optional


class animate_diff(FastSDK):
    """
    Generated client for lucataco/animate-diff
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="701a8b9d-7d39-433d-bde2-8bcc483e09a3", api_key=api_key)
    
    def predictions(self, path: str = 'toonyou_beta3.safetensors', steps: int = 25, prompt: str = 'masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes', n_prompt: str = '', motion_module: str = 'mm_sd_v14', guidance_scale: float = 7.5, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            path: Select a Module Defaults to 'toonyou_beta3.safetensors'.
            
            steps: Number of inference steps Defaults to 25.
            
            prompt: Input prompt Defaults to 'masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes'.
            
            n_prompt: Negative prompt Defaults to ''.
            
            motion_module: Select a Motion Model Defaults to 'mm_sd_v14'.
            
            guidance_scale: guidance scale Defaults to 7.5.
            
            seed: Seed (0 = random, maximum: 2147483647) Optional.
            
        """
        return self.submit_job("/predictions", path=path, steps=steps, prompt=prompt, n_prompt=n_prompt, motion_module=motion_module, guidance_scale=guidance_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions