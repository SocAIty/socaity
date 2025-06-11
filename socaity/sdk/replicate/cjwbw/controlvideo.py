from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class controlvideo(FastSDK):
    """
    Generated client for controlvideo
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="49f44d3b-5893-4b0a-90f2-269e4b8f6593", api_key=api_key)
    
    def predict(self, video_path: Union[MediaFile, str, bytes], prompt: str = 'A striking mallard floats effortlessly on the sparkling pond.', condition: str = 'depth', video_length: int = 15, is_long_video: bool = False, guidance_scale: float = 12.5, smoother_steps: str = '19, 20', num_inference_steps: int = 50, seed: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video_path: source video
            
            prompt: Text description of target video Defaults to 'A striking mallard floats effortlessly on the sparkling pond.'.
            
            condition: Condition of structure sequence Defaults to 'depth'.
            
            video_length: Length of synthesized video Defaults to 15.
            
            is_long_video: Whether to use hierarchical sampler to produce long video Defaults to False.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 12.5.
            
            smoother_steps: Timesteps at which using interleaved-frame smoother, separate with comma Defaults to '19, 20'.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", video_path=video_path, prompt=prompt, condition=condition, video_length=video_length, is_long_video=is_long_video, guidance_scale=guidance_scale, smoother_steps=smoother_steps, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
     