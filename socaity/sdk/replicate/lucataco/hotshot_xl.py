from fastsdk import FastSDK, APISeex
from typing import Optional


class hotshot_xl(FastSDK):
    """
    Generated client for lucataco/hotshot-xl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5ceba273-ccc6-4b04-b3fe-bc7a254e8456", api_key=api_key)
    
    def predictions(self, mp4: bool = False, steps: int = 30, width: int = 672, height: int = 384, prompt: str = 'a camel smoking a cigarette, hd, high quality', scheduler: str = 'EulerAncestralDiscreteScheduler', negative_prompt: str = 'blurry', seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            mp4: Save as mp4, False for GIF Defaults to False.
            
            steps: Number of denoising steps Defaults to 30.
            
            width: Width of the output Defaults to 672.
            
            height: Height of the output Defaults to 384.
            
            prompt: Input prompt Defaults to 'a camel smoking a cigarette, hd, high quality'.
            
            scheduler: Select a Scheduler Defaults to 'EulerAncestralDiscreteScheduler'.
            
            negative_prompt: Negative prompt Defaults to 'blurry'.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", mp4=mp4, steps=steps, width=width, height=height, prompt=prompt, scheduler=scheduler, negative_prompt=negative_prompt, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions