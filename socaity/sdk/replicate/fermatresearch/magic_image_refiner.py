from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class magic_image_refiner(FastSDK):
    """
    Generated client for fermatresearch/magic-image-refiner
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="52c089e7-8c07-4a9a-a862-01b7d6afd1e4", api_key=api_key)
    
    def predictions(self, hdr: float = 0.0, steps: int = 20, scheduler: str = 'DDIM', creativity: float = 0.25, guess_mode: bool = False, resolution: str = 'original', resemblance: float = 0.75, guidance_scale: float = 7.0, negative_prompt: str = 'teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant', mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            hdr: HDR improvement over the original image Defaults to 0.0.
            
            steps: Steps Defaults to 20.
            
            scheduler: Choose a scheduler. Defaults to 'DDIM'.
            
            creativity: Denoising strength. 1 means total destruction of the original image Defaults to 0.25.
            
            guess_mode: In this mode, the ControlNet encoder will try best to recognize the content of the input image even if you remove all prompts. The `guidance_scale` between 3.0 and 5.0 is recommended. Defaults to False.
            
            resolution: Image resolution Defaults to 'original'.
            
            resemblance: Conditioning scale for controlnet Defaults to 0.75.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.0.
            
            negative_prompt: Negative prompt Defaults to 'teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant'.
            
            mask: When provided, refines some section of the image. Must be the same size as the image Optional.
            
            seed: Seed Optional.
            
            image: Image to refine Optional.
            
            prompt: Prompt for the model Optional.
            
        """
        return self.submit_job("/predictions", hdr=hdr, steps=steps, scheduler=scheduler, creativity=creativity, guess_mode=guess_mode, resolution=resolution, resemblance=resemblance, guidance_scale=guidance_scale, negative_prompt=negative_prompt, mask=mask, seed=seed, image=image, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions