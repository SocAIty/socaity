from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class sdxl_controlnet(FastSDK):
    """
    Generated client for lucataco/sdxl-controlnet
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="53f34abc-e7b4-48e9-87ca-a3e4caf037c4", api_key=api_key)
    
    def predictions(self, seed: int = 0, prompt: str = 'aerial view, a futuristic research complex in a bright foggy jungle, hard lighting', condition_scale: float = 0.5, negative_prompt: str = 'low quality, bad quality, sketches', num_inference_steps: int = 50, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
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
        return self.submit_job("/predictions", seed=seed, prompt=prompt, condition_scale=condition_scale, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions