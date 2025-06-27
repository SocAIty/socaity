from fastsdk import FastSDK, APISeex
from typing import Optional


class hunyuan_video(FastSDK):
    """
    Generated client for tencent/hunyuan-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fadd9278-de64-4d38-bfab-dc987511fc0a", api_key=api_key)
    
    def predictions(self, fps: int = 24, width: int = 864, height: int = 480, prompt: str = 'A cat walks on the grass, realistic style', infer_steps: int = 50, video_length: int = 129, embedded_guidance_scale: float = 6.0, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            fps: Frames per second of the output video Defaults to 24.
            
            width: Width of the video in pixels (must be divisible by 16) Defaults to 864.
            
            height: Height of the video in pixels (must be divisible by 16) Defaults to 480.
            
            prompt: The prompt to guide the video generation Defaults to 'A cat walks on the grass, realistic style'.
            
            infer_steps: Number of denoising steps Defaults to 50.
            
            video_length: Number of frames to generate (must be 4k+1, ex: 49 or 129) Defaults to 129.
            
            embedded_guidance_scale: Guidance scale Defaults to 6.0.
            
            seed: Random seed (leave empty for random) Optional.
            
        """
        return self.submit_job("/predictions", fps=fps, width=width, height=height, prompt=prompt, infer_steps=infer_steps, video_length=video_length, embedded_guidance_scale=embedded_guidance_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions