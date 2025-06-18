from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class pia(FastSDK):
    """
    Generated client for open-mmlab/pia
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c31fd67c-4a25-423f-86db-1a30670b127a", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], prompt: str, style: str = '3d_cartoon', max_size: int = 512, motion_scale: int = 1, guidance_scale: float = 7.5, sampling_steps: int = 25, negative_prompt: str = 'wrong white balance, dark, sketches,worst quality,low quality, deformed, distorted, disfigured, bad eyes, wrong lips, weird mouth, bad teeth, mutated hands and fingers, bad anatomy,wrong anatomy, amputation, extra limb, missing limb, floating,limbs, disconnected limbs, mutation, ugly, disgusting, bad_pictures, negative_hand-neg', animation_length: int = 16, ip_adapter_scale: float = 0.0, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            prompt: Input prompt.
            
            style: Choose a style Defaults to '3d_cartoon'.
            
            max_size: Max size (The long edge of the input image will be resized to this value, larger value means slower inference speed) Defaults to 512.
            
            motion_scale: Larger value means larger motion but less identity consistency. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            sampling_steps: Number of denoising steps Defaults to 25.
            
            negative_prompt: Things do not show in the output. Defaults to 'wrong white balance, dark, sketches,worst quality,low quality, deformed, distorted, disfigured, bad eyes, wrong lips, weird mouth, bad teeth, mutated hands and fingers, bad anatomy,wrong anatomy, amputation, extra limb, missing limb, floating,limbs, disconnected limbs, mutation, ugly, disgusting, bad_pictures, negative_hand-neg'.
            
            animation_length: Length of the output Defaults to 16.
            
            ip_adapter_scale: Scale for classifier-free guidance Defaults to 0.0.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, style=style, max_size=max_size, motion_scale=motion_scale, guidance_scale=guidance_scale, sampling_steps=sampling_steps, negative_prompt=negative_prompt, animation_length=animation_length, ip_adapter_scale=ip_adapter_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions