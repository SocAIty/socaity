from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class sdxl_controlnet(FastSDK):
    """
    Generated client for sdxl_controlnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="eb1c633c-78cf-495c-9f58-39ffd0516c6a", api_key=api_key)
    
    def predict(self, seed: int = 0, prompt: str = 'aerial view, a futuristic research complex in a bright foggy jungle, hard lighting', condition_scale: float = 0.5, negative_prompt: str = 'low quality, bad quality, sketches', num_inference_steps: int = 50, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            seed: Random seed. Set to 0 to randomize the seed Defaults to 0.
            
            prompt: Input prompt Defaults to 'aerial view, a futuristic research complex in a bright foggy jungle, hard lighting'.
            
            condition_scale: controlnet conditioning scale for generalization Defaults to 0.5.
            
            negative_prompt: Input Negative Prompt Defaults to 'low quality, bad quality, sketches'.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            image: Input image for img2img or inpaint mode Optional.
            
        """
        return self.submit_job("/predict", seed=seed, prompt=prompt, condition_scale=condition_scale, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, image=image, **kwargs)
     