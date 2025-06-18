from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class open_dalle_v1_1(FastSDK):
    """
    Generated client for lucataco/open-dalle-v1-1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="142dd900-d9c7-475d-8255-f0d8c9f38de5", api_key=api_key)
    
    def predictions(self, width: int = 1024, height: int = 1024, prompt: str = 'black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed', scheduler: str = 'KarrasDPM', num_outputs: int = 1, guidance_scale: float = 7.5, apply_watermark: bool = True, negative_prompt: str = 'worst quality, low quality', prompt_strength: float = 0.8, num_inference_steps: int = 60, disable_safety_checker: bool = False, mask: Optional[Union[MediaFile, str, bytes]] = None, seed: Optional[int] = None, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed'.
            
            scheduler: scheduler Defaults to 'KarrasDPM'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 7.5.
            
            apply_watermark: Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking. Defaults to True.
            
            negative_prompt: Negative Input prompt Defaults to 'worst quality, low quality'.
            
            prompt_strength: Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps 60-70 for best detail, 35 for fast Defaults to 60.
            
            disable_safety_checker: Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety Defaults to False.
            
            mask: Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted. Optional.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            image: Input image for img2img or inpaint mode Optional.
            
        """
        return self.submit_job("/predictions", width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, apply_watermark=apply_watermark, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, disable_safety_checker=disable_safety_checker, mask=mask, seed=seed, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions