from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class pasd_magnify(FastSDK):
    """
    Generated client for lucataco/pasd-magnify
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ebd8b0d6-d26d-45b8-8ec9-4d33df9f714d", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes], prompt: str = 'Frog, clean, high-resolution, 8k, best quality, masterpiece', n_prompt: str = 'dotted, noise, blur, lowres, oversmooth, longbody, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', denoise_steps: int = 20, guidance_scale: float = 7.5, upsample_scale: int = 2, conditioning_scale: float = 1.1, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            prompt: Prompt Defaults to 'Frog, clean, high-resolution, 8k, best quality, masterpiece'.
            
            n_prompt: Negative Prompt Defaults to 'dotted, noise, blur, lowres, oversmooth, longbody, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'.
            
            denoise_steps: Denoise Steps Defaults to 20.
            
            guidance_scale: Guidance Scale Defaults to 7.5.
            
            upsample_scale: Upsample Scale Defaults to 2.
            
            conditioning_scale: Conditioning Scale Defaults to 1.1.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, n_prompt=n_prompt, denoise_steps=denoise_steps, guidance_scale=guidance_scale, upsample_scale=upsample_scale, conditioning_scale=conditioning_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions