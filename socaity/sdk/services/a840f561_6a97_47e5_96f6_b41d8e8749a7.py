from fastsdk import FastClient, APISeex

class hunyuan_video(FastClient):
    """
    Generated client based on tencent/hunyuan-video format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a840f561-6a97-47e5-96f6-b41d8e8749a7", api_key=api_key)
    
    def predictions(self, fps: int = 24, seed: int = 42, width: int = 864, height: int = 480, prompt: str = 'A cat walks on the grass, realistic style', infer_steps: int = 50, video_length: int = 129, embedded_guidance_scale: float = 6.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            fps: Frames per second of the output video Defaults to 24.
            
            seed: Random seed (leave empty for random) Defaults to 42.
            
            width: Width of the video in pixels (must be divisible by 16) Defaults to 864.
            
            height: Height of the video in pixels (must be divisible by 16) Defaults to 480.
            
            prompt: The prompt to guide the video generation Defaults to 'A cat walks on the grass, realistic style'.
            
            infer_steps: Number of denoising steps Defaults to 50.
            
            video_length: Number of frames to generate (must be 4k+1, ex: 49 or 129) Defaults to 129.
            
            embedded_guidance_scale: Guidance scale Defaults to 6.0.
            
        """
        return self.submit_job("/predictions", fps=fps, seed=seed, width=width, height=height, prompt=prompt, infer_steps=infer_steps, video_length=video_length, embedded_guidance_scale=embedded_guidance_scale, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
