from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class mmaudio(FastSDK):
    """
    Generated client for mmaudio
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="410272b9-90c7-4df7-8e0c-a349b204a48f", api_key=api_key)
    
    def predict(self, prompt: str = '', duration: float = 8.0, num_steps: int = 25, cfg_strength: float = 4.5, negative_prompt: str = 'music', seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, video: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Text prompt for generated audio Defaults to ''.
            
            duration: Duration of output in seconds Defaults to 8.0.
            
            num_steps: Number of inference steps Defaults to 25.
            
            cfg_strength: Guidance strength (CFG) Defaults to 4.5.
            
            negative_prompt: Negative prompt to avoid certain sounds Defaults to 'music'.
            
            seed: Random seed. Use -1 or leave blank to randomize the seed Optional.
            
            image: Optional image file for image-to-audio generation (experimental) Optional.
            
            video: Optional video file for video-to-audio generation Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, duration=duration, num_steps=num_steps, cfg_strength=cfg_strength, negative_prompt=negative_prompt, seed=seed, image=image, video=video, **kwargs)
     