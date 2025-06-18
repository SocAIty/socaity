from fastsdk import FastSDK, APISeex
from typing import Optional


class tile_morph(FastSDK):
    """
    Generated client for andreasjansson/tile-morph
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6234b606-4f64-4f6c-b87d-cd9d6be23f19", api_key=api_key)
    
    def predictions(self, prompt_end: str, prompt_start: str, width: int = 512, height: int = 512, guidance_scale: float = 7.5, frames_per_second: int = 20, intermediate_output: bool = False, num_inference_steps: int = 50, num_animation_frames: int = 10, num_interpolation_steps: int = 20, seed_end: Optional[int] = None, seed_start: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt_end: Prompt to end the animation with. You can include multiple prompts by separating the prompts with | (the 'pipe' character)
            
            prompt_start: Prompt to start the animation with
            
            width: Width of output video Defaults to 512.
            
            height: Height of output video Defaults to 512.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            frames_per_second: Frames per second in output video Defaults to 20.
            
            intermediate_output: Whether to display intermediate outputs during generation Defaults to False.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            num_animation_frames: Number of frames to animate Defaults to 10.
            
            num_interpolation_steps: Number of steps to interpolate between animation frames Defaults to 20.
            
            seed_end: Random seed for last prompt. Leave blank to randomize the seed Optional.
            
            seed_start: Random seed for first prompt. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", prompt_end=prompt_end, prompt_start=prompt_start, width=width, height=height, guidance_scale=guidance_scale, frames_per_second=frames_per_second, intermediate_output=intermediate_output, num_inference_steps=num_inference_steps, num_animation_frames=num_animation_frames, num_interpolation_steps=num_interpolation_steps, seed_end=seed_end, seed_start=seed_start, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions