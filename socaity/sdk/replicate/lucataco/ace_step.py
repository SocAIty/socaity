from fastsdk.fastSDK import FastSDK
from typing import Optional


class ace_step(FastSDK):
    """
    Generated client for ace_step
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="54669824-2a2b-41ea-828e-82e3c4a2682f", api_key=api_key)
    
    def predict(self, tags: str, seed: int = -1, duration: float = 60.0, scheduler: str = 'euler', guidance_type: str = 'apg', guidance_scale: float = 15.0, number_of_steps: int = 60, granularity_scale: float = 10.0, guidance_interval: float = 0.5, min_guidance_scale: float = 3.0, tag_guidance_scale: float = 0.0, lyric_guidance_scale: float = 0.0, guidance_interval_decay: float = 0.0, lyrics: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            tags: Text prompts to guide music generation, e.g., 'epic,cinematic'
            
            seed: Random seed. Set to -1 to randomize. Defaults to -1.
            
            duration: Duration of the generated audio in seconds. -1 means a random duration between 30 and 240 seconds. Defaults to 60.0.
            
            scheduler: Scheduler type. Defaults to 'euler'.
            
            guidance_type: Guidance type for CFG. Defaults to 'apg'.
            
            guidance_scale: Overall guidance scale. Defaults to 15.0.
            
            number_of_steps: Number of inference steps. Defaults to 60.
            
            granularity_scale: Omega scale for APG guidance, or similar for other CFG types. Defaults to 10.0.
            
            guidance_interval: Guidance interval. Defaults to 0.5.
            
            min_guidance_scale: Minimum guidance scale. Defaults to 3.0.
            
            tag_guidance_scale: Guidance scale for tags (text prompt). Defaults to 0.0.
            
            lyric_guidance_scale: Guidance scale for lyrics. Defaults to 0.0.
            
            guidance_interval_decay: Guidance interval decay. Defaults to 0.0.
            
            lyrics: Lyrics for the music. Use [verse], [chorus], and [bridge] to separate different parts of the lyrics. Use [instrumental] or [inst] to generate instrumental music Optional.
            
        """
        return self.submit_job("/predict", tags=tags, seed=seed, duration=duration, scheduler=scheduler, guidance_type=guidance_type, guidance_scale=guidance_scale, number_of_steps=number_of_steps, granularity_scale=granularity_scale, guidance_interval=guidance_interval, min_guidance_scale=min_guidance_scale, tag_guidance_scale=tag_guidance_scale, lyric_guidance_scale=lyric_guidance_scale, guidance_interval_decay=guidance_interval_decay, lyrics=lyrics, **kwargs)
     