from fastsdk.fastSDK import FastSDK
from typing import Optional


class stable_diffusion_animation(FastSDK):
    """
    Generated client for stable_diffusion_animation
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0bb4440e-c3d5-4050-b556-7d5f6800200b", api_key=api_key)
    
    def predict(self, prompt_end: str, prompt_start: str, width: int = 512, height: int = 512, gif_ping_pong: bool = False, output_format: str = 'gif', guidance_scale: float = 7.5, prompt_strength: float = 0.8, film_interpolation: bool = True, intermediate_output: bool = False, num_inference_steps: int = 50, num_animation_frames: int = 10, gif_frames_per_second: int = 20, num_interpolation_steps: int = 5, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt_end: Prompt to end the animation with. You can include multiple prompts by separating the prompts with | (the 'pipe' character)
            
            prompt_start: Prompt to start the animation with
            
            width: Width of output image Defaults to 512.
            
            height: Height of output image Defaults to 512.
            
            gif_ping_pong: Whether to reverse the animation and go back to the beginning before looping Defaults to False.
            
            output_format: Output file format Defaults to 'gif'.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            prompt_strength: Lower prompt strength generates more coherent gifs, higher respects prompts more but can be jumpy Defaults to 0.8.
            
            film_interpolation: Whether to use FILM for between-frame interpolation (film-net.github.io) Defaults to True.
            
            intermediate_output: Whether to display intermediate outputs during generation Defaults to False.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            num_animation_frames: Number of frames to animate Defaults to 10.
            
            gif_frames_per_second: Frames/second in output GIF Defaults to 20.
            
            num_interpolation_steps: Number of steps to interpolate between animation frames Defaults to 5.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", prompt_end=prompt_end, prompt_start=prompt_start, width=width, height=height, gif_ping_pong=gif_ping_pong, output_format=output_format, guidance_scale=guidance_scale, prompt_strength=prompt_strength, film_interpolation=film_interpolation, intermediate_output=intermediate_output, num_inference_steps=num_inference_steps, num_animation_frames=num_animation_frames, gif_frames_per_second=gif_frames_per_second, num_interpolation_steps=num_interpolation_steps, seed=seed, **kwargs)
     