from fastsdk.fastSDK import FastSDK
from typing import Optional


class videocrafter(FastSDK):
    """
    Generated client for videocrafter
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5659e8fa-58e7-45a5-870a-8bb9277652b9", api_key=api_key)
    
    def predict(self, prompt: str = 'With the style of van gogh, A young couple dances under the moonlight by the lake.', save_fps: int = 10, ddim_steps: int = 50, unconditional_guidance_scale: float = 12.0, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt for video generation. Defaults to 'With the style of van gogh, A young couple dances under the moonlight by the lake.'.
            
            save_fps: Frame per second for the generated video. Defaults to 10.
            
            ddim_steps: Number of denoising steps. Defaults to 50.
            
            unconditional_guidance_scale: Classifier-free guidance scale. Defaults to 12.0.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, save_fps=save_fps, ddim_steps=ddim_steps, unconditional_guidance_scale=unconditional_guidance_scale, seed=seed, **kwargs)
     