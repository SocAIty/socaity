from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class seesr(FastSDK):
    """
    Generated client for seesr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b57a9946-e27a-4582-9206-5ed5d64868c9", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], seed: int = 231, cfg_scale: float = 5.5, user_prompt: str = '', sample_times: int = 1, scale_factor: int = 4, negative_prompt: str = 'dotted, noise, blur, lowres, smooth', positive_prompt: str = 'clean, high-resolution, 8k', latent_tiled_size: int = 320, num_inference_steps: int = 50, latent_tiled_overlap: int = 4, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            seed: Seed Defaults to 231.
            
            cfg_scale: Guidance scale, set value to >1 to use Defaults to 5.5.
            
            user_prompt: Prompt to condition on Defaults to ''.
            
            sample_times: Number of samples to generate Defaults to 1.
            
            scale_factor: Scale factor Defaults to 4.
            
            negative_prompt: Prompt to remove Defaults to 'dotted, noise, blur, lowres, smooth'.
            
            positive_prompt: Prompt to add Defaults to 'clean, high-resolution, 8k'.
            
            latent_tiled_size: Size of latent tiles Defaults to 320.
            
            num_inference_steps: Number of inference steps Defaults to 50.
            
            latent_tiled_overlap: Overlap of latent tiles Defaults to 4.
            
        """
        return self.submit_job("/predict", image=image, seed=seed, cfg_scale=cfg_scale, user_prompt=user_prompt, sample_times=sample_times, scale_factor=scale_factor, negative_prompt=negative_prompt, positive_prompt=positive_prompt, latent_tiled_size=latent_tiled_size, num_inference_steps=num_inference_steps, latent_tiled_overlap=latent_tiled_overlap, **kwargs)
     