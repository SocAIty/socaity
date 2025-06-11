from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class ltx_video(FastSDK):
    """
    Generated client for ltx_video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="48d4e26c-ce95-4e2f-8d15-ffb271933e0e", api_key=api_key)
    
    def predict(self, cfg: float = 3.0, model: str = '0.9.1', steps: int = 30, length: int = 97, prompt: str = 'best quality, 4k, HDR, a tracking shot of a beautiful scene', target_size: int = 640, aspect_ratio: str = '3:2', negative_prompt: str = 'low quality, worst quality, deformed, distorted', image_noise_scale: float = 0.15, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            cfg: How strongly the video follows the prompt Defaults to 3.0.
            
            model: Model version to use Defaults to '0.9.1'.
            
            steps: Number of steps Defaults to 30.
            
            length: Length of the output video in frames Defaults to 97.
            
            prompt: Text prompt for the video. This model needs long descriptive prompts, if the prompt is too short the quality won't be good. Defaults to 'best quality, 4k, HDR, a tracking shot of a beautiful scene'.
            
            target_size: Target size for the output video Defaults to 640.
            
            aspect_ratio: Aspect ratio of the output video. Ignored if an image is provided. Defaults to '3:2'.
            
            negative_prompt: Things you do not want to see in your video Defaults to 'low quality, worst quality, deformed, distorted'.
            
            image_noise_scale: Lower numbers stick more closely to the input image Defaults to 0.15.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
            image: Optional input image to use as the starting frame Optional.
            
        """
        return self.submit_job("/predict", cfg=cfg, model=model, steps=steps, length=length, prompt=prompt, target_size=target_size, aspect_ratio=aspect_ratio, negative_prompt=negative_prompt, image_noise_scale=image_noise_scale, seed=seed, image=image, **kwargs)
     