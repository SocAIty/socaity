from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class material_diffusion(FastSDK):
    """
    Generated client for tstramer/material-diffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ccb73456-e827-42e9-8e65-e571b7bd0c02", api_key=api_key)
    
    def predict(self, width: int = 512, height: int = 512, prompt: str = '', scheduler: str = 'K-LMS', num_outputs: int = 1, guidance_scale: float = 7.5, prompt_strength: float = 0.8, num_inference_steps: int = 50, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, init_image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image. Maximum size is 1024x768 or 768x1024 because of memory limits Defaults to 512.
            
            height: Height of output image. Maximum size is 1024x768 or 768x1024 because of memory limits Defaults to 512.
            
            prompt: Input prompt Defaults to ''.
            
            scheduler: Choose a scheduler. If you use an init image, PNDM will be used Defaults to 'K-LMS'.
            
            num_outputs: Number of images to output. If the NSFW filter is triggered, you may get fewer outputs than this. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            prompt_strength: Prompt strength when using init image. 1.0 corresponds to full destruction of information in init image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            mask: Black and white image to use as mask for inpainting over init_image. Black pixels are inpainted and white pixels are preserved. Tends to work better with prompt strength of 0.5-0.7. Consider using https://replicate.com/andreasjansson/stable-diffusion-inpainting instead. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            init_image: Inital image to generate variations of. Will be resized to the specified width and height Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, mask=mask, seed=seed, init_image=init_image, **kwargs)
     