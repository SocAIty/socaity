from fastsdk import FastSDK, APISeex
from typing import Optional


class stable_diffusion_videos(FastSDK):
    """
    Generated client for nateraw/stable-diffusion-videos
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bfe0fe2b-a359-449c-8ae4-acc8fb4bb82c", api_key=api_key)
    
    def predictions(self, fps: int = 15, prompts: str = 'a cat | a dog | a horse', num_steps: int = 50, scheduler: str = 'klms', guidance_scale: float = 7.5, num_inference_steps: int = 50, seeds: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            fps: Frame rate for the video. Defaults to 15.
            
            prompts: Input prompts, separate each prompt with '|'. Defaults to 'a cat | a dog | a horse'.
            
            num_steps: Steps for generating the interpolation video. Recommended to set to 3 or 5 for testing, then up it to 60-200 for better results. Defaults to 50.
            
            scheduler: Choose the scheduler Defaults to 'klms'.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            num_inference_steps: Number of denoising steps for each image generated from the prompt Defaults to 50.
            
            seeds: Random seed, separated with '|' to use different seeds for each of the prompt provided above. Leave blank to randomize the seed. Optional.
            
        """
        return self.submit_job("/predictions", fps=fps, prompts=prompts, num_steps=num_steps, scheduler=scheduler, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seeds=seeds, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions