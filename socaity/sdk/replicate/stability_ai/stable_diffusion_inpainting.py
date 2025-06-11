from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class stable_diffusion_inpainting(FastSDK):
    """
    Generated client for stable_diffusion_inpainting
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1b52858a-5ca1-40f4-9715-b97914ee78bc", api_key=api_key)
    
    def predict(self, mask: Union[MediaFile, str, bytes], image: Union[MediaFile, str, bytes], width: int = 512, height: int = 512, prompt: str = 'a vision of paradise. unreal engine', scheduler: str = 'DPMSolverMultistep', num_outputs: int = 1, guidance_scale: float = 7.5, num_inference_steps: int = 50, disable_safety_checker: bool = False, seed: Optional[int] = None, negative_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            mask: Black and white image to use as mask for inpainting over the image provided. White pixels are inpainted and black pixels are preserved.
            
            image: Initial image to generate variations of. Will be resized to height x width
            
            width: Width of generated image in pixels. Needs to be a multiple of 64 Defaults to 512.
            
            height: Height of generated image in pixels. Needs to be a multiple of 64 Defaults to 512.
            
            prompt: Input prompt Defaults to 'a vision of paradise. unreal engine'.
            
            scheduler: Choose a scheduler. Defaults to 'DPMSolverMultistep'.
            
            num_outputs: Number of images to generate. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety) Defaults to False.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            negative_prompt: Specify things to not see in the output Optional.
            
        """
        return self.submit_job("/predict", mask=mask, image=image, width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, seed=seed, negative_prompt=negative_prompt, **kwargs)
     