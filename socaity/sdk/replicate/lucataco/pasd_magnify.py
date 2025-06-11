from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class pasd_magnify(FastSDK):
    """
    Generated client for pasd_magnify
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="422f1d97-2fd1-4c54-a883-d16b4fe25f7b", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], prompt: str = 'Frog, clean, high-resolution, 8k, best quality, masterpiece', n_prompt: str = 'dotted, noise, blur, lowres, oversmooth, longbody, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality', denoise_steps: int = 20, guidance_scale: float = 7.5, upsample_scale: int = 2, conditioning_scale: float = 1.1, seed: Optional[int] = None, **kwargs):
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
        return self.submit_job("/predict", image=image, prompt=prompt, n_prompt=n_prompt, denoise_steps=denoise_steps, guidance_scale=guidance_scale, upsample_scale=upsample_scale, conditioning_scale=conditioning_scale, seed=seed, **kwargs)
     