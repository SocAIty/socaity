from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class wan_2_1_1_3b_vid2vid(FastSDK):
    """
    Generated client for lucataco/wan-2-1-1-3b-vid2vid
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="78b7326b-ca6a-4fcd-a4e6-11963900b560", api_key=api_key)
    
    def predictions(self, prompt: str, tiled: bool = True, cfg_scale: float = 6.0, num_frames: int = 81, aspect_ratio: str = '832x480', negative_prompt: str = 'low quality, blurry, distorted, disfigured, text, watermark', frames_per_second: int = 16, denoising_strength: float = 0.7, num_inference_steps: int = 40, seed: Optional[int] = None, input_video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Text prompt describing what you want to generate or modify
            
            tiled: Whether to use tiled sampling for better quality on larger videos Defaults to True.
            
            cfg_scale: Classifier free guidance scale (higher values strengthen prompt adherence) Defaults to 6.0.
            
            num_frames: Number of frames to generate in the output video Defaults to 81.
            
            aspect_ratio: Aspect ratio for the output video Defaults to '832x480'.
            
            negative_prompt: Negative prompt to specify what to avoid in the generation Defaults to 'low quality, blurry, distorted, disfigured, text, watermark'.
            
            frames_per_second: Number of frames per second in the output video Defaults to 16.
            
            denoising_strength: Strength of denoising when using video-to-video mode. Higher values change more content. Defaults to 0.7.
            
            num_inference_steps: Number of sampling steps (higher = better quality but slower) Defaults to 40.
            
            seed: Random seed for reproducible results (leave blank for random) Optional.
            
            input_video: Input video for video-to-video generation Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, tiled=tiled, cfg_scale=cfg_scale, num_frames=num_frames, aspect_ratio=aspect_ratio, negative_prompt=negative_prompt, frames_per_second=frames_per_second, denoising_strength=denoising_strength, num_inference_steps=num_inference_steps, seed=seed, input_video=input_video, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions