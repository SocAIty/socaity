from fastsdk.fastSDK import FastSDK
from typing import Optional


class stable_diffusion_videos(FastSDK):
    """
    Generated client for stable_diffusion_videos
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="38e4414f-20c4-413f-90ea-244c751e6969", api_key=api_key)
    
    def predict(self, fps: int = 15, prompts: str = 'a cat | a dog | a horse', num_steps: int = 50, scheduler: str = 'klms', guidance_scale: float = 7.5, num_inference_steps: int = 50, seeds: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            fps: Frame rate for the video. Defaults to 15.
            
            prompts: Input prompts, separate each prompt with '|'. Defaults to 'a cat | a dog | a horse'.
            
            num_steps: Steps for generating the interpolation video. Recommended to set to 3 or 5 for testing, then up it to 60-200 for better results. Defaults to 50.
            
            scheduler: Choose the scheduler Defaults to 'klms'.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            num_inference_steps: Number of denoising steps for each image generated from the prompt Defaults to 50.
            
            seeds: Random seed, separated with '|' to use different seeds for each of the prompt provided above. Leave blank to randomize the seed. Optional.
            
        """
        return self.submit_job("/predict", fps=fps, prompts=prompts, num_steps=num_steps, scheduler=scheduler, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seeds=seeds, **kwargs)
     