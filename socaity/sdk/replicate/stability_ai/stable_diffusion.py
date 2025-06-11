from fastsdk.fastSDK import FastSDK
from typing import Optional


class stable_diffusion(FastSDK):
    """
    Generated client for stable_diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="106178c0-3000-49f9-8e18-3f62ca8d68ad", api_key=api_key)
    
    def predict(self, width: int = 768, height: int = 768, prompt: str = 'a vision of paradise. unreal engine', scheduler: str = 'DPMSolverMultistep', num_outputs: int = 1, guidance_scale: float = 7.5, num_inference_steps: int = 50, seed: Optional[int] = None, negative_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of generated image in pixels. Needs to be a multiple of 64 Defaults to 768.
            
            height: Height of generated image in pixels. Needs to be a multiple of 64 Defaults to 768.
            
            prompt: Input prompt Defaults to 'a vision of paradise. unreal engine'.
            
            scheduler: Choose a scheduler. Defaults to 'DPMSolverMultistep'.
            
            num_outputs: Number of images to generate. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            negative_prompt: Specify things to not see in the output Optional.
            
        """
        return self.submit_job("/predict", width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seed=seed, negative_prompt=negative_prompt, **kwargs)
     