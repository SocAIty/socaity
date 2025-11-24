from fastsdk import FastClient, APISeex
from typing import Literal

from media_toolkit import MediaFile


class wan_2_2_i2v_fast(FastClient):
    """
    Generated client based on wan-video/wan-2-2-i2v-fast format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="10b5ff37-90e0-4051-94f4-b9dc199eed59", api_key=api_key)
    
    def predictions(self, image: MediaFile, prompt: str, seed: int = 42, go_fast: bool = True, num_frames: int = 81, resolution: Literal["480p", "720p"] = '720p', aspect_ratio: Literal["16:9", "9:16"] = '16:9', sample_shift: float = 12.0, frames_per_second: int = 16, disable_safety_checker: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image to generate video from.
            
            prompt: Prompt for video generation
            
            seed: Random seed. Leave blank for random Defaults to 42.
            
            go_fast: Go fast Defaults to True.
            
            num_frames: Number of video frames. 81 frames give the best results Defaults to 81.
            
            resolution: Resolution of video. 16:9 corresponds to 832x480px, and 9:16 is 480x832px Defaults to '720p'.
            
            aspect_ratio: Aspect ratio of video. 16:9 corresponds to 832x480px, and 9:16 is 480x832px Defaults to '16:9'.
            
            sample_shift: Sample shift factor Defaults to 12.0.
            
            frames_per_second: Frames per second. Note that the pricing of this model is based on the video duration at 16 fps Defaults to 16.
            
            disable_safety_checker: Disable safety checker for generated video. Defaults to False.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, seed=seed, go_fast=go_fast, num_frames=num_frames, resolution=resolution, aspect_ratio=aspect_ratio, sample_shift=sample_shift, frames_per_second=frames_per_second, disable_safety_checker=disable_safety_checker, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
