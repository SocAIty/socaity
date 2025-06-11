from fastsdk.fastSDK import FastSDK
from typing import Optional


class hunyuan_video(FastSDK):
    """
    Generated client for hunyuan_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="de473a3a-a349-40e6-af9a-b6dd2241d083", api_key=api_key)
    
    def predict(self, fps: int = 24, width: int = 864, height: int = 480, prompt: str = 'A cat walks on the grass, realistic style', infer_steps: int = 50, video_length: int = 129, embedded_guidance_scale: float = 6.0, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
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
        return self.submit_job("/predict", fps=fps, width=width, height=height, prompt=prompt, infer_steps=infer_steps, video_length=video_length, embedded_guidance_scale=embedded_guidance_scale, seed=seed, **kwargs)
     