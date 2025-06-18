from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class wan2_1_with_lora(FastSDK):
    """
    Generated client for fofr/wan2-1-with-lora
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bc1e7c1e-2347-4085-b329-a03904a4514e", api_key=api_key)
    
    def predictions(self, prompt: str, model: str = '14b', frames: int = 81, fast_mode: str = 'Balanced', resolution: str = '480p', aspect_ratio: str = '16:9', sample_shift: float = 8.0, sample_steps: int = 30, negative_prompt: str = '', lora_strength_clip: float = 1.0, sample_guide_scale: float = 5.0, lora_strength_model: float = 1.0, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, lora_url: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Text prompt for video generation
            
            model: The model to use. 1.3b is faster, but 14b is better quality. A LORA either works with 1.3b or 14b, depending on the version it was trained on. Defaults to '14b'.
            
            frames: The number of frames to generate (1 to 5 seconds) Defaults to 81.
            
            fast_mode: Speed up generation with different levels of acceleration. Faster modes may degrade quality somewhat. The speedup is dependent on the content, so different videos may see different speedups. Defaults to 'Balanced'.
            
            resolution: The resolution of the video. 720p is not supported for 1.3b. Defaults to '480p'.
            
            aspect_ratio: The aspect ratio of the video. 16:9, 9:16, 1:1, etc. Defaults to '16:9'.
            
            sample_shift: Sample shift factor Defaults to 8.0.
            
            sample_steps: Number of generation steps. Fewer steps means faster generation, at the expensive of output quality. 30 steps is sufficient for most prompts Defaults to 30.
            
            negative_prompt: Things you do not want to see in your video Defaults to ''.
            
            lora_strength_clip: Strength of the LORA applied to the CLIP model. 0.0 is no LORA. Defaults to 1.0.
            
            sample_guide_scale: Higher guide scale makes prompt adherence better, but can reduce variation Defaults to 5.0.
            
            lora_strength_model: Strength of the LORA applied to the model. 0.0 is no LORA. Defaults to 1.0.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
            image: Image to use as a starting frame for image to video generation. Optional.
            
            lora_url: Optional: The URL of a LORA to use Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, model=model, frames=frames, fast_mode=fast_mode, resolution=resolution, aspect_ratio=aspect_ratio, sample_shift=sample_shift, sample_steps=sample_steps, negative_prompt=negative_prompt, lora_strength_clip=lora_strength_clip, sample_guide_scale=sample_guide_scale, lora_strength_model=lora_strength_model, seed=seed, image=image, lora_url=lora_url, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions