from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class zeroscope_v2_xl(FastSDK):
    """
    Generated client for anotherjesse/zeroscope-v2-xl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9c9c5066-abb8-4a4f-acfb-20f7d57d203f", api_key=api_key)
    
    def predict(self, fps: int = 8, model: str = 'xl', width: int = 576, height: int = 320, prompt: str = 'An astronaut riding a horse', batch_size: int = 1, num_frames: int = 24, init_weight: float = 0.5, guidance_scale: float = 7.5, remove_watermark: bool = False, num_inference_steps: int = 50, seed: Optional[int] = None, init_video: Optional[Union[MediaFile, str, bytes]] = None, negative_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            fps: fps for the output video Defaults to 8.
            
            model: Model to use Defaults to 'xl'.
            
            width: Width of the output video Defaults to 576.
            
            height: Height of the output video Defaults to 320.
            
            prompt: Input prompt Defaults to 'An astronaut riding a horse'.
            
            batch_size: Batch size Defaults to 1.
            
            num_frames: Number of frames for the output video Defaults to 24.
            
            init_weight: Strength of init_video Defaults to 0.5.
            
            guidance_scale: Guidance scale Defaults to 7.5.
            
            remove_watermark: Remove watermark Defaults to False.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            init_video: URL of the initial video (optional) Optional.
            
            negative_prompt: Negative prompt Optional.
            
        """
        return self.submit_job("/predictions", fps=fps, model=model, width=width, height=height, prompt=prompt, batch_size=batch_size, num_frames=num_frames, init_weight=init_weight, guidance_scale=guidance_scale, remove_watermark=remove_watermark, num_inference_steps=num_inference_steps, seed=seed, init_video=init_video, negative_prompt=negative_prompt, **kwargs)
     